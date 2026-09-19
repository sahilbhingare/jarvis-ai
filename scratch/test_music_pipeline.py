import sys
sys.path.insert(0, '.')
import json
from app import app

client = app.test_client()

print("Testing /api/chat with music query 'गुलाबी साडी'...")
res = client.post('/api/chat', json={'message': 'गुलाबी साडी', 'lang': 'mr'})
data = res.get_json()
print("Status Code:", res.status_code)
print("is_music:", data.get('is_music'))
print("audio_url:", data.get('audio_url'))
print("music_vid:", data.get('music_vid'))
print("response contains MUSIC_PLAYER:", '[MUSIC_PLAYER:' in data.get('response', ''))

vid = data.get('music_vid')
if vid:
    print(f"\nTesting /api/music/stream?v={vid} with Range request...")
    stream_res = client.get(f'/api/music/stream?v={vid}', headers={'Range': 'bytes=0-4096'})
    print("Stream Status Code:", stream_res.status_code)
    print("Content-Type:", stream_res.headers.get('Content-Type'))
    print("Content-Range:", stream_res.headers.get('Content-Range'))
    print("Data received bytes:", len(stream_res.data))

print("\nTesting /api/chat with 'गाणे वाजव'...")
res2 = client.post('/api/chat', json={'message': 'गाणे वाजव', 'lang': 'mr'})
data2 = res2.get_json()
print("Status Code:", res2.status_code)
print("is_music:", data2.get('is_music'))
print("audio_url:", data2.get('audio_url'))

print("\nTesting /api/chat with stop command 'गाणे थांबव'...")
res3 = client.post('/api/chat', json={'message': 'गाणे थांबव', 'lang': 'mr'})
data3 = res3.get_json()
print("Status Code:", res3.status_code)
print("is_stop:", data3.get('is_stop'))
print("audio_url:", data3.get('audio_url'))
