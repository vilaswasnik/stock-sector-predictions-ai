"""
AI-Powered Sector Prediction Model
Uses machine learning to predict leading sectors based on multiple indicators
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from datetime import datetime

class SectorPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        
    def calculate_sector_score(self, metrics_df):
        """
        Calculate AI-powered sector scores based on multiple factors
        Higher score = more likely to lead the market
        """
        scores = []
        
        for _, row in metrics_df.iterrows():
            # Weight different factors
            momentum_score = row['return_20d'] * 0.3  # 30% weight on momentum
            short_term_score = row['return_5d'] * 0.25  # 25% weight on short-term
            medium_term_score = row['return_60d'] * 0.20  # 20% weight on medium-term
            
            # Volatility penalty (lower volatility is better for stability)
            volatility_penalty = -abs(row['volatility']) * 0.1
            
            # Volume boost (high volume confirms strength)
            volume_boost = (row['volume_ratio'] - 1) * 5 if row['volume_ratio'] > 1 else 0
            
            # Recent performance boost
            recent_boost = row['return_1d'] * 0.15  # 15% weight on today's performance
            
            # Calculate composite score
            total_score = (
                momentum_score + 
                short_term_score + 
                medium_term_score + 
                volatility_penalty + 
                volume_boost + 
                recent_boost
            )
            
            scores.append({
                'sector': row['sector'],
                'ticker': row['ticker'],
                'ai_score': round(total_score, 2),
                'momentum_score': round(momentum_score, 2),
                'short_term_score': round(short_term_score, 2),
                'medium_term_score': round(medium_term_score, 2),
                'volatility_penalty': round(volatility_penalty, 2),
                'volume_boost': round(volume_boost, 2),
                'recent_boost': round(recent_boost, 2),
                'return_1d': row['return_1d'],
                'return_5d': row['return_5d'],
                'return_20d': row['return_20d'],
                'return_60d': row['return_60d'],
                'volatility': row['volatility'],
                'volume_ratio': row['volume_ratio']
            })
        
        scores_df = pd.DataFrame(scores)
        # Sort by AI score descending
        scores_df = scores_df.sort_values('ai_score', ascending=False).reset_index(drop=True)
        
        # Add rank
        scores_df['rank'] = range(1, len(scores_df) + 1)
        
        return scores_df
    
    def predict_trend(self, metrics_df):
        """
        Predict market trend direction based on sector performance
        """
        avg_return_1d = metrics_df['return_1d'].mean()
        avg_return_5d = metrics_df['return_5d'].mean()
        avg_return_20d = metrics_df['return_20d'].mean()
        
        # Count positive vs negative sectors
        positive_sectors = len(metrics_df[metrics_df['return_20d'] > 0])
        total_sectors = len(metrics_df)
        positive_ratio = positive_sectors / total_sectors if total_sectors > 0 else 0
        
        # Determine overall market trend
        if avg_return_20d > 2 and positive_ratio > 0.6:
            trend = "Bullish"
            confidence = min(95, 60 + (avg_return_20d * 2))
        elif avg_return_20d < -2 and positive_ratio < 0.4:
            trend = "Bearish"
            confidence = min(95, 60 + (abs(avg_return_20d) * 2))
        else:
            trend = "Neutral"
            confidence = 50 + (positive_ratio * 20)
        
        return {
            'trend': trend,
            'confidence': round(confidence, 1),
            'avg_return_1d': round(avg_return_1d, 2),
            'avg_return_5d': round(avg_return_5d, 2),
            'avg_return_20d': round(avg_return_20d, 2),
            'positive_sectors': positive_sectors,
            'total_sectors': total_sectors,
            'positive_ratio': round(positive_ratio * 100, 1)
        }
    
    def get_top_sectors(self, scores_df, n=3):
        """Get top N leading sectors"""
        top_sectors = scores_df.head(n).to_dict('records')
        return top_sectors
    
    def get_bottom_sectors(self, scores_df, n=3):
        """Get bottom N lagging sectors"""
        bottom_sectors = scores_df.tail(n).to_dict('records')
        return bottom_sectors
    
    def generate_insights(self, scores_df, trend_data):
        """Generate AI-powered insights and recommendations"""
        insights = []
        
        # Top performing sector insight
        top_sector = scores_df.iloc[0]
        insights.append({
            'type': 'top_performer',
            'title': f"{top_sector['sector']} Leading the Market",
            'description': f"{top_sector['sector']} ({top_sector['ticker']}) has the highest AI score of {top_sector['ai_score']}, with {top_sector['return_20d']}% return over 20 days.",
            'importance': 'high'
        })
        
        # Market trend insight
        insights.append({
            'type': 'market_trend',
            'title': f"Overall Market Trend: {trend_data['trend']}",
            'description': f"Market shows {trend_data['trend'].lower()} sentiment with {trend_data['confidence']}% confidence. {trend_data['positive_sectors']} out of {trend_data['total_sectors']} sectors are positive.",
            'importance': 'high'
        })
        
        # Momentum insight
        strong_momentum = scores_df[scores_df['return_20d'] > 5]
        if len(strong_momentum) > 0:
            insights.append({
                'type': 'momentum',
                'title': 'Strong Momentum Detected',
                'description': f"{len(strong_momentum)} sector(s) showing strong momentum (>5% in 20 days): {', '.join(strong_momentum['sector'].tolist())}",
                'importance': 'medium'
            })
        
        # Volatility warning
        high_volatility = scores_df[scores_df['volatility'] > 2]
        if len(high_volatility) > 0:
            insights.append({
                'type': 'risk',
                'title': 'High Volatility Alert',
                'description': f"{len(high_volatility)} sector(s) showing elevated volatility: {', '.join(high_volatility['sector'].tolist())}. Exercise caution.",
                'importance': 'medium'
            })
        
        return insights
