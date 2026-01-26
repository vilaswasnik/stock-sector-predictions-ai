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
<title>AI Stock Sector Prediction with Charts</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://s3.tradingview.com/tv.js"></script>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);padding:20px;margin:0;color:#fff;}
.container{max-width:1600px;margin:0 auto;}
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
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0;}
.chart-box{background:#fff;border-radius:10px;padding:20px;box-shadow:0 4px 8px rgba(0,0,0,0.2);height:400px;}
.chart-box canvas{max-height:350px;}
.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.8);}
.modal-content{background:#fff;margin:3% auto;padding:20px;border-radius:10px;width:90%;max-width:1200px;max-height:85vh;overflow-y:auto;}
.close{float:right;font-size:32px;font-weight:bold;cursor:pointer;color:#999;}
.close:hover{color:#333;}
#tradingview-widget{height:600px;margin-top:10px;}
</style>
</head><body>
<div class="container">
<h1 style="text-align:center;">🚀 AI Stock Sector Prediction with Trade Charts</h1>
<div class="controls">
<h3 style="color:#333;">Select Timeframe:</h3>
<button class="btn period-btn active" onclick="selectPeriod('30d',this)">📅 30 Days</button>
<button class="btn period-btn" onclick="selectPeriod('2m',this)">📆 2 Months</button>
<button class="btn period-btn" onclick="selectPeriod('3m',this)">🗓️ 3 Months</button>
<button class="btn period-btn" onclick="selectPeriod('6m',this)">📊 6 Months</button>
<button class="btn period-btn" onclick="selectPeriod('1y',this)">📈 1 Year</button>
<br><button class="btn" onclick="loadData()" style="margin-top:15px;">🔄 Refresh Analysis</button>
</div>
<div id="content"><div class="card"><p style="text-align:center;">⏳ Loading analysis data...</p></div></div>
</div>

<div id="stockModal" class="modal">
<div class="modal-content">
<span class="close" onclick="closeModal()">&times;</span>
<h2 id="modalTitle" style="color:#333;"></h2>
<div id="tradingview-widget"></div>
</div>
</div>

<script>
let currentPeriod = '30d';
let charts = {};

function selectPeriod(period, btn) {
    currentPeriod = period;
    document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

function showChart(symbol, name) {
    document.getElementById('modalTitle').textContent = name + ' (' + symbol + ') - Live Trading Chart';
    document.getElementById('stockModal').style.display = 'block';
    document.getElementById('tradingview-widget').innerHTML = '';
    
    new TradingView.widget({
        "width": "100%",
        "height": 600,
        "symbol": symbol,
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview-widget"
    });
}

function closeModal() {
    document.getElementById('stockModal').style.display = 'none';
    document.getElementById('tradingview-widget').innerHTML = '';
}

window.onclick = function(event) {
    if (event.target == document.getElementById('stockModal')) {
        closeModal();
    }
}

function destroyCharts() {
    Object.keys(charts).forEach(key => {
        if (charts[key]) charts[key].destroy();
    });
    charts = {};
}

async function loadData() {
    destroyCharts();
    document.getElementById('content').innerHTML = '<div class="card"><h2>⏳ Loading data...</h2></div>';
    
    try {
        const url = '/api/analysis?period=' + currentPeriod + '&t=' + Date.now();
        const response = await fetch(url);
        const data = await response.json();
        
        let html = '<div class="card">';
        html += '<h2>🎯 ' + data.timeframe_label + ' Market Analysis</h2>';
        html += '<h3>📊 Market Trend: ' + data.market_trend.trend + '</h3>';
        html += '<p><strong>Confidence:</strong> ' + data.market_trend.confidence + '% | ';
        html += '<strong>Expected Return:</strong> ' + data.market_trend.expected_return + '%</p>';
        html += '</div>';
        
        html += '<div class="card">';
        html += '<h2>📊 Visual Analysis Charts</h2>';
        html += '<div class="chart-grid">';
        html += '<div class="chart-box"><h3 style="text-align:center;color:#667eea;">AI Score Rankings</h3><canvas id="scoreChart"></canvas></div>';
        html += '<div class="chart-box"><h3 style="text-align:center;color:#667eea;">Expected Returns</h3><canvas id="returnChart"></canvas></div>';
        html += '</div></div>';
        
        html += '<div class="card">';
        html += '<h2>🏆 Top 5 Leading Sectors with Trade Charts</h2>';
        data.top_sectors.forEach((s, i) => {
            const returnClass = s.predicted_return >= 0 ? 'positive' : 'negative';
            html += '<div class="sector-box">';
            html += '<h3>' + (i+1) + '. ' + s.sector + ' (' + s.ticker + ')</h3>';
            html += '<p><strong>AI Score:</strong> ' + s.ai_score + ' | ';
            html += '<strong>Expected Return:</strong> <span class="' + returnClass + '">' + s.predicted_return + '%</span></p>';
            html += '<p style="font-size:0.9em;color:#666;">Momentum: ' + s.momentum + '% | Volatility: ' + s.volatility + '%</p>';
            
            const stocks = data.sector_stocks[s.sector] || [];
            if (stocks.length > 0) {
                html += '<p><strong>📈 Click to view live trade charts:</strong></p>';
                stocks.forEach(st => {
                    html += '<button class="stock-btn" onclick="showChart(\'' + st.symbol + '\',\'' + st.name + '\')">' + st.symbol + ' - ' + st.name + '</button>';
                });
            }
            html += '</div>';
        });
        html += '</div>';
        
        html += '<div class="card">';
        html += '<h2>📊 All ' + data.all_sectors.length + ' Sectors Ranked</h2>';
        html += '<table>';
        html += '<tr><th>Rank</th><th>Sector</th><th>Ticker</th><th>AI Score</th><th>Expected Return</th><th>Risk</th><th>View Charts</th></tr>';
        
        data.all_sectors.forEach(s => {
            const returnClass = s.predicted_return >= 0 ? 'positive' : 'negative';
            const risk = s.volatility < 2 ? '🟢 Low' : s.volatility < 3 ? '🟡 Med' : '🔴 High';
            const stocks = data.sector_stocks[s.sector] || [];
            
            html += '<tr>';
            html += '<td><strong>' + s.rank + '</strong></td>';
            html += '<td>' + s.sector + '</td>';
            html += '<td>' + s.ticker + '</td>';
            html += '<td><strong>' + s.ai_score + '</strong></td>';
            html += '<td class="' + returnClass + '">' + s.predicted_return + '%</td>';
            html += '<td>' + risk + '</td>';
            html += '<td>';
            stocks.slice(0, 2).forEach(st => {
                html += '<button class="stock-btn" onclick="showChart(\'' + st.symbol + '\',\'' + st.name + '\')">' + st.symbol + '</button> ';
            });
            html += '</td>';
            html += '</tr>';
        });
        
        html += '</table></div>';
        
        document.getElementById('content').innerHTML = html;
        
        createCharts(data);
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('content').innerHTML = '<div class="card"><h2 style="color:red;">Error: ' + error.message + '</h2></div>';
    }
}

function createCharts(data) {
    const top10 = data.all_sectors.slice(0, 10);
    
    const scoreCtx = document.getElementById('scoreChart').getContext('2d');
    charts.scoreChart = new Chart(scoreCtx, {
        type: 'bar',
        data: {
            labels: top10.map(s => s.sector),
            datasets: [{
                label: 'AI Score',
                data: top10.map(s => s.ai_score),
                backgroundColor: 'rgba(102, 126, 234, 0.7)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {x: {beginAtZero: true}},
            plugins: {legend: {display: false}}
        }
    });
    
    const returnCtx = document.getElementById('returnChart').getContext('2d');
    charts.returnChart = new Chart(returnCtx, {
        type: 'bar',
        data: {
            labels: top10.map(s => s.sector),
            datasets: [{
                label: 'Expected Return (%)',
                data: top10.map(s => s.predicted_return),
                backgroundColor: top10.map(s => s.predicted_return >= 0 ? 'rgba(16, 185, 129, 0.7)' : 'rgba(239, 68, 68, 0.7)'),
                borderColor: top10.map(s => s.predicted_return >= 0 ? 'rgba(16, 185, 129, 1)' : 'rgba(239, 68, 68, 1)'),
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {y: {beginAtZero: true}},
            plugins: {legend: {display: false}}
        }
    });
}

// Auto-load data when page loads
window.onload = loadData;
</script>
</body></html>'''

@app.route('/api/analysis')
def get_analysis():
    period = request.args.get('period', '30d')
    multipliers = {'30d': 1.0, '2m': 2.0, '3m': 3.0, '6m': 6.0, '1y': 12.0}
    labels = {'30d': '30 Days', '2m': '2 Months', '3m': '3 Months', '6m': '6 Months', '1y': '1 Year'}
    
    multiplier = multipliers.get(period, 1.0)
    label = labels.get(period, '30 Days')
    
    metrics_df = generate_demo_data()
    scores_df = predictor.calculate_sector_score(metrics_df)
    trend_data = predictor.predict_trend(metrics_df)
    
    for idx, row in scores_df.iterrows():
        sector_name = row['sector']
        orig_data = metrics_df[metrics_df['sector'] == sector_name].iloc[0]
        scores_df.at[idx, 'momentum'] = round(orig_data['momentum'], 2)
        scores_df.at[idx, 'volatility'] = round(orig_data['volatility'], 2)
    
    scores_df['predicted_return'] = (scores_df['return_20d'] * multiplier * 0.8).round(2)
    
    top_sectors = predictor.get_top_sectors(scores_df, n=5)
    all_sectors = scores_df.to_dict('records')
    sector_stocks = get_all_sector_stocks()
    
    return jsonify({
        'timeframe_label': label,
        'market_trend': trend_data,
        'top_sectors': top_sectors,
        'all_sectors': all_sectors,
        'sector_stocks': sector_stocks
    })

if __name__ == '__main__':
    print("Starting server with trade charts on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
