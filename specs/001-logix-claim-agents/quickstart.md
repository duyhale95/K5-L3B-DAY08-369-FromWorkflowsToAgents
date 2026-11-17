# Quickstart & Sequential 5-Member Handoff Protocol

All lab commands below MUST be executed inside `src/` using the Python 3.11–3.13 virtual environment.

## 1. Environment Setup (Each Member on First Pull)

Windows PowerShell:
```powershell
cd src
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m lab8.smoke
```

If using Spec Kit scripts from repo root in a fresh checkout, point Spec Kit to this feature folder:
```powershell
$env:SPECIFY_FEATURE_DIRECTORY = "specs/001-logix-claim-agents"
```

## 2. Sequential Pull → Implement → Verify → Push Gate

Before starting your assigned phase:
```bash
git checkout main
git pull origin main
```

Required verification checks before pushing to `main`:

- **Member 1 (Hà Lê Duy — `workflow`)**:
  - `python -m lab8.smoke`
  - `python -m pytest -q` (host gate green)
  - `python -m pytest -q -m student -o addopts= -k workflow` (`62 passed`)
- **Member 2 (`single`)**:
  - `python -m pytest -q` (host gate green)
  - `python -m pytest -q -m student -o addopts= -k "workflow or single"` (`124 passed`)
- **Member 3 (`orchestrator`)**:
  - `python -m pytest -q` (host gate green)
  - `python -m pytest -q -m student -o addopts=` (`248 passed` — note `swarm` asserts its expected miss on C-002 seed 55)
- **Member 4 (CP4 Must-Pass Audit + Bonus B7)**:
  - `python -m pytest -q` (includes `test_must_pass_audit.py`)
  - `python -m pytest -q tests/test_bonus_grader_audit.py`
  - `python -m lab8.crash_test --count 20 --out reports/crash.json` (`crash_safety 20/20`)
- **Member 5 (CP5 Benchmark + Reports + Submission Gate)**:
  - `python -m lab8.crash_test --count 20 --out reports/crash.json` (`20/20`)
  - `python -m lab8.benchmark --shapes "workflow,single,orchestrator,swarm" --cases data/public_claims.jsonl --seeds "11,22,33,44,55" --out reports/benchmark.json`
  - Optional if `student_drop/` provided: `python -m lab8.benchmark --shapes workflow,single,orchestrator --cases student_drop/hidden_claims.jsonl --world student_drop/hidden_world_state.json --out reports/hidden_selfcheck.json`
  - `python -m pytest -q`, `python -m pytest -q -m student -o addopts=`, and `python -m pytest -q tests/test_bonus_grader_audit.py`
  - Commit code and generated evidence, record that commit in `report/team/decision_adr.md` and `TEAM.md`, then commit the written reports. Run `python -m lab8.check_submission` (`0 FAIL`), push `nguyenthienbao`, and open a PR to `main`.

## 3. Team Lead Review and Submission

1. On the PR branch, run the Member 5 checks above. Re-run the commands in [research_card.md](../../report/team/research_card.md) and [bonus_report.md](../../report/team/bonus_report.md) to reproduce both experiments. Use `git diff --exit-code -- reports/benchmark.json reports/crash.json reports/research_r2.json reports/bonus_grader_audit.json` from `src/` to verify the evidence.
2. Merge the PR with **Create a merge commit** to preserve the evidence and contribution hashes. From the merged branch, confirm `git merge-base --is-ancestor 5c027d8 HEAD` succeeds and run `python -m lab8.check_submission` from `src/`.
3. Check the repository name and instructor access against [SUBMISSION.md](../../SUBMISSION.md). The documented name is `K5-L3A-DAY08-369-FromWorkflowsToAgents`; follow the coach's instructions if the class uses a different name. Give all five members the final repository URL for their individual LMS submissions.
