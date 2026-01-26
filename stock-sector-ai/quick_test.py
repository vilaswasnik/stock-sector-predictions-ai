#!/usr/bin/env python
import sys
sys.path.insert(0, '/workspaces/stock-sector-predictions-ai/stock-sector-ai')

try:
    from api.app import app
    
    print("\n" + "="*70)
    print("  Stock Sector Predictions AI - Test Results")
    print("="*70 + "\n")
    
    client = app.test_client()
    
    # Test 1
    print("[1/5] Testing Health Check...")
    r1 = client.get('/')
    assert r1.status_code == 200
    print("      ✅ Status: 200 OK")
    print(f"      Response: {r1.get_json()}\n")
    
    # Test 2
    print("[2/5] Testing Sectors Endpoint...")
    r2 = client.get('/api/sectors')
    assert r2.status_code == 200
    data = r2.get_json()
    print(f"      ✅ Status: 200 OK")
    print(f"      Sectors Found: {data.get('count')}")
    print(f"      Sample: {data.get('sectors')[:3]}\n")
    
    # Test 3
    print("[3/5] Testing Analysis Endpoint...")
    r3 = client.get('/api/analysis')
    assert r3.status_code == 200
    data = r3.get_json()
    print(f"      ✅ Status: 200 OK")
    print(f"      Market Trend: {data.get('market_trend')}")
    print(f"      Top Sectors: {len(data.get('top_sectors', []))}")
    print(f"      All Sectors: {len(data.get('all_sectors', []))}\n")
    
    # Test 4
    print("[4/5] Testing Analysis with Period Parameter...")
    r4 = client.get('/api/analysis?period=1y')
    assert r4.status_code == 200
    print(f"      ✅ Status: 200 OK (period=1y)\n")
    
    # Test 5
    print("[5/5] Testing Predictions Endpoint...")
    r5 = client.get('/api/predict')
    assert r5.status_code == 200
    data = r5.get_json()
    print(f"      ✅ Status: 200 OK")
    print(f"      Predictions: {len(data.get('predictions', []))}\n")
    
    print("="*70)
    print("  ✅ ALL TESTS PASSED!")
    print("="*70)
    print("\n🎉 Application is working perfectly!\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
