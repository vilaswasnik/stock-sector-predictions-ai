# 🚀 Stock Sector Predictions AI

**AI-powered stock sector analysis with real-time market data and news sentiment.** A Flask API scores and ranks the 11 major US market sectors, blends technical indicators with headline sentiment, and serves the result to a web dashboard — so you can see at a glance which sectors are leading, which are lagging, and whether the market reads bullish, bearish, or neutral.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Not financial advice.** This is an analysis and learning tool; sector scores are model output, not recommendations.

## 📚 Quick links

| Document | Description |
|---|---|
| [⚡ QUICK_START.md](QUICK_START.md) | Get started in 2 minutes — essential commands and URLs |
| [⌨️ SHORTCUTS.md](SHORTCUTS.md) | Cheat sheet — commands, shortcuts, and tips |
| [📖 SETUP_GUIDE.md](stock-sector-ai/SETUP_GUIDE.md) | Detailed installation and configuration |
| [📰 NEWS_SENTIMENT_GUIDE.md](stock-sector-ai/NEWS_SENTIMENT_GUIDE.md) | How news sentiment analysis works |
| [📱 Application README](stock-sector-ai/README.md) | Full application features and architecture |

## ✨ Features

- **Real-time sector analysis** — live data for 11 sector ETFs: Technology (XLK), Healthcare (XLV), Financials (XLF), Energy (XLE), Consumer Discretionary (XLY), Industrials (XLI), Consumer Staples (XLP), Utilities (XLU), Real Estate (XLRE), Materials (XLB), Communication Services (XLC)
- **Weighted scoring engine** — momentum, trend, and volatility combined into a single comparable score per sector
- **News sentiment** — NewsAPI headlines per sector, sentiment-scored and blended into the ranking
- **Market regime detection** — bullish / bearish / neutral classification with a confidence level
- **Dashboard** — rankings, trend indicators, leading vs lagging sectors, and sentiment scores in one page
- **Demo mode** — if the data APIs are unavailable or rate-limited, the app falls back to built-in demo data automatically

## 🚀 Quick start

Prerequisites: Python 3.12+. API keys are optional (demo mode works without them); for live data get free-tier keys from [Alpha Vantage](https://www.alphavantage.co/support/#api-key) and [NewsAPI](https://newsapi.org/register).

```bash
git clone https://github.com/vilaswasnik/stock-sector-predictions-ai.git
cd stock-sector-predictions-ai/stock-sector-ai
cp .env.example .env        # add ALPHAVANTAGE_API_KEY and NEWSAPI_KEY for live data
cd ..
bash stock-sector-ai/run.sh # creates a venv, installs dependencies, starts the API
```

`run.sh` starts the Flask API (`api/app.py`) on port 8000. Then:

```bash
curl http://localhost:8000/api/status     # health/status
curl http://localhost:8000/api/sectors    # list tracked sectors
curl http://localhost:8000/api/analysis   # full analysis
curl http://localhost:8000/api/predict    # predictions
```

Open `stock-sector-ai/frontend/index.html` in a browser for the dashboard.

> **⚠️ Never commit your `.env`.** It holds real API keys, it is listed in `.gitignore` for exactly that reason, and keys that reach a public repo must be rotated.

## 🧠 How it works

1. **Data collection** — historical prices and volume from Yahoo Finance (yfinance), with Alpha Vantage as an alternate fetcher.
2. **Technical scoring (85%)** — momentum/20-day (30%), short-term/5-day trend (25%), medium-term/60-day (20%), recent/1-day performance (15%), minus a volatility penalty (10%).
3. **News sentiment (15%)** — sector headlines from NewsAPI are sentiment-scored; positive news lifts a sector's score, negative news lowers it.
4. **Prediction** — sectors are ranked; the spread between leaders and laggards plus score distribution drives the bullish/bearish/neutral call and its confidence.

## 🏗️ Project structure

```text
stock-sector-predictions-ai/
├── README.md, QUICK_START.md, SHORTCUTS.md, DOCUMENTATION_SUMMARY.md
└── stock-sector-ai/
    ├── run.sh                 # one-command start (venv + install + serve)
    ├── requirements.txt
    ├── .env.example           # ALPHAVANTAGE_API_KEY, NEWSAPI_KEY (copy to .env)
    ├── api/
    │   └── app.py             # Flask API — THE entry point (other app_*.py are experiments)
    ├── models/
    │   ├── sector_predictor.py    # technical scoring model
    │   └── enhanced_predictor.py  # scoring + news sentiment
    ├── utils/
    │   ├── sector_data.py         # Yahoo Finance fetcher
    │   ├── alphavantage_fetcher.py
    │   ├── news_sentiment.py      # NewsAPI sentiment
    │   ├── sector_stocks.py, demo_data.py
    └── frontend/
        └── index.html         # dashboard
```

## 🔧 Troubleshooting

- **Port 8000 already in use** — `lsof -ti :8000 | xargs kill -9`, then restart.
- **Module not found** — activate the venv (`source stock-sector-ai/venv/bin/activate`) and `pip install -r stock-sector-ai/requirements.txt`.
- **API rate limits** — the app switches to demo data automatically; wait for the quota to reset for live analysis.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT — see `LICENSE`.
