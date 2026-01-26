# ⚡ Quick Start Guide - Stock Sector Predictions AI

**Get up and running in 2 minutes!**

---

## 🚀 One-Command Setup

```bash
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && \
source venv/bin/activate && \
cd api && \
python app.py
```

Then open: **http://localhost:8000/dashboard**

---

## 📋 Essential Commands

### Start the Application
```bash
# Full path (run from anywhere)
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && source venv/bin/activate && cd api && python app.py

# Short version (if already in stock-sector-ai directory)
source venv/bin/activate && cd api && python app.py
```

### Stop the Application
```bash
# Press Ctrl+C in the terminal where the app is running
# Or find and kill the process:
ps aux | grep "python app.py" | grep -v grep | awk '{print $2}' | xargs kill -9
```

### Check if App is Running
```bash
curl http://localhost:8000/api/status
# Should return: {"status": "running"}
```

### View Logs
```bash
# In the terminal where app is running
# Or check the console output
```

---

## 🌐 Quick Access URLs

| Endpoint | URL | Description |
|----------|-----|-------------|
| **Dashboard** | http://localhost:8000/dashboard | Main UI |
| **Home** | http://localhost:8000/ | Redirects to dashboard |
| **Status Check** | http://localhost:8000/api/status | API health check |
| **Sector Analysis** | http://localhost:8000/api/analysis | Get analysis data (JSON) |
| **All Sectors** | http://localhost:8000/api/sectors | List all sectors |
| **Predictions** | http://localhost:8000/api/predict | AI predictions (JSON) |

---

## 🔧 Configuration Shortcuts

### View API Keys
```bash
cat /workspaces/stock-sector-predictions-ai/stock-sector-ai/.env
```

### Edit API Keys
```bash
nano /workspaces/stock-sector-predictions-ai/stock-sector-ai/.env
# Or use VS Code: code .env
```

### Current Configuration:
- **Alpha Vantage API**: `ZGBEI4K9F14A0S4E` (25 calls/day, 5/min)
- **NewsAPI Key**: `9ae580dbe17f4621a1c549114b529b52` (100 calls/day)
- **Server Port**: `8000`
- **Debug Mode**: `Enabled`

---

## 📊 API Testing Shortcuts

### Test Status Endpoint
```bash
curl http://localhost:8000/api/status
```

### Get Full Analysis
```bash
curl http://localhost:8000/api/analysis | jq
```

### Get Predictions Only
```bash
curl http://localhost:8000/api/predict | jq
```

### Get Specific Sector Data
```bash
curl http://localhost:8000/api/sectors | jq '.[] | select(.symbol=="XLK")'
```

---

## 🔑 Keyboard Shortcuts (Dashboard)

| Key | Action |
|-----|--------|
| `F5` | Refresh dashboard |
| `Ctrl + R` | Reload page |
| `Ctrl + Shift + I` | Open DevTools |
| `Ctrl + Shift + J` | Open Console |

---

## 📱 Common Tasks

### 1. Quick Restart
```bash
# Kill existing process
pkill -f "python app.py"

# Start fresh
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && \
source venv/bin/activate && \
cd api && \
python app.py
```

### 2. View Real-Time Data
```bash
# Open dashboard in browser
$BROWSER http://localhost:8000/dashboard

# Or use curl to watch updates every 5 seconds
watch -n 5 'curl -s http://localhost:8000/api/analysis | jq ".predictions"'
```

### 3. Check API Quota
```bash
# Check logs for rate limit messages
grep -i "rate limit\|quota" /path/to/logs

# Manual check: Count API calls
# Alpha Vantage: 25/day limit
# NewsAPI: 100/day limit
```

### 4. Switch to Demo Mode (No API Calls)
```bash
# Edit .env file
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
nano .env

# Comment out API keys:
# ALPHAVANTAGE_API_KEY=your_key
# NEWSAPI_KEY=your_key

# Restart app - will use demo data
```

