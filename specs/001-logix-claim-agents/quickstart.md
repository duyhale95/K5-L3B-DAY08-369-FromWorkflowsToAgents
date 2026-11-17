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
  - `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
  - Optional if `student_drop/` provided: `python -m lab8.benchmark --shapes workflow,single,orchestrator --cases student_drop/hidden_claims.jsonl --world student_drop/hidden_world_state.json --out reports/hidden_selfcheck.json`
  - `python -m pytest -q` and `python -m pytest -q -m student -o addopts=` and `python -m pytest -q tests/test_bonus_*.py`
  - Commit code + reports → run `git rev-parse --short HEAD` → update `report/team/decision_adr.md` & `TEAM.md` → commit → run `python -m lab8.check_submission` (`0 FAIL`) → `git push origin main`
