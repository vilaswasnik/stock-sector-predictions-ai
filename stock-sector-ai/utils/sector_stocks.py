"""
Mapping of sectors to their key constituent stocks
"""

SECTOR_STOCKS = {
    'Technology': [
        {'symbol': 'AAPL', 'name': 'Apple Inc.'},
        {'symbol': 'MSFT', 'name': 'Microsoft'},
        {'symbol': 'NVDA', 'name': 'NVIDIA'},
        {'symbol': 'GOOGL', 'name': 'Alphabet (Google)'},
        {'symbol': 'META', 'name': 'Meta Platforms'}
    ],
    'Healthcare': [
        {'symbol': 'JNJ', 'name': 'Johnson & Johnson'},
        {'symbol': 'UNH', 'name': 'UnitedHealth'},
        {'symbol': 'PFE', 'name': 'Pfizer'},
        {'symbol': 'ABBV', 'name': 'AbbVie'},
        {'symbol': 'TMO', 'name': 'Thermo Fisher'}
    ],
    'Financials': [
        {'symbol': 'JPM', 'name': 'JPMorgan Chase'},
        {'symbol': 'BAC', 'name': 'Bank of America'},
        {'symbol': 'WFC', 'name': 'Wells Fargo'},
        {'symbol': 'V', 'name': 'Visa'},
        {'symbol': 'MA', 'name': 'Mastercard'}
    ],
    'Energy': [
        {'symbol': 'XOM', 'name': 'Exxon Mobil'},
        {'symbol': 'CVX', 'name': 'Chevron'},
        {'symbol': 'COP', 'name': 'ConocoPhillips'},
        {'symbol': 'SLB', 'name': 'Schlumberger'},
        {'symbol': 'EOG', 'name': 'EOG Resources'}
    ],
    'Consumer Discretionary': [
        {'symbol': 'AMZN', 'name': 'Amazon'},
        {'symbol': 'TSLA', 'name': 'Tesla'},
        {'symbol': 'HD', 'name': 'Home Depot'},
        {'symbol': 'MCD', 'name': 'McDonald\'s'},
        {'symbol': 'NKE', 'name': 'Nike'}
    ],
    'Industrials': [
        {'symbol': 'BA', 'name': 'Boeing'},
        {'symbol': 'CAT', 'name': 'Caterpillar'},
        {'symbol': 'UNP', 'name': 'Union Pacific'},
        {'symbol': 'HON', 'name': 'Honeywell'},
        {'symbol': 'GE', 'name': 'General Electric'}
    ],
    'Consumer Staples': [
        {'symbol': 'WMT', 'name': 'Walmart'},
        {'symbol': 'PG', 'name': 'Procter & Gamble'},
        {'symbol': 'KO', 'name': 'Coca-Cola'},
        {'symbol': 'PEP', 'name': 'PepsiCo'},
        {'symbol': 'COST', 'name': 'Costco'}
    ],
    'Utilities': [
        {'symbol': 'NEE', 'name': 'NextEra Energy'},
        {'symbol': 'DUK', 'name': 'Duke Energy'},
        {'symbol': 'SO', 'name': 'Southern Company'},
        {'symbol': 'D', 'name': 'Dominion Energy'},
        {'symbol': 'AEP', 'name': 'American Electric'}
    ],
    'Real Estate': [
        {'symbol': 'AMT', 'name': 'American Tower'},
        {'symbol': 'PLD', 'name': 'Prologis'},
        {'symbol': 'CCI', 'name': 'Crown Castle'},
        {'symbol': 'EQIX', 'name': 'Equinix'},
        {'symbol': 'PSA', 'name': 'Public Storage'}
    ],
    'Materials': [
        {'symbol': 'LIN', 'name': 'Linde'},
        {'symbol': 'APD', 'name': 'Air Products'},
        {'symbol': 'ECL', 'name': 'Ecolab'},
        {'symbol': 'DD', 'name': 'DuPont'},
        {'symbol': 'NEM', 'name': 'Newmont'}
    ],
    'Communication Services': [
        {'symbol': 'GOOGL', 'name': 'Alphabet'},
        {'symbol': 'META', 'name': 'Meta'},
        {'symbol': 'DIS', 'name': 'Disney'},
        {'symbol': 'NFLX', 'name': 'Netflix'},
        {'symbol': 'CMCSA', 'name': 'Comcast'}
    ],
    'Gold': [
        {'symbol': 'NEM', 'name': 'Newmont'},
        {'symbol': 'GOLD', 'name': 'Barrick Gold'},
        {'symbol': 'AEM', 'name': 'Agnico Eagle'},
        {'symbol': 'FNV', 'name': 'Franco-Nevada'},
        {'symbol': 'WPM', 'name': 'Wheaton Precious'}
    ],
    'Silver': [
        {'symbol': 'AG', 'name': 'First Majestic'},
        {'symbol': 'PAAS', 'name': 'Pan American Silver'},
        {'symbol': 'HL', 'name': 'Hecla Mining'},
        {'symbol': 'FSM', 'name': 'Fortuna Silver'},
        {'symbol': 'EXK', 'name': 'Endeavour Silver'}
    ],
    'Metals & Mining': [
        {'symbol': 'FCX', 'name': 'Freeport-McMoRan'},
        {'symbol': 'NUE', 'name': 'Nucor'},
        {'symbol': 'VALE', 'name': 'Vale'},
        {'symbol': 'SCCO', 'name': 'Southern Copper'},
        {'symbol': 'MT', 'name': 'ArcelorMittal'}
    ],
    'Crypto/Bitcoin': [
        {'symbol': 'COIN', 'name': 'Coinbase'},
        {'symbol': 'MSTR', 'name': 'MicroStrategy'},
        {'symbol': 'RIOT', 'name': 'Riot Platforms'},
        {'symbol': 'MARA', 'name': 'Marathon Digital'},
        {'symbol': 'CLSK', 'name': 'CleanSpark'}
    ],
    'Defense & Aerospace': [
        {'symbol': 'LMT', 'name': 'Lockheed Martin'},
        {'symbol': 'RTX', 'name': 'Raytheon'},
        {'symbol': 'BA', 'name': 'Boeing'},
        {'symbol': 'NOC', 'name': 'Northrop Grumman'},
        {'symbol': 'GD', 'name': 'General Dynamics'}
    ]
}

def get_sector_stocks(sector_name):
    """Get related stocks for a given sector"""
    return SECTOR_STOCKS.get(sector_name, [])

def get_all_sector_stocks():
    """Get all sector-stock mappings"""
    return SECTOR_STOCKS
