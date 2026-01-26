"""Demo data generator for when Yahoo Finance is unavailable"""
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_demo_data():
    """Generate realistic demo sector data"""
    sectors = {
        'Technology': {'ticker': 'XLK', 'base_return': 8.5},
        'Healthcare': {'ticker': 'XLV', 'base_return': 5.2},
        'Financials': {'ticker': 'XLF', 'base_return': 6.8},
        'Energy': {'ticker': 'XLE', 'base_return': -2.3},
        'Consumer Discretionary': {'ticker': 'XLY', 'base_return': 7.1},
        'Industrials': {'ticker': 'XLI', 'base_return': 4.9},
        'Consumer Staples': {'ticker': 'XLP', 'base_return': 3.2},
        'Utilities': {'ticker': 'XLU', 'base_return': 2.1},
        'Real Estate': {'ticker': 'XLRE', 'base_return': 1.8},
        'Materials': {'ticker': 'XLB', 'base_return': 3.7},
        'Communication Services': {'ticker': 'XLC', 'base_return': 6.3},
        'Gold': {'ticker': 'GLD', 'base_return': 12.4},
        'Silver': {'ticker': 'SLV', 'base_return': 15.8},
        'Metals & Mining': {'ticker': 'XME', 'base_return': 9.2},
        'Crypto/Bitcoin': {'ticker': 'BITO', 'base_return': 45.7},
        'Defense & Aerospace': {'ticker': 'ITA', 'base_return': 11.3}
    }
    
    metrics = []
    for sector_name, data in sectors.items():
        base = data['base_return']
        
        metrics.append({
            'sector': sector_name,
            'ticker': data['ticker'],
            'current_price': round(random.uniform(80, 150), 2),
            'return_1d': round(base * random.uniform(0.05, 0.15), 2),
            'return_5d': round(base * random.uniform(0.3, 0.5), 2),
            'return_20d': round(base, 2),
            'return_60d': round(base * random.uniform(1.5, 2.0), 2),
            'volatility': round(random.uniform(1.0, 3.5), 2),
            'momentum': round(base, 2),
            'volume_ratio': round(random.uniform(0.8, 1.3), 2),
            'timestamp': datetime.now().isoformat()
        })
    
    return pd.DataFrame(metrics)
