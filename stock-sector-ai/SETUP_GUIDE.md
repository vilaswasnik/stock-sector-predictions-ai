# Stock Sector Predictions AI - Setup Guide

## 🚀 Getting Real Market Data

Currently, the app uses demo/simulated data. To get **real market data**, follow these steps:

### Option 1: Alpha Vantage (Recommended - FREE)

1. **Get Free API Key:**
   - Visit: https://www.alphavantage.co/support/#api-key
   - Enter your email
   - Get instant API key (no credit card required)
   - **Free tier:** 25 requests/day, 5 requests/minute

2. **Configure the App:**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your key
   nano .env
   # Add: ALPHAVANTAGE_API_KEY=your_actual_api_key_here
   ```

3. **Update app.py to use Alpha Vantage:**
   ```python
   # In api/app.py, replace this line:
   from utils.sector_data import SectorDataFetcher
   
   # With:
   from utils.alphavantage_fetcher import AlphaVantageDataFetcher as SectorDataFetcher
   ```

4. **Install python-dotenv (if not installed):**
   ```bash
   source venv/bin/activate
   pip install python-dotenv
   ```

5. **Restart the server**

### Option 2: Other Free APIs

#### Finnhub (60 calls/minute)
- Sign up: https://finnhub.io/register
- Good for: Real-time data, news, sentiment
- Free tier: 60 API calls/minute

#### Twelve Data (800 calls/day)
- Sign up: https://twelvedata.com/pricing
- Good for: Technical indicators, fundamentals
- Free tier: 800 requests/day

#### Polygon.io (Delayed data)
- Sign up: https://polygon.io/pricing
- Good for: Historical data
- Free tier: 5 API calls/minute, 15-min delayed

#### IEX Cloud (50K messages/month)
- Sign up: https://iexcloud.io/pricing
- Good for: US stocks, ETFs
- Free tier: 50,000 core messages/month

## 🔧 Current Setup

The app is currently running with:
- **Port:** 8000
- **Dashboard:** http://127.0.0.1:8000/
- **API Endpoints:** http://127.0.0.1:8000/api/*
- **Data Source:** Demo/Simulated data

## 📊 What You'll Get With Real Data

- **Real-time prices** from actual market ETFs
- **Accurate performance metrics** (1D, 1W, 1M, 3M returns)
- **Live volatility calculations**
- **Actual volume data**
- **AI predictions** based on real market trends

## ⚠️ Important Notes

1. **Rate Limits:** Free APIs have request limits. The Alpha Vantage integration includes automatic rate limiting (12 seconds between requests).

2. **Data Freshness:** Free tiers usually provide:
   - Alpha Vantage: Daily data (end of day)
   - Finnhub: Real-time during market hours
   - Twelve Data: 1-minute delayed
   - Polygon: 15-minute delayed

3. **Market Hours:** Stock market data is only updated during trading hours (9:30 AM - 4:00 PM EST, Monday-Friday).

4. **Demo Mode Fallback:** If API requests fail, the app automatically falls back to demo data.

## 🎯 Quick Start (Alpha Vantage)

```bash
# 1. Get API key from https://www.alphavantage.co/support/#api-key

# 2. Set environment variable
export ALPHAVANTAGE_API_KEY=your_key_here

# 3. Update app.py (line 11):
# Change: from utils.sector_data import SectorDataFetcher
# To: from utils.alphavantage_fetcher import AlphaVantageDataFetcher as SectorDataFetcher

# 4. Restart server
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
source venv/bin/activate
cd api
python app.py
```

## 📈 Performance Optimization

For better performance with free APIs:
- **Cache data:** Store API responses to minimize requests
- **Reduce sectors:** Focus on top 5-10 sectors instead of all 16
- **Longer refresh intervals:** Update every 15-30 minutes instead of real-time
- **Use multiple APIs:** Rotate between different free APIs

## 🆘 Troubleshooting

**Problem:** "API key invalid" error
- **Solution:** Double-check your API key in .env file

**Problem:** Rate limit exceeded
- **Solution:** Wait a few minutes, or reduce number of sectors

**Problem:** No data returned
- **Solution:** Check if symbol is valid, try during market hours

**Problem:** Still seeing demo data
- **Solution:** Make sure .env file is in the correct location and app is restarted
