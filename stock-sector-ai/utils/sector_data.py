"""
Sector Data Fetcher - Retrieves real-time market sector performance data
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Set user agent to avoid blocks
import requests
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

class SectorDataFetcher:
    def __init__(self):
        # Major sector ETFs
        self.sectors = {
            'Technology': 'XLK',
            'Healthcare': 'XLV',
            'Financials': 'XLF',
            'Energy': 'XLE',
            'Consumer Discretionary': 'XLY',
            'Industrials': 'XLI',
            'Consumer Staples': 'XLP',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Materials': 'XLB',
            'Communication Services': 'XLC',
            'Gold': 'GLD',
            'Silver': 'SLV',
            'Metals & Mining': 'XME',
            'Crypto/Bitcoin': 'BITO',
            'Defense & Aerospace': 'ITA'
        }
        
    def fetch_sector_data(self, period='3mo'):
        """Fetch historical data for all sectors"""
        sector_data = {}
        
        for sector_name, ticker in self.sectors.items():
            try:
                etf = yf.Ticker(ticker)
                etf.session = session
                hist = etf.history(period=period)
                if not hist.empty:
                    sector_data[sector_name] = {
                        'ticker': ticker,
                        'data': hist,
                        'current_price': hist['Close'].iloc[-1],
                        'volume': hist['Volume'].iloc[-1]
                    }
                else:
                    print(f"Warning: No data for {sector_name} ({ticker})")
            except Exception as e:
                print(f"Error fetching {sector_name}: {e}")
                
        return sector_data
    
    def calculate_performance_metrics(self, sector_data):
        """Calculate key performance metrics for each sector"""
        metrics = []
        
        for sector_name, data in sector_data.items():
            hist = data['data']
            
            # Calculate returns
            current_price = hist['Close'].iloc[-1]
            price_1d_ago = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_5d_ago = hist['Close'].iloc[-5] if len(hist) > 5 else current_price
            price_20d_ago = hist['Close'].iloc[-20] if len(hist) > 20 else current_price
            price_60d_ago = hist['Close'].iloc[-60] if len(hist) > 60 else current_price
            
            # Calculate percentage changes
            return_1d = ((current_price - price_1d_ago) / price_1d_ago) * 100
            return_5d = ((current_price - price_5d_ago) / price_5d_ago) * 100
            return_20d = ((current_price - price_20d_ago) / price_20d_ago) * 100
            return_60d = ((current_price - price_60d_ago) / price_60d_ago) * 100
            
            # Calculate volatility (standard deviation of returns)
            returns = hist['Close'].pct_change().dropna()
            volatility = returns.std() * 100
            
            # Calculate momentum (rate of change)
            momentum = return_20d
            
            # Volume trend
            avg_volume = hist['Volume'].mean()
            current_volume = data['volume']
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            metrics.append({
                'sector': sector_name,
                'ticker': data['ticker'],
                'current_price': round(current_price, 2),
                'return_1d': round(return_1d, 2),
                'return_5d': round(return_5d, 2),
                'return_20d': round(return_20d, 2),
                'return_60d': round(return_60d, 2),
                'volatility': round(volatility, 2),
                'momentum': round(momentum, 2),
                'volume_ratio': round(volume_ratio, 2),
                'timestamp': datetime.now().isoformat()
            })
        
        return pd.DataFrame(metrics)
