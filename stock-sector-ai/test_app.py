#!/usr/bin/env python3
"""
Comprehensive test script for Stock Sector Predictions AI
"""
import sys
sys.path.insert(0, '/workspaces/stock-sector-predictions-ai/stock-sector-ai')

from api.app import app
import json

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    """Test health check endpoint"""
    print_header("TEST 1: Health Check")
    client = app.test_client()
    response = client.get('/')
    
    print(f"Status Code: {response.status_code}")
    data = response.get_json()
    print(f"Status: {data.get('status')}")
    print(f"Service: {data.get('service')}")
    print(f"Version: {data.get('version')}")
    
    assert response.status_code == 200, "Health check failed"
    assert data['status'] == 'online', "Service is not online"
    print("✅ PASSED")

def test_sectors():
    """Test sectors list endpoint"""
    print_header("TEST 2: Get Sectors List")
    client = app.test_client()
    response = client.get('/api/sectors')
    
    print(f"Status Code: {response.status_code}")
    data = response.get_json()
    print(f"Total Sectors: {data.get('count')}")
    print(f"Sectors: {data.get('sectors')}")
    
    assert response.status_code == 200, "Sectors endpoint failed"
    assert data['count'] == 11, f"Expected 11 sectors, got {data['count']}"
    print("✅ PASSED")

def test_analysis():
    """Test analysis endpoint"""
    print_header("TEST 3: Get Sector Analysis")
    client = app.test_client()
    response = client.get('/api/analysis')
    
    print(f"Status Code: {response.status_code}")
    data = response.get_json()
    
    print(f"Market Trend: {data.get('market_trend')}")
    print(f"Period: {data.get('period')}")
    print(f"Demo Mode: {data.get('demo_mode')}")
    print(f"All Sectors Count: {len(data.get('all_sectors', []))}")
    
    top = data.get('top_sectors', [])
    print(f"\nTop 3 Sectors:")
    for i, sector in enumerate(top[:3], 1):
        print(f"  {i}. {sector['symbol']}: Score {sector['score']:.1f}")
    
    assert response.status_code == 200, "Analysis endpoint failed"
    assert 'market_trend' in data, "Missing market_trend"
    assert 'top_sectors' in data, "Missing top_sectors"
    print("✅ PASSED")

def test_analysis_with_period():
    """Test analysis endpoint with different periods"""
    print_header("TEST 4: Analysis with Different Periods")
    client = app.test_client()
    
    periods = ['1mo', '3mo', '6mo', '1y']
    for period in periods:
        response = client.get(f'/api/analysis?period={period}')
        print(f"Period: {period} - Status: {response.status_code} ✅")
        assert response.status_code == 200, f"Failed for period {period}"
    
    print("✅ PASSED")

def test_predictions():
    """Test predictions endpoint"""
    print_header("TEST 5: Get Predictions")
    client = app.test_client()
    response = client.get('/api/predict')
    
    print(f"Status Code: {response.status_code}")
    data = response.get_json()
    
    preds = data.get('predictions', [])
    print(f"Predictions Count: {len(preds)}")
    print(f"Message: {data.get('message')}")
    
    print(f"\nTop Predictions:")
    for i, pred in enumerate(preds[:5], 1):
        print(f"  {i}. {pred['symbol']}: Score {pred['score']:.1f}, Trend: {pred['trend']}")
    
    assert response.status_code == 200, "Predictions endpoint failed"
    assert 'predictions' in data, "Missing predictions"
    print("✅ PASSED")

def run_all_tests():
    """Run all tests"""
    print("\n" + "🚀"*20)
    print("  Stock Sector Predictions AI - Test Suite")
    print("🚀"*20)
    
    try:
        test_health()
        test_sectors()
        test_analysis()
        test_analysis_with_period()
        test_predictions()
        
        print_header("ALL TESTS PASSED ✅")
        print("\n✨ Application is working perfectly!\n")
        return True
        
    except AssertionError as e:
        print_header(f"TEST FAILED ❌")
        print(f"Error: {str(e)}\n")
        return False
    except Exception as e:
        print_header(f"ERROR ❌")
        print(f"Unexpected error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
