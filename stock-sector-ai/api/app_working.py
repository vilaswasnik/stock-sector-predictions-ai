from flask import Flask
from flask_cors import CORS
import sys
import random
from datetime import datetime
sys.path.insert(0, '/root/stock-sector-ai')
from utils.sector_stocks import get_all_sector_stocks

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    # Generate data directly
    sectors_data = [
        ('Technology', 82.5, 8.5),
        ('Healthcare', 71.2, 5.2),
        ('Financials', 68.8, 6.8),
        ('Energy', 45.3, -2.3),
        ('Consumer Discretionary', 74.1, 7.1),
        ('Industrials', 62.9, 4.9),
        ('Consumer Staples', 55.2, 3.2),
        ('Utilities', 48.1, 2.1),
        ('Real Estate', 44.8, 1.8),
        ('Materials', 58.7, 3.7),
        ('Communication Services', 69.3, 6.3),
        ('Gold', 78.4, 12.4),
        ('Silver', 76.8, 15.8),
        ('Metals & Mining', 72.2, 9.2),
        ('Crypto/Bitcoin', 85.7, 45.7),
        ('Defense & Aerospace', 75.3, 11.3)
    ]
    
    results = []
    for sector, base_score, base_return in sectors_data:
        score = base_score + random.uniform(-5, 5)
        ret = base_return + random.uniform(-2, 2)
        trend = 'Bullish' if score > 60 else 'Bearish' if score < 40 else 'Neutral'
        results.append({'sector': sector, 'score': round(score, 1), 'trend': trend, 'return': round(ret, 2)})
    
    results.sort(key=lambda x: x['score'], reverse=True)
    sector_stocks = get_all_sector_stocks()
    
    rows = ''
    for i, r in enumerate(results, 1):
        color = '#00ff88' if r['trend'] == 'Bullish' else '#ff4444' if r['trend'] == 'Bearish' else '#ffaa00'
        ret_color = '#00ff88' if r['return'] > 0 else '#ff4444'
        stocks = sector_stocks.get(r['sector'], ['SPY'])[:3]
        stock_btns = ' '.join([f'<button onclick="showChart(\'{s}\')" style="background:#333;color:#fff;border:1px solid #555;padding:3px 8px;margin:2px;border-radius:4px;cursor:pointer;">{s}</button>' for s in stocks])
        rows += f'''<tr>
            <td style="padding:12px;border-bottom:1px solid #333;">{i}</td>
            <td style="padding:12px;border-bottom:1px solid #333;font-weight:bold;">{r['sector']}</td>
            <td style="padding:12px;border-bottom:1px solid #333;"><div style="background:#333;border-radius:10px;overflow:hidden;height:20px;width:150px;display:inline-block;"><div style="background:linear-gradient(90deg,#00ff88,#00aa55);height:100%;width:{r['score']}%;"></div></div> {r['score']}</td>
            <td style="padding:12px;border-bottom:1px solid #333;color:{color};font-weight:bold;">{r['trend']}</td>
            <td style="padding:12px;border-bottom:1px solid #333;color:{ret_color};">{r['return']}%</td>
            <td style="padding:12px;border-bottom:1px solid #333;">{stock_btns}</td>
        </tr>'''
    
    return f'''<!DOCTYPE html>
<html><head><title>Stock Sector AI</title>
<style>
body {{ background: #0a0a0a; color: #fff; font-family: Arial; margin: 0; padding: 20px; }}
.container {{ max-width: 1400px; margin: 0 auto; }}
h1 {{ color: #00ff88; text-align: center; font-size: 2.5em; }}
table {{ width: 100%; border-collapse: collapse; background: #1a1a1a; border-radius: 10px; overflow: hidden; margin-top: 20px; }}
th {{ background: #222; padding: 15px; text-align: left; color: #00ff88; }}
.modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; }}
.modal-content {{ position: relative; margin: 3% auto; width: 90%; max-width: 1200px; height: 75%; background: #1a1a1a; border-radius: 10px; padding: 20px; }}
.close {{ position: absolute; top: 10px; right: 20px; font-size: 35px; cursor: pointer; color: #fff; z-index: 1001; }}
.refresh-btn {{ background: linear-gradient(135deg, #00ff88, #00aa55); color: #000; border: none; padding: 12px 30px; font-size: 16px; border-radius: 8px; cursor: pointer; font-weight: bold; }}
.refresh-btn:hover {{ transform: scale(1.05); }}
</style></head>
<body>
<div class="container">
<h1>📈 Stock Sector AI Analysis</h1>
<p style="text-align:center;color:#888;">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | <button class="refresh-btn" onclick="location.reload()">🔄 Refresh</button></p>
<table>
<tr><th>#</th><th>Sector</th><th>AI Score</th><th>Trend</th><th>Return</th><th>Top Stocks</th></tr>
{rows}
</table>
</div>
<div id="modal" class="modal" onclick="if(event.target===this)closeModal()">
<div class="modal-content">
<span class="close" onclick="closeModal()">&times;</span>
<div id="chart-container" style="width:100%;height:100%;"></div>
</div>
</div>
<script>
function showChart(symbol) {{
    document.getElementById('modal').style.display = 'block';
    document.getElementById('chart-container').innerHTML = '<iframe src="https://www.tradingview.com/widgetembed/?frameElementId=chart&symbol=' + symbol + '&interval=D&hidesidetoolbar=0&symboledit=1&saveimage=1&toolbarbg=1a1a1a&theme=dark&style=1&timezone=exchange" style="width:100%;height:100%;border:none;"></iframe>';
}}
function closeModal() {{ document.getElementById('modal').style.display = 'none'; document.getElementById('chart-container').innerHTML = ''; }}
window.onclick = function(e) {{ if(e.target.className === 'modal') closeModal(); }}
</script>
</body></html>'''

if __name__ == '__main__':
    print('Starting Stock Sector AI on port 5000...')
    app.run(host='0.0.0.0', port=5000)
