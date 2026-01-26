"""
Alpha Vantage Data Fetcher - Free alternative to Yahoo Finance
Get your free API key from: https://www.alphavantage.co/support/#api-key
"""
import requests
import pandas as pd
from datetime import datetime
import time
import os

class AlphaVantageDataFetcher:
    def __init__(self, api_key=None):
        """
        Initialize with Alpha Vantage API key
        Get free key from: https://www.alphavantage.co/support/#api-key
        """
        self.api_key = api_key or os.getenv('ALPHAVANTAGE_API_KEY', 'demo')
        self.base_url = 'https://www.alphavantage.co/query'
        
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
        
    def fetch_daily_data(self, symbol):
        """Fetch daily time series data for a symbol"""
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'apikey': self.api_key,
                'outputsize': 'compact'  # Last 100 days
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            data = response.json()
            
            # Check for rate limit
            if 'Note' in data:
                print(f"Rate limit reached for {symbol}: {data['Note']}")
                return None
            
            if 'Time Series (Daily)' in data:
                df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.astype(float)
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df = df.sort_index()
                return df
            else:
                error_msg = data.get('Note', data.get('Error Message', 'Unknown error'))
                if 'premium endpoint' not in error_msg.lower():
                    print(f"Error fetching {symbol}: {error_msg}")
                return None
                
        except Exception as e:
            print(f"Exception fetching {symbol}: {str(e)}")
            return None
    
    def fetch_sector_data(self, period='3mo', max_sectors=10):
        """Fetch historical data for sectors (limited to avoid timeouts)"""
        sector_data = {}
        
        print(f"Note: Alpha Vantage free tier limits to 25 requests/day")
        print(f"Fetching data for top {max_sectors} sectors to avoid timeouts...")
        
        # Limit to top sectors to avoid timeout
        limited_sectors = dict(list(self.sectors.items())[:max_sectors])
        
        for idx, (sector_name, ticker) in enumerate(limited_sectors.items(), 1):
            print(f"[{idx}/{len(limited_sectors)}] Fetching {sector_name} ({ticker})...")
            
            hist = self.fetch_daily_data(ticker)
            
            if hist is not None and not hist.empty:
                sector_data[sector_name] = {
                    'ticker': ticker,
                    'data': hist,
                    'current_price': hist['Close'].iloc[-1],
                    'volume': hist['Volume'].iloc[-1]
                }
            else:
                print(f"Warning: No data for {sector_name} ({ticker})")
            
            # Rate limiting: Alpha Vantage free tier allows 5 requests per minute
            # Reduce sleep time to 6 seconds (10 requests/minute should be safe)
            if idx < len(limited_sectors):
                time.sleep(6)
        
        return sector_data
    
    def calculate_performance_metrics(self, sector_data):
        """Calculate performance metrics from sector data"""
        metrics = []
        
        for sector_name, data in sector_data.items():
            try:
                df = data['data']
                current_price = data['current_price']
                
                # Calculate returns for different periods
                return_1d = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2] * 100) if len(df) > 1 else 0
                return_5d = ((df['Close'].iloc[-1] - df['Close'].iloc[-6]) / df['Close'].iloc[-6] * 100) if len(df) > 5 else 0
                return_20d = ((df['Close'].iloc[-1] - df['Close'].iloc[-21]) / df['Close'].iloc[-21] * 100) if len(df) > 20 else 0
                return_60d = ((df['Close'].iloc[-1] - df['Close'].iloc[-61]) / df['Close'].iloc[-61] * 100) if len(df) > 60 else 0
                
                # Calculate volatility (standard deviation of daily returns)
                daily_returns = df['Close'].pct_change().dropna()
                volatility = daily_returns.std() * 100
                
                # Calculate momentum (rate of change)
                momentum = return_20d
                
                # Calculate volume ratio
                avg_volume = df['Volume'].tail(20).mean()
                current_volume = df['Volume'].iloc[-1]
                volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1.0
                
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
                
            except Exception as e:
                print(f"Error calculating metrics for {sector_name}: {str(e)}")
                continue
        
        return pd.DataFrame(metrics)
