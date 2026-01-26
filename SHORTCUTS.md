# ⌨️ Shortcuts & Commands Cheat Sheet

**Quick reference for Stock Sector Predictions AI**

---

## 🎯 Most Used Commands

```bash
# START APP
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && source venv/bin/activate && cd api && python app.py

# STOP APP
Ctrl+C  # or: pkill -f "python app.py"

# OPEN DASHBOARD
$BROWSER http://localhost:8000/dashboard

# CHECK STATUS
curl http://localhost:8000/api/status
```

---

## 🔗 Quick URLs

| What | URL |
|------|-----|
| Dashboard | http://localhost:8000/dashboard |
| API Status | http://localhost:8000/api/status |
| Full Analysis | http://localhost:8000/api/analysis |
| Predictions | http://localhost:8000/api/predict |
| Sectors List | http://localhost:8000/api/sectors |

---

## 💻 Terminal Commands

### Application Control
```bash
# Start
source venv/bin/activate && python api/app.py

# Stop
Ctrl+C

# Restart
pkill -f "python app.py" && source venv/bin/activate && python api/app.py

# Check if running
ps aux | grep "python app.py"

# Kill process
lsof -ti :8000 | xargs kill -9
```

### API Testing
```bash
# Status check
curl http://localhost:8000/api/status

# Get analysis (pretty print)
curl -s http://localhost:8000/api/analysis | jq

# Get predictions only
curl -s http://localhost:8000/api/predict | jq '.predictions'

# Watch updates every 5 seconds
watch -n 5 'curl -s http://localhost:8000/api/analysis | jq ".predictions.market_trend"'

# Get specific sector
curl -s http://localhost:8000/api/sectors | jq '.[] | select(.symbol=="XLK")'
```

### Configuration
```bash
# View API keys
cat .env

# Edit configuration
nano .env  # or: code .env

# Check Python packages
pip list

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## 🌐 Browser Shortcuts

| Key | Action |
|-----|--------|
| `F5` | Refresh page |
| `Ctrl+R` | Reload page |
| `Ctrl+Shift+R` | Hard reload (clear cache) |
| `Ctrl+Shift+I` | Open Developer Tools |
| `Ctrl+Shift+J` | Open Console |
| `Ctrl+Shift+Delete` | Clear browsing data |

---

## 🐛 Debug Shortcuts

```bash
# Check logs
tail -f app.log  # if logging to file

# Test port availability
nc -zv localhost 8000

# Check what's using port 8000
lsof -i :8000

# View environment variables
env | grep API

# Test Alpha Vantage API
curl "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=YOUR_KEY"

# Test NewsAPI
curl "https://newsapi.org/v2/everything?q=stocks&apiKey=YOUR_KEY"
```

---

## 🔄 Git Shortcuts

```bash
# Quick status
git status -s

# Add all changes
git add .

# Commit
git commit -m "Your message"

# Push
git push origin main

# Pull latest
git pull origin main

# View recent commits
git log --oneline -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- .
```

---

## 📁 File Navigation

```bash
# Main app
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai/api

# Dashboard
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai/frontend

# Models
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai/models

# Utils
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai/utils

# Root
cd /workspaces/stock-sector-predictions-ai
```

---

## ⚙️ Environment Aliases (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Stock App Aliases
alias stockapp='cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && source venv/bin/activate && cd api && python app.py'
alias stockstop='pkill -f "python app.py"'
alias stockcheck='curl http://localhost:8000/api/status'
alias stockdash='$BROWSER http://localhost:8000/dashboard'
alias stocklogs='tail -f /workspaces/stock-sector-predictions-ai/stock-sector-ai/app.log'
alias stockcd='cd /workspaces/stock-sector-predictions-ai/stock-sector-ai'

# After adding, reload:
source ~/.bashrc
```

Usage after setup:
```bash
stockapp      # Start the app
stockstop     # Stop the app
stockcheck    # Check if running
stockdash     # Open dashboard
stockcd       # Go to project directory
```

---

## 🎨 VS Code Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+` ` | Toggle terminal |
| `Ctrl+Shift+E` | Explorer |
| `Ctrl+Shift+F` | Search in files |
| `Ctrl+P` | Quick file open |
| `Ctrl+Shift+P` | Command palette |
| `Ctrl+/` | Toggle comment |
| `Ctrl+S` | Save file |
| `Ctrl+Shift+K` | Delete line |

---

## 📊 Data Shortcuts

### View Current Predictions
```bash
curl -s http://localhost:8000/api/predict | jq '{
  market_trend: .predictions.market_trend,
  confidence: .predictions.confidence,
  leading: .predictions.leading_sectors,
  lagging: .predictions.lagging_sectors
}'
```

### Get Top Sector
```bash
curl -s http://localhost:8000/api/analysis | jq '.analysis | sort_by(-.score) | first | {name, symbol, score, trend}'
```

### Check All Sector Scores
```bash
curl -s http://localhost:8000/api/analysis | jq '.analysis[] | {symbol, score}' | less
```

### Export to File
```bash
# Save analysis to JSON
curl -s http://localhost:8000/api/analysis > analysis_$(date +%Y%m%d_%H%M%S).json

# Save predictions to JSON
curl -s http://localhost:8000/api/predict > predictions_$(date +%Y%m%d_%H%M%S).json
```

---

## 🔐 Security Shortcuts

```bash
# Check .env is in .gitignore
grep ".env" .gitignore

# Verify .env not tracked by git
git status --ignored | grep .env

# Generate new .env.example (without real keys)
cp .env .env.example
sed -i 's/=.*/=your_key_here/g' .env.example
```

---

## 📈 Performance Shortcuts

```bash
# Check memory usage
ps aux | grep "python app.py" | awk '{print $6/1024 " MB"}'

# Monitor CPU usage
top -p $(pgrep -f "python app.py")

# Check disk space
df -h /workspaces/stock-sector-predictions-ai

# Count API calls (if logging)
grep -c "API call" app.log
```

---

## 🆘 Emergency Shortcuts

```bash
# Force kill all Python processes
killall -9 python

# Reset to last commit
git reset --hard HEAD

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Full restart
pkill -f "python app.py" && \
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai && \
source venv/bin/activate && \
cd api && \
python app.py
```

---

## 🎯 Power User Tips

1. **Use tab completion** - Type partial commands and press Tab
2. **Use `!!`** - Repeats last command
3. **Use `!$`** - Last argument of previous command
4. **Use `Ctrl+R`** - Search command history
5. **Use `&`** - Run command in background: `python app.py &`
6. **Use `nohup`** - Keep running after logout: `nohup python app.py &`

---

## 📋 Quick Checklist

```bash
# Daily startup routine
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
source venv/bin/activate
cd api
python app.py
# Open http://localhost:8000/dashboard in browser

# Before committing
git status
git diff
git add .
git commit -m "Your message"
git push origin main

# When API limit reached
# Comment out API keys in .env
# Restart app (uses demo data)
```

---

**Tip**: Print this page or bookmark it for quick reference!

**Last Updated**: January 26, 2026
