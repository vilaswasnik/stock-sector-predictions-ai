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
.stock-list{font-size:0.85em;color:#666;}
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
<div id="content"><div class="card"><p style="text-align:center;">Click "Refresh Analysis" to start...</p></div></div>
</div>

<script>
console.log('Script loaded');
let currentPeriod = '30d';

function selectPeriod(period, btn) {
    currentPeriod = period;
    document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}

async function loadData() {
    document.getElementById('content').innerHTML = '<div class="card"><h2>⏳ Loading data for ' + currentPeriod + '...</h2></div>';
    
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
        html += '<h2>🏆 Top 5 Leading Sectors</h2>';
        data.top_sectors.forEach((s, i) => {
            const returnClass = s.predicted_return >= 0 ? 'positive' : 'negative';
            html += '<div class="sector-box">';
            html += '<h3>' + (i+1) + '. ' + s.sector + ' (' + s.ticker + ')</h3>';
            html += '<p><strong>AI Score:</strong> ' + s.ai_score + ' | ';
            html += '<strong>Expected Return:</strong> <span class="' + returnClass + '">' + s.predicted_return + '%</span></p>';
            html += '<p style="font-size:0.9em;color:#666;">Momentum: ' + s.momentum + '% | Volatility: ' + s.volatility + '%</p>';
            
            const stocks = data.sector_stocks[s.sector] || [];
            if (stocks.length > 0) {
                html += '<p class="stock-list">📈 Key Stocks: ' + stocks.map(st => st.symbol).join(', ') + '</p>';
            }
            html += '</div>';
        });
        html += '</div>';
        
        html += '<div class="card">';
        html += '<h2>📊 All ' + data.all_sectors.length + ' Sectors Ranked</h2>';
        html += '<table>';
        html += '<tr><th>Rank</th><th>Sector</th><th>Ticker</th><th>AI Score</th><th>Expected Return</th><th>Risk</th><th>Top Stocks</th></tr>';
        
        data.all_sectors.forEach(s => {
            const returnClass = s.predicted_return >= 0 ? 'positive' : 'negative';
            const risk = s.volatility < 2 ? '🟢 Low' : s.volatility < 3 ? '🟡 Med' : '🔴 High';
            const stocks = data.sector_stocks[s.sector] || [];
            const stockList = stocks.slice(0, 3).map(st => st.symbol).join(', ');
            
            html += '<tr>';
            html += '<td><strong>' + s.rank + '</strong></td>';
            html += '<td>' + s.sector + '</td>';
            html += '<td>' + s.ticker + '</td>';
            html += '<td><strong>' + s.ai_score + '</strong></td>';
            html += '<td class="' + returnClass + '">' + s.predicted_return + '%</td>';
            html += '<td>' + risk + '</td>';
            html += '<td class="stock-list">' + stockList + '</td>';
            html += '</tr>';
        });
        
        html += '</table></div>';
        
        document.getElementById('content').innerHTML = html;
        console.log('Display complete - showing', data.all_sectors.length, 'sectors');
        
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('content').innerHTML = '<div class="card"><h2 style="color:red;">Error: ' + error.message + '</h2></div>';
    }
}
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
    print("Starting full server with all 16 sectors on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)
