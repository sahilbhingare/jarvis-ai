import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import requests

BASE_URL = "http://127.0.0.1:5000"

print("--- TEST 1: Request 'गुलाबी साडी वाजव' ---")
r1 = requests.post(f"{BASE_URL}/api/chat", json={"message": "गुलाबी साडी वाजव", "lang": "mr"})
d1 = r1.json()
print("Status:", r1.status_code)
print("is_music:", d1.get("is_music"))
print("audio_url:", d1.get("audio_url"))
print("music_vid:", d1.get("music_vid"))
assert d1.get("is_music") is True, "Failed: is_music should be True"
assert d1.get("audio_url", "").startswith("/api/music/stream?v="), "Failed: audio_url should point to /api/music/stream"

print("\n--- TEST 2: Direct Audio Stream Range Request ---")
stream_url = f"{BASE_URL}{d1['audio_url']}"
r_stream = requests.get(stream_url, headers={"Range": "bytes=0-2048"}, stream=True, timeout=10)
print("Stream Status Code:", r_stream.status_code)
print("Content-Type:", r_stream.headers.get("Content-Type"))
print("Content-Range:", r_stream.headers.get("Content-Range"))
chunk = r_stream.raw.read(2048)
print("Streamed Bytes:", len(chunk))
assert r_stream.status_code in (200, 206), "Failed: stream status should be 206 or 200"
assert len(chunk) > 0, "Failed: chunk should contain audio data"

print("\n--- TEST 3: Request 'kesariya play kar' ---")
r2 = requests.post(f"{BASE_URL}/api/chat", json={"message": "kesariya play kar", "lang": "mr"})
d2 = r2.json()
print("Status:", r2.status_code)
print("is_music:", d2.get("is_music"))
print("audio_url:", d2.get("audio_url"))
assert d2.get("is_music") is True

print("\n--- TEST 4: Stop Song 'गाणे थांबव' ---")
r3 = requests.post(f"{BASE_URL}/api/chat", json={"message": "गाणे थांबव", "lang": "mr"})
d3 = r3.json()
print("Status:", r3.status_code)
print("is_stop:", d3.get("is_stop"))
print("audio_url:", d3.get("audio_url"))
assert d3.get("is_stop") is True
assert d3.get("audio_url") is None

print("\n--- TEST 5: Generic 'play song' ---")
r4 = requests.post(f"{BASE_URL}/api/chat", json={"message": "play song", "lang": "en"})
d4 = r4.json()
print("Status:", r4.status_code)
print("is_music:", d4.get("is_music"))
print("audio_url:", d4.get("audio_url"))
assert d4.get("is_music") is True

print("\nALL MUSIC STREAMING TESTS PASSED PERFECTLY! 🎵🚀")
