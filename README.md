# 🚀 Stock Sector Predictions AI

**AI-powered stock sector analysis with real-time market data and news sentiment**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📚 Quick Links

| Document | Description |
|----------|-------------|
| [⚡ QUICK_START.md](QUICK_START.md) | **Get started in 2 minutes** - Essential commands and URLs |
| [⌨️ SHORTCUTS.md](SHORTCUTS.md) | **Cheat sheet** - All commands, shortcuts, and tips |
| [📖 SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed installation and configuration guide |
| [📰 NEWS_SENTIMENT_GUIDE.md](stock-sector-ai/NEWS_SENTIMENT_GUIDE.md) | News sentiment analysis documentation |
| [📱 Application README](stock-sector-ai/README.md) | Full application features and architecture |

---

## 🎯 One-Command Start

```bash
cd stock-sector-ai && source venv/bin/activate && cd api && python app.py
```

Then open: **http://localhost:8000/dashboard**

---

## ✨ Features

- 🤖 **AI-Powered Predictions** - Machine learning analyzes 11 major market sectors
- 📊 **Real-Time Data** - Integration with Alpha Vantage for live market data
- 📰 **News Sentiment Analysis** - NewsAPI integration for enhanced predictions
- 📈 **Technical Analysis** - RSI, MACD, Bollinger Bands, and more
- 🎨 **Beautiful Dashboard** - Interactive web interface with real-time updates
- 💾 **Demo Mode** - Fallback data when API limits reached
- 🔄 **Auto-Refresh** - Dashboard updates automatically

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Virtual environment (included)
- API Keys (free tier available)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vilaswasnik/stock-sector-predictions-ai.git
   cd stock-sector-predictions-ai/stock-sector-ai
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Configure API keys** (optional - app works in demo mode)
   ```bash
   # Edit .env file
   nano .env
   
   # Add your keys:
   ALPHAVANTAGE_API_KEY=your_key_here
   NEWSAPI_KEY=your_key_here
   ```

4. **Start the application**
   ```bash
   cd api
   python app.py
   ```

5. **Open dashboard**
   - Navigate to: http://localhost:8000/dashboard
   - Or run: `$BROWSER http://localhost:8000/dashboard`

---

## 🎮 Usage

### API Endpoints

```bash
# Check status
curl http://localhost:8000/api/status

# Get full analysis
curl http://localhost:8000/api/analysis

# Get predictions
curl http://localhost:8000/api/predict

# List all sectors
curl http://localhost:8000/api/sectors
```

### Dashboard Features
- **Real-time sector rankings** with AI scores
- **Market trend indicators** (Bullish/Bearish/Neutral)
- **Leading vs Lagging sectors** identification
- **Technical indicators** visualization
- **News sentiment scores** for each sector
- **AI-generated insights** and recommendations

---

## 📊 Tracked Sectors

| Sector | ETF Symbol | Category |
|--------|-----------|----------|
| Technology | XLK | Growth |
| Healthcare | XLV | Defensive |
| Financials | XLF | Cyclical |
| Energy | XLE | Cyclical |
| Consumer Discretionary | XLY | Cyclical |
| Industrials | XLI | Cyclical |
| Consumer Staples | XLP | Defensive |
| Utilities | XLU | Defensive |
| Real Estate | XLRE | Interest-Sensitive |
| Materials | XLB | Cyclical |
| Communication Services | XLC | Growth |

---

## 🔧 Configuration

### API Keys (Free Tier)

**Alpha Vantage** (Market Data)
- Sign up: https://www.alphavantage.co/support/#api-key
- Limit: 25 requests/day, 5 requests/minute
- Free forever

**NewsAPI** (Sentiment Analysis)
- Sign up: https://newsapi.org/register
- Limit: 100 requests/day
- Free for development

### Environment Variables

```bash
# .env file
ALPHAVANTAGE_API_KEY=your_alpha_vantage_key
NEWSAPI_KEY=your_newsapi_key
PORT=8000
DEBUG=True
```

---

## 🏗️ Project Structure

```
stock-sector-predictions-ai/
├── stock-sector-ai/
│   ├── api/
│   │   └── app.py              # Flask application
│   ├── models/
│   │   ├── sector_predictor.py      # Original AI model
│   │   └── enhanced_predictor.py    # With news sentiment
│   ├── utils/
│   │   ├── sector_data.py           # Yahoo Finance data
│   │   ├── alphavantage_fetcher.py  # Alpha Vantage API
│   │   ├── news_sentiment.py        # NewsAPI integration
│   │   └── demo_data.py             # Fallback demo data
│   ├── frontend/
│   │   └── index.html               # Dashboard UI
│   ├── .env                         # Configuration
│   ├── requirements.txt             # Dependencies
│   └── venv/                        # Virtual environment
├── QUICK_START.md                   # Quick reference guide
├── SHORTCUTS.md                     # Commands cheat sheet
├── SETUP_GUIDE.md                   # Detailed setup
└── README.md                        # This file
```

---

## 🧠 How It Works

### AI Scoring Algorithm

The AI model calculates sector scores using weighted factors:

1. **Technical Analysis (85%)**
   - Momentum (30%) - 20-day price performance
   - Short-term (25%) - 5-day trend
   - Medium-term (20%) - 60-day performance
   - Recent Performance (15%) - 1-day returns
   - Volatility Penalty (10%) - Risk adjustment

2. **News Sentiment (15%)**
   - Positive news → Score boost
   - Negative news → Score reduction
   - Neutral news → No impact

### Prediction Logic

- **Bullish Market**: Top 3 sectors strong, bottom 3 weak
- **Bearish Market**: All sectors declining
- **Neutral Market**: Mixed signals across sectors
- **Confidence**: Based on score distribution and volatility

---

## 🛠️ Troubleshooting

### Common Issues

**Port 8000 already in use**
```bash
lsof -ti :8000 | xargs kill -9
```

**Module not found errors**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**API rate limits exceeded**
- App automatically switches to demo mode
- Wait 24 hours for quota reset
- Or use demo mode: comment out API keys in .env

**Dashboard not loading**
```bash
# Check if server is running
ps aux | grep "python app.py"

# Check server logs
# Look for errors in terminal output
```

---

## 📈 Performance

- **Startup Time**: < 5 seconds
- **API Response**: < 1 second (with cache)
- **Dashboard Load**: < 2 seconds
- **Memory Usage**: ~50-100 MB
- **CPU Usage**: < 5% idle, < 20% during analysis

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Alpha Vantage** - Market data API
- **NewsAPI** - News sentiment data
- **Yahoo Finance** - Fallback data source
- **Flask** - Web framework
- **scikit-learn** - Machine learning
- **pandas** - Data analysis
- **TextBlob** - Sentiment analysis

---

## 📞 Support

- **Documentation**: See Quick Start and Setup guides
- **Issues**: [GitHub Issues](https://github.com/vilaswasnik/stock-sector-predictions-ai/issues)
- **Questions**: Open a discussion on GitHub

---

## 🎯 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] Additional data providers (Finnhub, Twelve Data)
- [ ] Historical backtesting
- [ ] Email/SMS alerts
- [ ] Mobile app
- [ ] Docker containerization
- [ ] Advanced charting
- [ ] Portfolio tracking

---

**⭐ Star this repo if you find it useful!**

**Last Updated**: January 26, 2026  
**Version**: 1.0  
**Status**: Production Ready ✅