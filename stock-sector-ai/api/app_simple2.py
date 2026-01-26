from flask import Flask, jsonify, request
from flask_cors import CORS
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.sector_predictor import SectorPredictor
from utils.demo_data import generate_demo_data
from utils.sector_stocks import get_all_sector_stocks

app = Flask(__name__)
CORS(app)
predictor = SectorPredictor()

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<title>AI Stock Sector Prediction</title>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px;margin:0;color:#fff;}
.container{max-width:1400px;margin:0 auto;}
.controls{background:#fff;border-radius:10px;padding:20px;margin:20px 0;box-shadow:0 4px 8px rgba(0,0,0,0.2);text-align:center;}
.btn{background:#667eea;color:#fff;border:none;padding:12px 24px;border-radius:5px;cursor:pointer;font-size:1em;margin:5px;}
.btn:hover{background:#764ba2;}
.btn.active{background:#10b981;}
.card{background:#fff;color:#333;border-radius:10px;padding:20px;margin:20px 0;box-shadow:0 4px 8px rgba(0,0,0,0.2);}
.sector-box{background:#f8f9fa;padding:15px;margin:10px 0;border-radius:8px;border-left:5px solid #667eea;}
.positive{color:#10b981;font-weight:bold;}
.negative{color:#ef4444;font-weight:bold;}
table{width:100%;border-collapse:collapse;margin-top:15px;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd;}
th{background:#f0f0f0;font-weight:bold;}
tr:hover{background:#f5f5f5;}
.stock-btn{background:#10b981;color:#fff;border:none;padding:6px 12px;margin:2px;border-radius:4px;cursor:pointer;font-size:0.85em;}
.stock-btn:hover{background:#059669;}
.bar-container{background:#e0e0e0;height:25px;border-radius:5px;margin:5px 0;position:relative;}
.bar{height:100%;border-radius:5px;transition:width 0.5s;}
.bar-label{position:absolute;right:10px;top:3px;font-size:12px;color:#333;}
.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.8);}
.modal-content{background:#fff;margin:3% auto;padding:20px;border-radius:10px;width:90%;max-width:1200px;max-height:85vh;overflow-y:auto;}
.close{float:right;font-size:32px;font-weight:bold;cursor:pointer;color:#999;}
.close:hover{color:#333;}
#tradingview-widget{height:600px;margin-top:10px;}
</style>
</head><body>
<div class="container">
<h1 style="text-align:center;">🚀 AI Stock Sector Prediction</h1>
<div class="controls">
<h3 style="color:#333;">Select Timeframe:</h3>
<button class="btn period-btn active" onclick="selectPeriod('30d',this)">📅 30 Days</button>
<button class="btn period-btn" onclick="selectPeriod('2m',this)">📆 2 Months</button>
<button class="btn period-btn" onclick="selectPeriod('3m',this)">🗓️ 3 Months</button>
<button class="btn period-btn" onclick="selectPeriod('6m',this)">📊 6 Months</button>
<button class="btn period-btn" onclick="selectPeriod('1y',this)">📈 1 Year</button>
<br><button class="btn" onclick="loadData()" style="margin-top:15px;">🔄 Refresh Analysis</button>
</div>
<div id="content"><div class="card"><p style="text-align:center;">⏳ Loading...</p></div></div>
</div>

<div id="stockModal" class="modal">
<div class="modal-content">
<span class="close" onclick="closeModal()">&times;</span>
<h2 id="modalTitle" style="color:#333;"></h2>
<div id="tradingview-widget"></div>
</div>
</div>

<script src="https://s3.tradingview.com/tv.js"></script>
<script>
var currentPeriod = "30d";

function selectPeriod(period, btn) {
    currentPeriod = period;
    var btns = document.querySelectorAll(".period-btn");
    for(var i=0; i<btns.length; i++) btns[i].classList.remove("active");
    btn.classList.add("active");
    loadData();
}

function showChart(symbol, name) {
    document.getElementById("modalTitle").textContent = name + " (" + symbol + ") - Live Chart";
    document.getElementById("stockModal").style.display = "block";
    document.getElementById("tradingview-widget").innerHTML = "";
    new TradingView.widget({
        "width": "100%", "height": 600, "symbol": symbol, "interval": "D",
        "timezone": "Etc/UTC", "theme": "light", "style": "1", "locale": "en",
        "toolbar_bg": "#f1f3f6", "enable_publishing": false, "allow_symbol_change": true,
        "container_id": "tradingview-widget"
    });
}

function closeModal() {
    document.getElementById("stockModal").style.display = "none";
    document.getElementById("tradingview-widget").innerHTML = "";
}

function loadData() {
    document.getElementById("content").innerHTML = "<div class='card'><h2>⏳ Loading data...</h2></div>";
    
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/analysis?period=" + currentPeriod + "&t=" + Date.now(), true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                try {
                    var data = JSON.parse(xhr.responseText);
                    renderData(data);
                } catch(e) {
                    document.getElementById("content").innerHTML = "<div class='card'><h2>❌ Error parsing data</h2><p>" + e.message + "</p></div>";
                }
            } else {
                document.getElementById("content").innerHTML = "<div class='card'><h2>❌ Error loading data</h2><p>Status: " + xhr.status + "</p></div>";
            }
        }
    };
    xhr.send();
}

function renderData(data) {
    var maxScore = Math.max.apply(null, data.all_sectors.map(function(s){return s.ai_score;}));
    
    var html = "<div class='card'>";
    html += "<h2>🎯 " + data.timeframe_label + " Market Analysis</h2>";
    html += "<h3>📊 Market Trend: " + data.market_trend.trend + "</h3>";
    html += "<p><strong>Confidence:</strong> " + data.market_trend.confidence + "% | ";
    html += "<strong>Expected Return:</strong> " + data.market_trend.expected_return + "%</p>";
    html += "</div>";
    
    html += "<div class='card'>";
    html += "<h2>📊 AI Score Visual Rankings (Top 10)</h2>";
    var top10 = data.all_sectors.slice(0, 10);
    for(var i=0; i<top10.length; i++) {
        var s = top10[i];
        var width = (s.ai_score / maxScore * 100).toFixed(1);
        var color = s.predicted_return >= 0 ? "#10b981" : "#ef4444";
        html += "<p style='margin:5px 0;font-weight:bold;'>" + s.rank + ". " + s.sector + "</p>";
        html += "<div class='bar-container'><div class='bar' style='width:" + width + "%;background:" + color + ";'></div>";
        html += "<span class='bar-label'>Score: " + s.ai_score + " | Return: " + s.predicted_return + "%</span></div>";
    }
    html += "</div>";
    
    html += "<div class='card'>";
    html += "<h2>🏆 Top 5 Sectors with Trade Charts</h2>";
    for(var i=0; i<data.top_sectors.length; i++) {
        var s = data.top_sectors[i];
        var returnClass = s.predicted_return >= 0 ? "positive" : "negative";
        html += "<div class='sector-box'>";
        html += "<h3>" + (i+1) + ". " + s.sector + " (" + s.ticker + ")</h3>";
        html += "<p><strong>AI Score:</strong> " + s.ai_score + " | <strong>Expected Return:</strong> <span class='" + returnClass + "'>" + s.predicted_return + "%</span></p>";
        html += "<p style='font-size:0.9em;color:#666;'>Momentum: " + s.momentum + "% | Volatility: " + s.volatility + "%</p>";
        if(s.stocks && s.stocks.length > 0) {
            html += "<p><strong>Trade These Stocks:</strong></p>";
            for(var j=0; j<s.stocks.length; j++) {
                var stock = s.stocks[j];
                html += "<button class='stock-btn' onclick='showChart(\"" + stock.symbol + "\",\"" + stock.name.replace(/'/g, '') + "\")'>📈 " + stock.symbol + "</button>";
            }
        }
        html += "</div>";
    }
    html += "</div>";
    
    html += "<div class='card'>";
    html += "<h2>📋 All 16 Sectors Ranking</h2>";
    html += "<table><thead><tr><th>Rank</th><th>Sector</th><th>Ticker</th><th>AI Score</th><th>Return</th><th>Momentum</th></tr></thead><tbody>";
    for(var i=0; i<data.all_sectors.length; i++) {
        var s = data.all_sectors[i];
        var returnClass = s.predicted_return >= 0 ? "positive" : "negative";
        html += "<tr><td>" + s.rank + "</td><td>" + s.sector + "</td><td>" + s.ticker + "</td>";
        html += "<td>" + s.ai_score + "</td><td class='" + returnClass + "'>" + s.predicted_return + "%</td><td>" + s.momentum + "%</td></tr>";
    }
    html += "</tbody></table></div>";
    
    document.getElementById("content").innerHTML = html;
}

// Auto-load when page loads
window.onload = loadData;
</script>
</body></html>'''

@app.route('/api/analysis')
def get_analysis():
    period = request.args.get('period', '30d')
    period_map = {'7d': 7, '30d': 30, '2m': 60, '3m': 90, '6m': 180, '1y': 365}
    days = period_map.get(period, 30)
    
    label_map = {'7d': '7-Day', '30d': '30-Day', '2m': '2-Month', '3m': '3-Month', '6m': '6-Month', '1y': '1-Year'}
    timeframe_label = label_map.get(period, '30-Day')
    
    data = generate_demo_data(num_days=max(days, 60))
    sector_stocks = get_all_sector_stocks()
    all_results = []
    
    for sector, df in data.items():
        score_data = predictor.calculate_sector_score(df)
        stock_list = sector_stocks.get(sector, [])[:6]
        all_results.append({
            'sector': sector,
            'ticker': score_data['ticker'],
            'ai_score': score_data['ai_score'],
            'predicted_return': score_data['predicted_return'],
            'momentum': score_data['momentum'],
            'volatility': score_data['volatility'],
            'return_1d': score_data['return_1d'],
            'return_5d': score_data['return_5d'],
            'return_20d': score_data['return_20d'],
            'return_60d': score_data['return_60d'],
            'volume_ratio': score_data['volume_ratio'],
            'short_term_score': score_data['short_term_score'],
            'medium_term_score': score_data['medium_term_score'],
            'momentum_score': score_data['momentum_score'],
            'volatility_penalty': score_data['volatility_penalty'],
            'volume_boost': score_data['volume_boost'],
            'recent_boost': score_data['recent_boost'],
            'stocks': stock_list
        })
    
    all_results.sort(key=lambda x: x['ai_score'], reverse=True)
    for i, r in enumerate(all_results): r['rank'] = i + 1
    top_sectors = all_results[:5]
    avg_return = sum(r['predicted_return'] for r in all_results) / len(all_results)
    
    return jsonify({
        'timeframe_label': timeframe_label,
        'top_sectors': top_sectors,
        'all_sectors': all_results,
        'market_trend': {
            'trend': 'Bullish' if avg_return > 2 else ('Bearish' if avg_return < -2 else 'Neutral'),
            'confidence': min(85, max(50, 65 + avg_return * 2)),
            'expected_return': round(avg_return, 2)
        }
    })

if __name__ == '__main__':
    print('Starting simple server on port 5000...')
    app.run(host='0.0.0.0', port=5000)
