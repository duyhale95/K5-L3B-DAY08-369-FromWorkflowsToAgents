"""R2 ablation: keep swarm's model calls but disable the ticket-delay override."""

from dataclasses import replace
from unittest.mock import patch

from lab8.schemas import RunResult, make_run_id
from lab8.shapes import swarm_reference


def run_claim(
    claim_id: str,
    *,
    seed: int,
    store_path: str,
    crash_at: str | None = None,
) -> RunResult:
    """Run the ablation in the sequential benchmark's process."""
    shape = "swarm_order_only"
    run_id = make_run_id(shape, claim_id, seed)
    # Patch the swarm's local binding only. MockLLM still parses the same
    # prompt and records its usage. Give the variant a separate trace path.
    with (
        patch.object(swarm_reference, "parse_delay_days", return_value=None),
        patch.object(swarm_reference, "make_run_id", return_value=run_id),
    ):
        result = swarm_reference.run_claim(
            claim_id, seed=seed, store_path=store_path, crash_at=crash_at
        )
    return replace(result, shape=shape)
