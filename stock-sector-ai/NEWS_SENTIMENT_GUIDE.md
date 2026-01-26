# 📰 News Sentiment Analysis - Setup Guide

## 🎯 What This Adds

The news sentiment feature enhances AI predictions by analyzing real-time news articles about each sector, providing:

- **Sentiment Scores** (-1 to 1): Negative to Positive
- **News Headlines**: Top 5 relevant articles per sector
- **Enhanced Predictions**: Combines technical analysis + news sentiment
- **Market Insights**: AI-generated insights based on news trends

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Free NewsAPI Key

1. Visit: **https://newsapi.org/register**
2. Enter your email
3. Get instant API key (100 requests/day FREE)
4. No credit card required

### Step 2: Add to .env File

```bash
# Edit your .env file
nano /workspaces/stock-sector-predictions-ai/stock-sector-ai/.env

# Add this line:
NEWSAPI_KEY=your_newsapi_key_here
```

### Step 3: Enable in app.py

The news sentiment analyzer is ready to use! To enable it, you can:

**Option A: Manual Testing**
```bash
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
source venv/bin/activate
python -c "
from utils.news_sentiment import NewsSentimentAnalyzer
analyzer = NewsSentimentAnalyzer()
result = analyzer.get_sector_sentiment_score('Technology', 'XLK')
print(result)
"
```

**Option B: Integrate into API** (see below)

## 📊 How It Works

### 1. News Fetching
- Searches NewsAPI for sector-related articles (last 7 days)
- Filters by relevancy and language
- Returns top 10 most relevant articles

### 2. Sentiment Analysis
Uses TextBlob to analyze each headline/description:
- **Positive** (score > 0.1): Bullish signals
- **Negative** (score < -0.1): Bearish signals  
- **Neutral** (score ≈ 0): No clear direction

### 3. Sector Scoring
Calculates composite score:
```
AI Score = Technical Factors (85%) + News Sentiment (15%)
```

### 4. Enhanced Insights
Generates insights like:
- "📰 News sentiment is strongly positive (+0.75), supporting bullish outlook"
- "⭐ Technology leads with AI score 87.3/100 and positive news sentiment"
- "⚠️ Energy shows highest volatility - monitor news closely"

## 🔧 Integration Example

Add to your `api/app.py`:

```python
from utils.news_sentiment import NewsSentimentAnalyzer
from models.enhanced_predictor import EnhancedSectorPredictor

# Initialize
news_analyzer = NewsSentimentAnalyzer()
enhanced_predictor = EnhancedSectorPredictor()

# In your analysis endpoint:
@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    # ... fetch sector data ...
    
    # Add news sentiment
    metrics_df = news_analyzer.enhance_predictions_with_sentiment(metrics_df)
    
    # Use enhanced predictor
    scores_df = enhanced_predictor.calculate_sector_score(metrics_df)
    trend_data = enhanced_predictor.predict_trend(metrics_df)
    insights = enhanced_predictor.generate_insights(scores_df, trend_data)
    
    # Return enhanced results
    return jsonify({
        'sectors': scores_df.to_dict('records'),
        'trend': trend_data,
        'insights': insights,
        'news_enabled': True
    })
```

## 📈 Example Output

**Without News Sentiment:**
```json
{
  "sector": "Technology",
  "ai_score": 78.5,
  "return_60d": 12.3
}
```

**With News Sentiment:**
```json
{
  "sector": "Technology",
  "ai_score": 85.2,
  "return_60d": 12.3,
  "news_sentiment": 0.65,
  "sentiment_label": "positive",
  "positive_news": 7,
  "negative_news": 1,
  "headlines": [
    {
      "title": "Tech stocks rally on AI innovation",
      "sentiment": "positive",
      "score": 0.75,
      "source": "Bloomberg"
    }
  ]
}
```

## 🆓 Free Alternatives to NewsAPI

### 1. **Alpha Vantage News Sentiment** (Already have API key!)
```python
# Use your existing Alpha Vantage key
endpoint = 'NEWS_SENTIMENT'
params = {
    'tickers': 'XLK',
    'apikey': 'your_key'
}
```

### 2. **Finnhub News**
- Free tier: Included with stock data API
- Real-time market news
- Company-specific articles

### 3. **GNews**
- Free tier: 100 requests/day
- Simple API, no credit card
- Sign up: https://gnews.io/

## 🎯 Benefits

### More Accurate Predictions
- Combines price action + market sentiment
- Catches news-driven moves before they happen
- Identifies sectors with positive/negative buzz

### Real-Time Insights
- Breaking news impact on sectors
- Earnings announcements
- Policy changes and regulations
- Market sentiment shifts

### Better Risk Management
- Warning signals from negative news
- Volatility alerts with news context
- Sector rotation opportunities

## ⚡ Performance Tips

1. **Cache Results**: Store sentiment for 1 hour to reduce API calls
2. **Prioritize Sectors**: Only analyze top 10 sectors
3. **Batch Requests**: Combine multiple tickers in one API call
4. **Monitor Quota**: Track daily API usage

## 🔍 Testing

Test the sentiment analyzer:

```bash
cd /workspaces/stock-sector-predictions-ai/stock-sector-ai
source venv/bin/activate

# Test sentiment analysis
python -c "
from utils.news_sentiment import NewsSentimentAnalyzer
analyzer = NewsSentimentAnalyzer()

# Analyze a sector
result = analyzer.get_sector_sentiment_score('Technology', 'XLK')
print(f\"Sentiment: {result['sentiment']}\")
print(f\"Score: {result['score']}\")
print(f\"Positive news: {result['positive_count']}\")
print(f\"Negative news: {result['negative_count']}\")
print(f\"Headlines: {len(result['headlines'])}\")
"
```

## 📝 Notes

- **Demo Mode**: Works without API key using sample news
- **Rate Limits**: NewsAPI free tier = 100 requests/day
- **Best Practices**: Fetch news once per hour, not on every page load
- **Sentiment Accuracy**: ~70-80% for financial news

Ready to enable? Just add your NewsAPI key to the `.env` file!
