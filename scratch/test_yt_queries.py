import requests
import re
import urllib.parse
import time

queries = ['gulabi sadi', 'tauba tauba', 'chhatrapati shivaji maharaj song', 'kesariya', 'believer song', 'lofi songs', 'romantic hindi songs', 'marathi gane']

for q in queries:
    t0 = time.time()
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=5)
        dt = time.time() - t0
        vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
        print(f"[{q}] Status: {res.status_code} ({dt:.2f}s) | Vids found: {len(vids)} | Top: {vids[0] if vids else 'NONE'}")
    except Exception as e:
        print(f"[{q}] Exception: {e}")
