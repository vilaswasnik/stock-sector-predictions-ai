# Contributing to Stock Sector Predictions AI

Thanks for looking. This is a Python/Flask app that ranks US stock sectors with a weighted technical model plus NewsAPI sentiment, served to a static dashboard. Contributions of code, scoring improvements, docs, and bug reports are all welcome.

## Run it locally

Prerequisites: Python 3.12+. API keys are optional — without them the app runs on demo data.

```bash
git clone https://github.com/vilaswasnik/stock-sector-predictions-ai.git
cd stock-sector-predictions-ai/stock-sector-ai
cp .env.example .env   # optional: add ALPHAVANTAGE_API_KEY and NEWSAPI_KEY for live data
cd .. && bash stock-sector-ai/run.sh
curl http://localhost:8000/api/status
```

Ground rules:

- **API keys live in `.env` only — and `.env` is never committed.** It is in `.gitignore` ("DO NOT COMMIT") for a reason. If a key ever reaches the repo, it must be rotated and the file history-purged, not just deleted. Check `git status` before every commit.
- **One canonical app.** `api/app.py` is the entry point (`run.sh` runs it). Experiments belong in branches, not as additional `app_*.py` files in `api/`.
- **No generated files in commits:** no `*.log`, no `__pycache__`, no `venv/`.
- Scoring changes must be explained: if you touch the weights or indicators in `models/`, say what changed and why in the PR — the 85/15 technical/sentiment blend and the factor weights are the product's methodology, documented in the README.

## Filing an issue

Use GitHub Issues. A useful report includes: live data or demo mode, the endpoint or dashboard element involved, what you expected, what you got, and (for data issues) the sector and approximate time — market data is time-sensitive.

## PR process

1. Fork, branch from `main`, keep the change focused.
2. Run the API locally and hit `/api/status` and `/api/analysis`; run `test_app.py` / `quick_test.py` if your change touches the API or models.
3. Describe in the PR how you verified, and include before/after sector rankings if scoring changed.
4. One approval from the maintainer merges.

## Good first issues

Concrete, evidence-based starting points (each cites where the gap is):

1. **Archive the spare Flask apps.** `api/` holds nine app variants (`app_charts.py`, `app_final.py`, `app_full.py`, `app_inline.py`, `app_simple.py`, `app_simple2.py`, `app_working.py`, plus `.backup` files) next to the canonical `app.py`. Move the keepers to an `experiments/` folder with a note, delete the duplicates, and make sure `run.sh` + the README point only at `app.py`.
2. **Clean the tracked generated files.** `server*.log` files and `__pycache__/` folders are committed despite matching `.gitignore` rules — remove them from tracking (`git rm -r --cached`) so the ignore rules take effect.
3. **Fix the root README's dead link.** Its Quick Links table points to `SETUP_GUIDE.md` at the repo root; the file actually lives in `stock-sector-ai/`. (The README draft in the promotion package already corrects this.)
4. **Add a scoring unit test.** The weights in `models/sector_predictor.py` have no tests — a fixture-data test asserting the ranking order for a known input would lock the methodology in.
