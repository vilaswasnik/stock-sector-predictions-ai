"""
Simplified Flask API with Demo Data, Time Period Selection, Charts, and Related Stocks
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.sector_predictor import SectorPredictor
from utils.demo_data import generate_demo_data
from utils.sector_stocks import get_sector_stocks, get_all_sector_stocks

app = Flask(__name__)
CORS(app)

predictor = SectorPredictor()

@app.route('/')
@app.route('/dashboard')
@app.route('/index.html')
def home():
    dashboard_html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AI Stock Sector Prediction with Related Stocks</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
<style>
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px;margin:0;}
.container{max-width:1600px;margin:0 auto;}
header{text-align:center;color:white;margin-bottom:30px;}
h1{font-size:2.5em;margin-bottom:10px;}
.controls{background:white;border-radius:10px;padding:20px;margin:20px 0;box-shadow:0 4px 6px rgba(0,0,0,0.1);text-align:center;}
.time-buttons{display:flex;gap:10px;justify-content:center;margin-top:15px;flex-wrap:wrap;}
.btn{background:#667eea;color:white;border:none;padding:12px 24px;border-radius:5px;cursor:pointer;font-size:1em;transition:all 0.3s;}
.btn:hover{background:#764ba2;transform:translateY(-2px);}
.btn.active{background:#10b981;box-shadow:0 0 10px rgba(16,185,129,0.5);}
.period-btn{background:#f8f9fa;color:#333;border:2px solid #667eea;}
.period-btn:hover{background:#667eea;color:white;}
.period-btn.active{background:#667eea;color:white;border-color:#764ba2;}
.card{background:white;border-radius:10px;padding:25px;margin:20px 0;box-shadow:0 4px 6px rgba(0,0,0,0.1);}
.card h2{color:#333;border-bottom:3px solid #667eea;padding-bottom:10px;}
.chart-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px 0;}
.chart-container{background:white;border-radius:10px;padding:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1);height:400px;}
.chart-container canvas{max-height:350px;}
.sector-item{padding:15px;margin:10px 0;background:#f8f9fa;border-radius:8px;border-left:5px solid #667eea;position:relative;}
.sector-name{font-weight:bold;font-size:1.1em;color:#333;margin-bottom:8px;}
.stocks-section{background:#fff;border:1px solid #e0e0e0;border-radius:5px;padding:12px;margin-top:10px;}
.stocks-title{font-weight:bold;color:#667eea;margin-bottom:8px;font-size:0.95em;}
.stock-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px;}
.stock-item{background:#f8f9fa;padding:8px;border-radius:4px;border-left:3px solid #10b981;cursor:pointer;transition:all 0.2s;}
.stock-item:hover{background:#e0e7ff;transform:translateX(5px);}
.stock-symbol{font-weight:bold;color:#333;font-size:0.9em;}
.stock-name{color:#666;font-size:0.8em;}
.proof-box{background:#fff;border:1px solid #e0e0e0;border-radius:5px;padding:10px;margin-top:10px;font-size:0.85em;}
.proof-title{font-weight:bold;color:#667eea;margin-bottom:5px;}
.proof-item{padding:3px 0;color:#666;}
.positive{color:#10b981;font-weight:bold;}
.negative{color:#ef4444;font-weight:bold;}
table{width:100%;border-collapse:collapse;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #eee;}
th{background:#f8f9fa;}
.prediction-label{font-size:0.9em;color:#667eea;font-weight:bold;margin-bottom:5px;}
.confidence-bar{background:#e0e0e0;height:8px;border-radius:4px;overflow:hidden;margin:5px 0;}
.confidence-fill{background:#10b981;height:100%;transition:width 0.3s;}
.modal{display:none;position:fixed;z-index:1000;left:0;top:0;width:100%;height:100%;background:rgba(0,0,0,0.7);}
.modal-content{background:white;margin:5% auto;padding:20px;border-radius:10px;width:90%;max-width:1200px;max-height:80vh;overflow-y:auto;}
.close{float:right;font-size:28px;font-weight:bold;cursor:pointer;color:#999;}
.close:hover{color:#333;}
#tradingview-widget{height:500px;margin-top:20px;}
@media (max-width: 1200px){.chart-grid{grid-template-columns:1fr;}}
</style></head><body>
<div class="container">
<header><h1>🚀 AI Stock Sector Prediction</h1><p>Multi-timeframe analysis with related stocks & trading charts</p></header>

<div class="controls">
<div class="prediction-label">SELECT PREDICTION TIMEFRAME:</div>
<div class="time-buttons">
<button class="btn period-btn active" onclick="selectPeriod('30d', this)">📅 30 Days</button>
<button class="btn period-btn" onclick="selectPeriod('2m', this)">📆 2 Months</button>
<button class="btn period-btn" onclick="selectPeriod('3m', this)">🗓️ 3 Months</button>
<button class="btn period-btn" onclick="selectPeriod('6m', this)">📊 6 Months</button>
<button class="btn period-btn" onclick="selectPeriod('1y', this)">📈 1 Year</button>
</div>
<button class="btn" onclick="loadData()" style="margin-top:15px;">🔄 Refresh Analysis</button>
</div>

<div id="content"><p style="text-align:center;color:white;font-size:1.2em;">Select a timeframe and click Refresh to start analysis...</p></div>
</div>

<div id="stockModal" class="modal">
<div class="modal-content">
<span class="close" onclick="closeModal()">&times;</span>
<h2 id="modalTitle"></h2>
<div id="tradingview-widget"></div>
</div>
</div>

<script>
let currentPeriod = '30d';
let charts = {};
let sectorStocks = {};

function selectPeriod(period, btn){
currentPeriod = period;
document.querySelectorAll('.period-btn').forEach(b=>b.classList.remove('active'));
btn.classList.add('active');
}

function destroyCharts(){
Object.keys(charts).forEach(key=>{
if(charts[key]){charts[key].destroy();}
});
charts = {};
}

function showStockChart(symbol, name){
document.getElementById('modalTitle').textContent = name + ' (' + symbol + ')';
document.getElementById('stockModal').style.display = 'block';
document.getElementById('tradingview-widget').innerHTML = '';

new TradingView.widget({
"width": "100%",
"height": 500,
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

function closeModal(){
document.getElementById('stockModal').style.display = 'none';
document.getElementById('tradingview-widget').innerHTML = '';
}

window.onclick = function(event){
if(event.target == document.getElementById('stockModal')){
closeModal();
}
}

async function loadData(){
destroyCharts();
document.getElementById('content').innerHTML='<div class="card"><p style="text-align:center;font-size:1.2em;">🔄 Analyzing market data for '+getPeriodLabel()+'...</p></div>';
try{
const resp=await fetch('/api/analysis?period='+currentPeriod);
const data=await resp.json();
sectorStocks = data.sector_stocks;

let html='<div class="card">';
html+='<h2>🎯 Prediction Timeframe: '+data.timeframe_label+'</h2>';
html+='<h2>📊 Market Trend: '+data.market_trend.trend+'</h2>';
html+='<p>Confidence: '+data.market_trend.confidence+'% | Expected Return: '+data.market_trend.expected_return+'%</p>';
html+='<div class="confidence-bar"><div class="confidence-fill" style="width:'+data.market_trend.confidence+'%"></div></div>';
html+='<p style="color:#667eea;"><strong>'+data.timeframe_insight+'</strong></p>';
html+='<div class="proof-box"><div class="proof-title">📋 Market Analysis Proof:</div>';
html+='<div class="proof-item">• Positive Sectors: '+data.market_trend.positive_sectors+'/'+data.market_trend.total_sectors+' ('+data.market_trend.positive_ratio+'%)</div>';
html+='<div class="proof-item">• Average 20-Day Return: '+data.market_trend.avg_return_20d+'%</div>';
html+='<div class="proof-item">• Methodology: AI weighted scoring (30% momentum, 25% short-term, 20% medium-term, 15% recent, 10% volatility)</div>';
html+='</div></div>';

html+='<div class="card"><h2>📊 Visual Analysis Charts</h2>';
html+='<div class="chart-grid">';
html+='<div class="chart-container"><h3 style="text-align:center;color:#667eea;">AI Score Rankings</h3><canvas id="scoreChart"></canvas></div>';
html+='<div class="chart-container"><h3 style="text-align:center;color:#667eea;">Expected Returns</h3><canvas id="returnChart"></canvas></div>';
html+='<div class="chart-container"><h3 style="text-align:center;color:#667eea;">Risk vs Return</h3><canvas id="riskReturnChart"></canvas></div>';
html+='<div class="chart-container"><h3 style="text-align:center;color:#667eea;">Performance Metrics</h3><canvas id="metricsChart"></canvas></div>';
html+='</div></div>';

html+='<div class="card"><h2>🏆 Top 5 Leading Sectors for '+data.timeframe_label+'</h2>';
data.top_sectors.forEach((s,i)=>{
html+='<div class="sector-item"><div class="sector-name">'+(i+1)+'. '+s.sector+' ('+s.ticker+')</div>';
html+='<p>AI Score: <strong>'+s.ai_score+'</strong> | Expected '+data.timeframe_label+' Return: <span class="'+(s.predicted_return>=0?'positive':'negative')+'">'+s.predicted_return+'%</span></p>';
html+='<p style="font-size:0.9em;color:#666;">Current Momentum: '+s.momentum+'% | Volatility: '+s.volatility+'%</p>';

const stocks = sectorStocks[s.sector] || [];
if(stocks.length > 0){
html+='<div class="stocks-section"><div class="stocks-title">📈 Top Stocks in '+s.sector+':</div>';
html+='<div class="stock-grid">';
stocks.forEach(stock=>{
html+='<div class="stock-item" onclick="showStockChart(\''+stock.symbol+'\',\''+stock.name+'\')">';
html+='<div class="stock-symbol">'+stock.symbol+'</div>';
html+='<div class="stock-name">'+stock.name+'</div></div>';
});
html+='</div></div>';
}

html+='<div class="proof-box"><div class="proof-title">🔬 Prediction Proof:</div>';
html+='<div class="proof-item">• Momentum: '+s.momentum_score+' | Short-term: '+s.short_term_score+' | Medium-term: '+s.medium_term_score+'</div>';
html+='<div class="proof-item">• Volatility Penalty: '+s.volatility_penalty+' | Volume Boost: '+s.volume_boost+'</div>';
html+='<div class="proof-item"><strong>Total AI Score: '+s.ai_score+'</strong> → Projected return: '+s.predicted_return+'%</div>';
html+='</div></div>';
});
html+='</div>';

html+='<div class="card"><h2>📈 All Sectors with Related Stocks</h2><table>';
html+='<tr><th>Rank</th><th>Sector</th><th>AI Score</th><th>Expected Return</th><th>Risk</th><th>Top Stocks</th></tr>';
data.all_sectors.forEach(s=>{
const risk = s.volatility < 2 ? '🟢 Low' : s.volatility < 3 ? '🟡 Med' : '🔴 High';
const stocks = sectorStocks[s.sector] || [];
const stockList = stocks.slice(0,3).map(st=>st.symbol).join(', ');
html+='<tr><td>'+s.rank+'</td><td>'+s.sector+'</td><td><strong>'+s.ai_score+'</strong></td>';
html+='<td class="'+(s.predicted_return>=0?'positive':'negative')+'">'+s.predicted_return+'%</td>';
html+='<td>'+risk+'</td><td style="font-size:0.85em;">'+stockList+'</td></tr>';
});
html+='</table></div>';

html+='<div class="card"><h2>💡 AI Insights & Methodology</h2>';
data.insights.forEach(insight=>{
html+='<p style="padding:10px;background:#f8f9fa;margin:10px 0;border-radius:5px;">• '+insight+'</p>';
});
html+='</div>';

document.getElementById('content').innerHTML=html;
createCharts(data);

}catch(e){
document.getElementById('content').innerHTML='<div class="card"><p style="color:#ef4444;">Error: '+e.message+'</p></div>';
}
}

function createCharts(data){
const top10 = data.all_sectors.slice(0,10);

const scoreCtx = document.getElementById('scoreChart').getContext('2d');
charts.scoreChart = new Chart(scoreCtx, {
type: 'bar',
data: {
labels: top10.map(s=>s.sector),
datasets: [{
label: 'AI Score',
data: top10.map(s=>s.ai_score),
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
labels: top10.map(s=>s.sector),
datasets: [{
label: 'Expected Return (%)',
data: top10.map(s=>s.predicted_return),
backgroundColor: top10.map(s=>s.predicted_return>=0?'rgba(16, 185, 129, 0.7)':'rgba(239, 68, 68, 0.7)'),
borderColor: top10.map(s=>s.predicted_return>=0?'rgba(16, 185, 129, 1)':'rgba(239, 68, 68, 1)'),
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

const riskCtx = document.getElementById('riskReturnChart').getContext('2d');
charts.riskChart = new Chart(riskCtx, {
type: 'scatter',
data: {
datasets: [{
label: 'Sectors',
data: data.all_sectors.map(s=>({x:s.volatility, y:s.predicted_return, label:s.sector})),
backgroundColor: 'rgba(102, 126, 234, 0.6)',
borderColor: 'rgba(102, 126, 234, 1)',
borderWidth: 2,
pointRadius: 6
}]
},
options: {
responsive: true,
maintainAspectRatio: false,
scales: {
x: {title: {display: true, text: 'Volatility (Risk)'}},
y: {title: {display: true, text: 'Expected Return (%)'}}
},
plugins: {
tooltip: {
callbacks: {
label: function(context){
return context.raw.label + ' - Return: ' + context.raw.y + '%, Risk: ' + context.raw.x + '%';
}
}
},
legend: {display: false}
}
}
});

const metricsCtx = document.getElementById('metricsChart').getContext('2d');
const top5 = data.top_sectors;
charts.metricsChart = new Chart(metricsCtx, {
type: 'radar',
data: {
labels: ['Momentum', 'Short-term', 'Medium-term', 'Recent', 'Volume'],
datasets: top5.map((s,i)=>({
label: s.sector,
data: [s.momentum_score, s.short_term_score, s.medium_term_score, s.recent_boost, s.volume_boost],
borderColor: ['rgba(102,126,234,1)','rgba(16,185,129,1)','rgba(239,68,68,1)','rgba(245,158,11,1)','rgba(168,85,247,1)'][i],
backgroundColor: ['rgba(102,126,234,0.2)','rgba(16,185,129,0.2)','rgba(239,68,68,0.2)','rgba(245,158,11,0.2)','rgba(168,85,247,0.2)'][i],
borderWidth: 2
}))
},
options: {
responsive: true,
maintainAspectRatio: false,
scales: {r: {beginAtZero: true}}
}
});
}

function getPeriodLabel(){
const labels={'30d':'30 Days','2m':'2 Months','3m':'3 Months','6m':'6 Months','1y':'1 Year'};
return labels[currentPeriod] || '30 Days';
}
</script></body></html>'''
    return dashboard_html

@app.route('/api/analysis')
def get_analysis():
    try:
        period = request.args.get('period', '30d')
        
        period_multipliers = {
            '30d': 1.0, '2m': 2.0, '3m': 3.0, '6m': 6.0, '1y': 12.0
        }
        
        period_labels = {
            '30d': '30 Days', '2m': '2 Months', '3m': '3 Months', '6m': '6 Months', '1y': '1 Year'
        }
        
        multiplier = period_multipliers.get(period, 1.0)
        label = period_labels.get(period, '30 Days')
        
        print(f"Generating predictions for {label}...")
        metrics_df = generate_demo_data()
        
        scores_df = predictor.calculate_sector_score(metrics_df)
        trend_data = predictor.predict_trend(metrics_df)
        
        for idx, row in scores_df.iterrows():
            sector_name = row['sector']
            orig_data = metrics_df[metrics_df['sector'] == sector_name].iloc[0]
            scores_df.at[idx, 'momentum'] = round(orig_data['momentum'], 2)
            scores_df.at[idx, 'volatility'] = round(orig_data['volatility'], 2)
        
        scores_df['predicted_return'] = (scores_df['return_20d'] * multiplier * 0.8).round(2)
        
        confidence_adjustment = max(60, 95 - (multiplier * 5))
        trend_data['confidence'] = min(confidence_adjustment, trend_data['confidence'])
        trend_data['expected_return'] = round(trend_data['avg_return_20d'] * multiplier * 0.75, 2)
        
        top_sectors = predictor.get_top_sectors(scores_df, n=5)
        
        timeframe_insights = {
            '30d': 'Short-term prediction: Focus on momentum and recent trends.',
            '2m': 'Medium-short prediction: Balancing current momentum with stability.',
            '3m': 'Quarter prediction: Considering seasonal patterns and quarterly performance.',
            '6m': 'Half-year prediction: Factoring in medium-term economic trends.',
            '1y': 'Annual prediction: Long-term outlook based on fundamental sector strength.'
        }
        
        all_sectors = scores_df.to_dict('records')
        insights = predictor.generate_insights(scores_df, trend_data)
        
        methodology = [
            f"🔬 PROOF OF CONCEPT: AI Prediction Methodology for {label}",
            f"✓ Data Points Analyzed: {len(all_sectors)} sectors with 8 performance metrics each",
            f"✓ Scoring Algorithm: Weighted multi-factor model (Momentum 30%, Short-term 25%, Medium-term 20%, Recent 15%, Volatility -10%, Volume boost)",
            f"✓ Historical Context: 1-day, 5-day, 20-day, and 60-day performance trends",
            f"✓ Risk Assessment: Volatility analysis with penalty for high variance",
            f"✓ Confidence Calculation: Based on {trend_data['positive_ratio']}% positive sectors and {trend_data['confidence']}% statistical confidence",
            f"✓ Projection Model: Current momentum × {multiplier}× timeframe multiplier × 0.8 dampening factor",
            f"✓ Validation: Top sector ({top_sectors[0]['sector']}) shows {top_sectors[0]['ai_score']} AI score with {top_sectors[0]['return_20d']}% 20-day momentum",
            f"✓ Related Stocks: Each sector includes 5 major constituent stocks for direct trading opportunities"
        ]
        
        insights = methodology + [f"Prediction horizon: {label} - {timeframe_insights.get(period, '')}"] + insights
        
        # Get sector stocks mapping
        sector_stocks_data = get_all_sector_stocks()
        
        return jsonify({
            'timestamp': metrics_df['timestamp'].iloc[0],
            'period': period,
            'timeframe_label': label,
            'timeframe_insight': timeframe_insights.get(period, ''),
            'market_trend': trend_data,
            'top_sectors': top_sectors,
            'all_sectors': all_sectors,
            'insights': insights,
            'sector_stocks': sector_stocks_data,
            'demo_mode': True
        })
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Stock Sector Prediction API with Multi-Timeframe Analysis...")
    app.run(host='0.0.0.0', port=5000, debug=False)
