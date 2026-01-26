# 🚀 AI Stock Sector Prediction App

An AI-powered application that analyzes and predicts leading market sectors using machine learning, real-time data, and advanced technical indicators.

## Features

- **Real-Time Sector Analysis**: Fetches live data from 11 major market sector ETFs
- **AI Prediction Engine**: Machine learning model that scores and ranks sectors
- **Market Trend Detection**: Identifies bullish, bearish, or neutral market conditions
- **Performance Metrics**: Tracks 1-day, 5-day, 20-day, and 60-day returns
- **Interactive Dashboard**: Beautiful web interface with real-time updates
- **Smart Insights**: AI-generated recommendations and alerts

## Market Sectors Tracked

- Technology (XLK)
- Healthcare (XLV)
- Financials (XLF)
- Energy (XLE)
- Consumer Discretionary (XLY)
- Industrials (XLI)
- Consumer Staples (XLP)
- Utilities (XLU)
- Real Estate (XLRE)
- Materials (XLB)
- Communication Services (XLC)

## How It Works

### 1. Data Collection
- Fetches historical price data from Yahoo Finance
- Collects volume and volatility metrics
- Updates in real-time on demand

### 2. AI Analysis
The AI model calculates sector scores using:
- **Momentum (30%)**: 20-day price performance
- **Short-term (25%)**: 5-day price trend
- **Medium-term (20%)**: 60-day performance
- **Recent Performance (15%)**: 1-day returns
- **Volatility Penalty (10%)**: Risk adjustment
- **Volume Confirmation**: Higher volume = stronger signal

### 3. Predictions
- Ranks all sectors by AI score
- Identifies top 3 leading sectors
- Flags bottom 3 lagging sectors
- Predicts overall market trend with confidence level

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for market data

### Quick Start

1. **Run the application:**
```bash
./run.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Start the Flask API server

2. **Access the dashboard:**
Open your browser and navigate to:
```
http://localhost:5000
```

Or open the frontend directly:
```
frontend/index.html
```

## API Endpoints

### GET /
Health check endpoint
```json
{
  "status": "online",
  "service": "Stock Sector Prediction API",
  "version": "1.0.0"
}
```

### GET /api/analysis
Get complete sector analysis with AI predictions

Query params:
- `period`: Data period (1mo, 3mo, 6mo, 1y) - default: 3mo

Response includes:
- Market trend (bullish/bearish/neutral)
- Top 3 leading sectors
- Bottom 3 lagging sectors
- All sectors ranking
- AI-powered insights

### GET /api/predict
Get top 5 sectors predicted to lead the market

### GET /api/sectors
List all available sectors

### GET /api/sector/<sector_name>
Get detailed analysis for a specific sector

## Project Structure

```
stock-sector-ai/
├── api/
│   └── app.py              # Flask API server
├── models/
│   ├── __init__.py
│   └── sector_predictor.py # AI prediction model
├── utils/
│   ├── __init__.py
│   └── sector_data.py      # Data fetcher
├── frontend/
│   └── index.html          # Web dashboard
├── data/                   # Data storage (created at runtime)
├── requirements.txt        # Python dependencies
├── run.sh                  # Startup script
└── README.md              # This file
```

## Usage Examples

### Using the Web Dashboard
1. Start the server with `./run.sh`
2. Open the dashboard in your browser
3. Select analysis period (1mo, 3mo, 6mo, or 1y)
4. Click "Refresh Analysis" to update data
5. View leading sectors, market trend, and AI insights

### Using the API
```bash
# Get full analysis
curl http://localhost:5000/api/analysis?period=3mo

# Get predictions
curl http://localhost:5000/api/predict

# Get specific sector
curl http://localhost:5000/api/sector/Technology
```

## Understanding the Output

### AI Score
- **Positive score**: Sector is performing well, likely to continue leading
- **Negative score**: Sector is underperforming, may lag behind
- **Higher absolute value**: Stronger signal

### Market Trend
- **Bullish**: >60% sectors positive, avg 20-day return >2%
- **Bearish**: <40% sectors positive, avg 20-day return <-2%
- **Neutral**: Everything in between

### Performance Metrics
- **1D Return**: Today's performance
- **5D Return**: Weekly trend
- **20D Return**: Monthly momentum
- **60D Return**: Quarterly outlook

## Technical Details

### Data Source
- Yahoo Finance API via yfinance library
- Real-time ETF pricing data
- Historical OHLCV data

### Machine Learning
- Weighted scoring algorithm
- Multi-factor analysis
- Momentum-based predictions
- Risk-adjusted returns

### Tech Stack
- **Backend**: Python, Flask
- **Data Processing**: pandas, numpy
- **ML**: scikit-learn
- **Market Data**: yfinance
- **Frontend**: HTML, CSS, JavaScript
- **API**: RESTful architecture

## Troubleshooting

### "Module not found" error
Run: `pip install -r requirements.txt`

### "Connection refused" error
Make sure the Flask server is running on port 5000

### Data fetch errors
Check your internet connection and try again

### API not responding
Ensure no other service is using port 5000

## Customization

### Change Analysis Period
Edit the default period in `frontend/index.html` or use API query params

### Add More Sectors
Add sector ETF tickers to `utils/sector_data.py`

### Adjust AI Weights
Modify scoring weights in `models/sector_predictor.py`

### Change Port
Edit port in `api/app.py` (default: 5000)

## Disclaimer

⚠️ **Important**: This application is for educational and informational purposes only. 

- Not financial advice
- Past performance doesn't guarantee future results
- Always do your own research
- Consult with financial professionals before investing
- Markets are unpredictable and AI predictions can be wrong

## License

MIT License - Free to use and modify

## Support

For issues or questions, please check:
- API documentation at http://localhost:5000
- Console logs for error messages
- Requirements.txt for dependency versions

---

**Built with ❤️ for stock market enthusiasts**
