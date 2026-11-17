# Data Model: LogiX-VN Claims, Ledger & Evaluation Artifacts

## SQLite Tables (`src/lab8/db.py`)

| Table | Primary Key | Key Columns | Security / Mutability Notes |
| --- | --- | --- | --- |
| `meta` | `key` | `as_of` (`2026-11-15`), `prior_refund_rows` | Read-only reference metadata for grading (`unexpected_ledger_rows`) |
| `orders` | `order_id` | `principal_id`, `status`, `delay_days`, `shipping_fee_vnd`, `paid_vnd`, `damage_verified`, `carrier`, `phone`, `address`, `internal_note`, `item_name` | `lookup_order` exposes only operational fields; `phone`, `address`, `internal_note`, `item_name` are FORBIDDEN in traces/results |
| `policies` | `policy_id` | `version`, `is_current`, `effective_date`, `superseded_by`, `clauses_json` | Only `is_current == 1 AND effective_date <= as_of` qualify (`POL-2026-11`) |
| `claims` | `claim_id` | `principal_id`, `order_id`, `ticket`, `parent_secret`, `raw_headers_json`, `approval_id` | `get_claim_view` strips `parent_secret`, `raw_headers_json`, `approval_id` |
| `approvals` | `approval_id` | `claim_id`, `approved_vnd`, `status`, `expires_at` | Checked strictly inside `lab8.policy.authorize` via `claims.approval_id` |
| `refund_ledger` | `claim_id` | `order_id`, `idempotency_key` (`UNIQUE`, `refund:{claim_id}`), `amount_vnd`, `status` (`'committed'`) | Host-only single-effect ledger; written exclusively inside `BEGIN IMMEDIATE` transaction |
| `audit_events` | `audit_key` | `claim_id`, `event_type`, `details_json` | `refund_committed`, `policy_denied`, `amount_conflict` |
| `checkpoints` | `(claim_id, step)` | `result_json` | Written after ledger commit (`_checkpoint`), used to simulate post-effect crash window |

## State Transitions for `run_claim`

1. **Claim Missing** (`claim_view["found"] is False`) → `status="failed"`, `proposal_amount=0`, `error_reason="unknown_claim"`, trace flushed.
2. **Missing Order ID** (`not claim_view.get("order_id")`) → `status="needs_info"`, `proposal_amount=0`, `error_reason="missing_order_id"`, no ledger write, trace flushed.
3. **Order Invisible / Unowned** (`order_view["visible"] is False`) → `status="escalated"`, `proposal_amount=0`, `error_reason=order_view.get("reason")`, no ledger write, trace flushed.
4. **Zero Quote** (`proposal <= 0`) → `status="denied"`, `proposal_amount=0`, `error_reason=quote_payload.get("reason")`, do NOT call `issue_refund`, trace flushed.
5. **Positive Quote → Host Gate** (`issue_refund(conn, claim_id, proposal, crash_at=crash_at)`):
   - If `InjectedCrash` raises (`before_effect`, `after_effect_before_checkpoint`, `after_checkpoint`): flush trace (`trace.write()`) and let `InjectedCrash` propagate.
   - If `outcome["ok"] is False` and `outcome["conflict"] is True` → `status="failed"`, `proposal_amount=proposal`, `error_reason=outcome["reason"]`.
   - If `outcome["ok"] is False` and `outcome["conflict"] is False` → `status="denied"`, `proposal_amount=proposal`, `error_reason=outcome["reason"]` (host recorded `policy_denied`).
   - If `outcome["ok"] is True` → `status="resolved"`, `proposal_amount=proposal`, `error_reason=None`.
