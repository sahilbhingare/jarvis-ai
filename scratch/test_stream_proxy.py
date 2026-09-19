import requests
from jarvis_music import get_audio_stream_url

vid = "B_6d3RBiEN0"
url = get_audio_stream_url(vid)
print("Fetched URL successfully")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Range': 'bytes=0-1024'
}
r = requests.get(url, headers=headers, stream=True, timeout=10)
print("Status code:", r.status_code)
print("Headers:")
for k in ['Content-Type', 'Content-Range', 'Content-Length', 'Accept-Ranges']:
    print(f"  {k}: {r.headers.get(k)}")

chunk = next(r.iter_content(chunk_size=1024))
print(f"Read chunk of size {len(chunk)} bytes. First 16 bytes: {chunk[:16]}")
