"""
Flask API for Stock Sector Prediction
"""
from flask import Flask, jsonify, request, Response, redirect
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Choose data source: use Alpha Vantage if API key is set, otherwise use Yahoo Finance
USE_ALPHAVANTAGE = os.getenv('ALPHAVANTAGE_API_KEY') and os.getenv('ALPHAVANTAGE_API_KEY') != 'your_api_key_here'

if USE_ALPHAVANTAGE:
    from utils.alphavantage_fetcher import AlphaVantageDataFetcher as SectorDataFetcher
    print("Using Alpha Vantage for real market data")
else:
    from utils.sector_data import SectorDataFetcher
    print("Using Yahoo Finance (may fall back to demo data)")

from models.sector_predictor import SectorPredictor
from models.enhanced_predictor import EnhancedSectorPredictor
from utils.demo_data import generate_demo_data
from utils.news_sentiment import NewsSentimentAnalyzer

# Check if NewsAPI is configured
USE_NEWS_SENTIMENT = os.getenv('NEWSAPI_KEY') and os.getenv('NEWSAPI_KEY') != 'your_newsapi_key_here'

if USE_NEWS_SENTIMENT:
    news_analyzer = NewsSentimentAnalyzer()
    predictor = EnhancedSectorPredictor()
    print("News sentiment analysis enabled")
else:
    predictor = SectorPredictor()
    print("Using basic predictor (no news sentiment)")

app = Flask(__name__)
CORS(app)

data_fetcher = SectorDataFetcher()

@app.route('/')
def home():
    # Redirect to dashboard
    return redirect('/dashboard')

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'service': 'Stock Sector Prediction API',
        'version': '1.0.0'
    })

@app.route('/api/sectors', methods=['GET'])
def get_sectors():
    return jsonify({
        'sectors': list(data_fetcher.sectors.keys()),
        'count': len(data_fetcher.sectors)
    })

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    try:
        period = request.args.get('period', '3mo')
        
        print("Fetching sector data...")
        sector_data = data_fetcher.fetch_sector_data(period=period, max_sectors=10)
        
        # Fallback to demo data if fetching fails or not enough data
        if not sector_data or len(sector_data) < 5:
            print(f"Using demo data (only {len(sector_data) if sector_data else 0} sectors fetched)")
            metrics_df = generate_demo_data()
        else:
            metrics_df = data_fetcher.calculate_performance_metrics(sector_data)
        
        # Add news sentiment if enabled
        if USE_NEWS_SENTIMENT:
            print("Analyzing news sentiment...")
            metrics_df = news_analyzer.enhance_predictions_with_sentiment(metrics_df)
        
        print("Running AI predictions...")
        scores_df = predictor.calculate_sector_score(metrics_df)
        trend_data = predictor.predict_trend(metrics_df)
        top_sectors = predictor.get_top_sectors(scores_df, n=3)
        bottom_sectors = predictor.get_bottom_sectors(scores_df, n=3)
        insights = predictor.generate_insights(scores_df, trend_data)
        
        response = {
            'timestamp': metrics_df['timestamp'].iloc[0],
            'market_trend': trend_data,
            'top_sectors': top_sectors,
            'bottom_sectors': bottom_sectors,
            'all_sectors': scores_df.to_dict('records'),
            'insights': insights,
            'period': period,
            'demo_mode': len(sector_data) == 0 if sector_data is not None else True,
            'news_sentiment_enabled': USE_NEWS_SENTIMENT
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict', methods=['GET'])
def predict_leaders():
    try:
        period = request.args.get('period', '3mo')
        sector_data = data_fetcher.fetch_sector_data(period=period)
        
        if not sector_data:
            metrics_df = generate_demo_data()
        else:
            metrics_df = data_fetcher.calculate_performance_metrics(sector_data)
        
        scores_df = predictor.calculate_sector_score(metrics_df)
        predictions = predictor.get_top_sectors(scores_df, n=5)
        
        return jsonify({
            'predictions': predictions,
            'timestamp': metrics_df['timestamp'].iloc[0],
            'message': 'Top 5 sectors predicted to lead the market'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
@app.route('/index.html')
@app.route('/index')
def serve_dashboard():
    """Serve the dashboard HTML"""
    try:
        dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'index.html')
        with open(dashboard_path, 'r') as f:
            html_content = f.read()
            # Update API URL to use same origin
            html_content = html_content.replace("const API_URL = 'http://192.168.244.138:5000';", "const API_URL = window.location.origin;")
            html_content = html_content.replace("const API_URL = 'http://localhost:5000';", "const API_URL = window.location.origin;")
            return Response(html_content, mimetype='text/html')
    except Exception as e:
        return f"Error loading dashboard: {str(e)}", 500

@app.route('/test')
def test_page():
    """Simple test page"""
    return '''
<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <h1>Page Loaded Successfully!</h1>
    <p>If you can see this, the server is working.</p>
    <button onclick="testAPI()">Test API Call</button>
    <div id="result"></div>
    <script>
        async function testAPI() {
            document.getElementById('result').innerHTML = 'Testing API...';
            try {
                const response = await fetch(window.location.origin + '/api/analysis');
                const data = await response.json();
                document.getElementById('result').innerHTML = 'API Response: ' + JSON.stringify(data.market_trend);
            } catch (error) {
                document.getElementById('result').innerHTML = 'API Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/debug')
def serve_debug():
    """Serve debug page"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Debug Page</title>
</head>
<body>
    <h1>Debug Page</h1>
    <div id="api_url"></div>
    <div id="location_origin"></div>
    <button onclick="testAPI()">Test API</button>
    <div id="result"></div>

    <script>
        // Show what API_URL is set to
        document.getElementById('api_url').innerHTML = 'API_URL: ' + (typeof API_URL !== 'undefined' ? API_URL : 'NOT SET');
        document.getElementById('location_origin').innerHTML = 'window.location.origin: ' + window.location.origin;

        async function testAPI() {
            const result = document.getElementById('result');
            result.innerHTML = 'Testing...';

            try {
                const response = await fetch(window.location.origin + '/api/analysis');
                const data = await response.json();
                result.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (error) {
                result.innerHTML = 'Error: ' + error.message;
            }
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    print("Starting Stock Sector Prediction API...")
    print("API will be available at http://0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)