### 5. Update Dependencies
```bash
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## 🐛 Troubleshooting Shortcuts

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
lsof -ti :8000 | xargs kill -9

# Or use different port
PORT=8080 python app.py
```

### Module Not Found Error
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues
```bash
# Verify .env file exists
ls -la /workspaces/stock-sector-predictions-ai/stock-sector-ai/.env

# Check API key format
cat .env | grep API_KEY

# Test API keys
curl "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=ZGBEI4K9F14A0S4E"
```

### Dashboard Not Loading
```bash
# Check if server is running
ps aux | grep "python app.py"

# Check server logs
# Look for errors in terminal output

# Test API directly
curl http://localhost:8000/api/status

# Clear browser cache
# Press Ctrl+Shift+Delete in browser
```

---

## 📁 Quick Navigation

### Project Structure
```
stock-sector-ai/
├── api/
│   └── app.py          # Main Flask application
├── models/
│   ├── sector_predictor.py      # Original AI model
│   └── enhanced_predictor.py    # With news sentiment
├── utils/
│   ├── sector_data.py           # Yahoo Finance data
│   ├── alphavantage_fetcher.py  # Alpha Vantage API
│   ├── news_sentiment.py        # NewsAPI integration
│   └── demo_data.py             # Fallback demo data
├── frontend/
│   └── index.html               # Dashboard UI
├── .env                         # API keys (not in git)
├── requirements.txt             # Python dependencies
└── venv/                        # Virtual environment
```

### Quick File Access
```bash
# Edit main app
code /workspaces/stock-sector-predictions-ai/stock-sector-ai/api/app.py

# Edit dashboard
code /workspaces/stock-sector-predictions-ai/stock-sector-ai/frontend/index.html

# Edit AI model
code /workspaces/stock-sector-predictions-ai/stock-sector-ai/models/enhanced_predictor.py

# View logs
tail -f /path/to/app.log  # If logging to file
```

---

## 🔄 Git Shortcuts

### Quick Status
```bash
cd /workspaces/stock-sector-predictions-ai
git status -s
```

### Quick Commit & Push
```bash
git add .
git commit -m "Update: your message here"
git push origin main
```

### View Recent Changes
```bash
git log --oneline -5
git diff HEAD~1
```

---

## 💡 Pro Tips

1. **Keep Multiple Terminals Open**
   - Terminal 1: Run the app
   - Terminal 2: Test API calls
   - Terminal 3: Edit files

2. **Use Aliases** (Add to ~/.bashrc)
   ```bash
   alias startapp='cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && source venv/bin/activate && cd api && python app.py'
   alias stopapp='pkill -f "python app.py"'
   alias checkapp='curl http://localhost:8000/api/status'
   ```

3. **Monitor API Limits**
   - Alpha Vantage: Resets daily (25 calls)
   - NewsAPI: Resets daily (100 calls)
   - Use demo mode during development

4. **Bookmark Dashboard**
   - Save http://localhost:8000/dashboard
   - Check regularly for market updates

5. **Use jq for JSON Parsing**
   ```bash
   curl http://localhost:8000/api/analysis | jq '.predictions.leading_sectors'
   ```

---

## 📞 Need Help?

- **Documentation**: See SETUP_GUIDE.md for detailed setup
- **News Feature**: See NEWS_SENTIMENT_GUIDE.md for sentiment analysis
- **Issues**: Check GitHub Issues or create new one
- **API Docs**: Visit Alpha Vantage and NewsAPI documentation

---

## ✅ Quick Validation Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] .env file configured with API keys
- [ ] Port 8000 available
- [ ] Server running without errors
- [ ] Dashboard loads at http://localhost:8000
- [ ] API returns data (check /api/status)
- [ ] No rate limit errors in logs

---

**Last Updated**: January 26, 2026  
**App Version**: 1.0 with Alpha Vantage + NewsAPI  
**Python**: 3.12.8 | **Flask**: 3.0.0 | **Port**: 8000
