import requests

def test_gold_and_nifty():
    results = {}
    # Nifty 50 (^NSEI)
    try:
        res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        meta = res.json()['chart']['result'][0]['meta']
        results['nifty'] = meta.get('regularMarketPrice')
    except Exception as e:
        results['nifty'] = str(e)
        
    # Gold (GC=F)
    try:
        res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        meta = res.json()['chart']['result'][0]['meta']
        results['gold_usd'] = meta.get('regularMarketPrice')
    except Exception as e:
        results['gold_usd'] = str(e)

    return results

print(test_gold_and_nifty())
