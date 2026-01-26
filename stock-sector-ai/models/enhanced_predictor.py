"""
Enhanced Sector Predictor with News Sentiment Integration
"""
import pandas as pd
import numpy as np
from datetime import datetime

class EnhancedSectorPredictor:
    def __init__(self):
        # Weights for different factors
        self.weights = {
            'return_60d': 0.25,
            'momentum': 0.20,
            'volatility': -0.15,  # Lower volatility is better
            'volume_ratio': 0.10,
            'return_20d': 0.15,
            'news_sentiment': 0.15  # News sentiment weight
        }
    
    def calculate_sector_score(self, metrics_df):
        """Calculate composite score with news sentiment"""
        scores_df = metrics_df.copy()
        
        # Normalize metrics to 0-100 scale
        for column in ['return_60d', 'return_20d', 'momentum', 'volume_ratio']:
            if column in scores_df.columns:
                min_val = scores_df[column].min()
                max_val = scores_df[column].max()
                if max_val > min_val:
                    scores_df[f'{column}_norm'] = 100 * (scores_df[column] - min_val) / (max_val - min_val)
                else:
                    scores_df[f'{column}_norm'] = 50
        
        # Normalize volatility (inverse - lower is better)
        if 'volatility' in scores_df.columns:
            min_vol = scores_df['volatility'].min()
            max_vol = scores_df['volatility'].max()
            if max_vol > min_vol:
                scores_df['volatility_norm'] = 100 * (max_vol - scores_df['volatility']) / (max_vol - min_vol)
            else:
                scores_df['volatility_norm'] = 50
        
        # Normalize sentiment score (-1 to 1 → 0 to 100)
        if 'news_sentiment' in scores_df.columns:
            scores_df['news_sentiment_norm'] = (scores_df['news_sentiment'] + 1) * 50
        else:
            scores_df['news_sentiment_norm'] = 50  # Neutral if no sentiment data
        
        # Calculate weighted composite score
        scores_df['ai_score'] = (
            scores_df['return_60d_norm'] * self.weights['return_60d'] +
            scores_df['return_20d_norm'] * self.weights['return_20d'] +
            scores_df['momentum_norm'] * self.weights['momentum'] +
            scores_df['volatility_norm'] * abs(self.weights['volatility']) +
            scores_df['volume_ratio_norm'] * self.weights['volume_ratio'] +
            scores_df['news_sentiment_norm'] * self.weights['news_sentiment']
        )
        
        scores_df['ai_score'] = scores_df['ai_score'].round(2)
        scores_df = scores_df.sort_values('ai_score', ascending=False)
        
        return scores_df
    
    def predict_trend(self, metrics_df):
        """Predict overall market trend with sentiment"""
        avg_return = metrics_df['return_60d'].mean()
        avg_sentiment = metrics_df.get('news_sentiment', pd.Series([0])).mean()
        
        # Combine technical and sentiment signals
        combined_signal = (avg_return * 0.7) + (avg_sentiment * 30 * 0.3)
        
        if combined_signal > 5:
            trend = 'bullish'
            confidence = min(95, 50 + combined_signal)
        elif combined_signal < -5:
            trend = 'bearish'
            confidence = min(95, 50 + abs(combined_signal))
        else:
            trend = 'neutral'
            confidence = 50 + abs(combined_signal)
        
        return {
            'trend': trend,
            'confidence': round(confidence, 1),
            'technical_signal': round(avg_return, 2),
            'sentiment_signal': round(avg_sentiment, 2)
        }
    
    def get_top_sectors(self, scores_df, n=3):
        """Get top N sectors to invest in"""
        top = scores_df.nlargest(n, 'ai_score')
        return top[['sector', 'ticker', 'ai_score', 'return_60d', 'sentiment_label']].to_dict('records')
    
    def get_bottom_sectors(self, scores_df, n=3):
        """Get bottom N sectors to avoid"""
        bottom = scores_df.nsmallest(n, 'ai_score')
        return bottom[['sector', 'ticker', 'ai_score', 'return_60d', 'sentiment_label']].to_dict('records')
    
    def generate_insights(self, scores_df, trend_data):
        """Generate AI insights with news sentiment"""
        insights = []
        
        # Market trend insight
        trend = trend_data['trend']
        confidence = trend_data['confidence']
        sentiment = trend_data.get('sentiment_signal', 0)
        
        if sentiment > 0.2:
            insights.append(f"📰 News sentiment is strongly positive ({sentiment:.2f}), supporting {trend} outlook")
        elif sentiment < -0.2:
            insights.append(f"📰 News sentiment is negative ({sentiment:.2f}), adding caution to market outlook")
        
        insights.append(f"🎯 Market trend: {trend.upper()} with {confidence:.1f}% confidence")
        
        # Top sector insights
        top_sector = scores_df.iloc[0]
        sentiment_label = top_sector.get('sentiment_label', 'neutral')
        insights.append(
            f"⭐ {top_sector['sector']} leads with AI score {top_sector['ai_score']:.1f}/100 "
            f"and {sentiment_label} news sentiment"
        )
        
        # Volatility insight with sentiment
        high_vol = scores_df.nlargest(1, 'volatility').iloc[0]
        insights.append(
            f"⚠️ {high_vol['sector']} shows highest volatility ({high_vol['volatility']:.2f}%) - "
            f"monitor news closely"
        )
        
        # Momentum insight
        high_momentum = scores_df.nlargest(1, 'momentum').iloc[0]
        insights.append(
            f"🚀 {high_momentum['sector']} has strongest momentum ({high_momentum['momentum']:.2f}%)"
        )
        
        return insights
