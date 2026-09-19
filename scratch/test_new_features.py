import subprocess
import requests
import re
import datetime
import psutil
import ctypes

def test_clipboard():
    try:
        p = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, timeout=3)
        return p.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def test_cricket():
    try:
        url = "https://news.google.com/rss/search?q=cricket+live+score+india&hl=en-IN&gl=IN&ceid=IN:en"
        res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res.content)
        items = []
        for it in root.findall('./channel/item')[:3]:
            title = it.find('title').text
            items.append(title)
        return items
    except Exception as e:
        return f"Error: {e}"

def test_markets():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN"
        res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        data = res.json()
        meta = data['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice')
        prev = meta.get('chartPreviousClose')
        change = round(price - prev, 2) if (price and prev) else 0
        return f"Sensex: {price} ({'+' if change>=0 else ''}{change})"
    except Exception as e:
        return f"Error: {e}"

print("Clipboard:", test_clipboard()[:50])
print("Cricket:", test_cricket())
print("Markets:", test_markets())
