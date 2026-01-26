"""
News Sentiment Analyzer - Fetches and analyzes market news sentiment
"""
import requests
import os
from datetime import datetime, timedelta
from textblob import TextBlob  # For sentiment analysis

class NewsSentimentAnalyzer:
    def __init__(self):
        # API keys from environment
        self.newsapi_key = os.getenv('NEWSAPI_KEY', None)
        self.alphavantage_key = os.getenv('ALPHAVANTAGE_API_KEY', None)
        
    def fetch_sector_news(self, sector_name, ticker, days=7):
        """Fetch news articles for a specific sector/ticker"""
        if not self.newsapi_key:
            return self.get_sample_news(sector_name)
        
        try:
            # NewsAPI endpoint
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': f'{sector_name} OR {ticker}',
                'from': (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en',
                'apiKey': self.newsapi_key,
                'pageSize': 10
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == 'ok':
                return data.get('articles', [])
            else:
                print(f"NewsAPI error for {sector_name}: {data.get('message', 'Unknown error')}")
                return self.get_sample_news(sector_name)
                
        except Exception as e:
            print(f"Error fetching news for {sector_name}: {str(e)}")
            return self.get_sample_news(sector_name)
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using TextBlob"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1 (negative to positive)
            
            if polarity > 0.1:
                return 'positive', polarity
            elif polarity < -0.1:
                return 'negative', polarity
            else:
                return 'neutral', polarity
        except:
            return 'neutral', 0.0
    
    def get_sector_sentiment_score(self, sector_name, ticker):
        """Get overall sentiment score for a sector"""
        articles = self.fetch_sector_news(sector_name, ticker)
        
        if not articles:
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_articles': 0,
                'headlines': []
            }
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        headlines = []
        
        for article in articles[:10]:  # Analyze top 10 articles
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title}. {description}"
            
            sentiment, score = self.analyze_sentiment(text)
            sentiments.append(score)
            
            if sentiment == 'positive':
                positive_count += 1
            elif sentiment == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
            
            headlines.append({
                'title': title,
                'sentiment': sentiment,
                'score': round(score, 2),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', 'Unknown'),
                'published': article.get('publishedAt', '')
            })
        
        # Calculate average sentiment
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0
        
        if avg_sentiment > 0.1:
            overall_sentiment = 'positive'
        elif avg_sentiment < -0.1:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        return {
            'sentiment': overall_sentiment,
            'score': round(avg_sentiment, 2),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_articles': len(articles),
            'headlines': headlines[:5]  # Return top 5 headlines
        }
    
    def get_sample_news(self, sector_name):
        """Return sample news when API is unavailable"""
        sample_news = {
            'Technology': [
                {'title': 'Tech stocks rally on AI optimism', 'description': 'Major technology companies see gains.'},
                {'title': 'Cloud computing growth accelerates', 'description': 'Sector shows strong momentum.'}
            ],
            'Healthcare': [
                {'title': 'Healthcare sector shows resilience', 'description': 'Biotech companies report positive results.'},
                {'title': 'Medical innovation drives growth', 'description': 'New treatments boost sector outlook.'}
            ],
            'Energy': [
                {'title': 'Oil prices fluctuate on supply concerns', 'description': 'Energy sector remains volatile.'},
                {'title': 'Renewable energy investments surge', 'description': 'Clean energy sees increased funding.'}
            ]
        }
        
        articles = sample_news.get(sector_name, [
            {'title': f'{sector_name} sector update', 'description': 'Market conditions remain stable.'}
        ])
        
        return [
            {
                'title': article['title'],
                'description': article['description'],
                'url': '#',
                'source': {'name': 'Demo News'},
                'publishedAt': datetime.now().isoformat()
            }
            for article in articles
        ]
    
    def enhance_predictions_with_sentiment(self, predictions_df):
        """Add sentiment scores to prediction data"""
        for idx, row in predictions_df.iterrows():
            sector_name = row['sector']
            ticker = row['ticker']
            
            sentiment_data = self.get_sector_sentiment_score(sector_name, ticker)
            
            # Add sentiment score to prediction
            predictions_df.at[idx, 'news_sentiment'] = sentiment_data['score']
            predictions_df.at[idx, 'sentiment_label'] = sentiment_data['sentiment']
            predictions_df.at[idx, 'positive_news'] = sentiment_data['positive_count']
            predictions_df.at[idx, 'negative_news'] = sentiment_data['negative_count']
        
        return predictions_df
