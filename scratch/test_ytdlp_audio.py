import yt_dlp
import time

def test_search(query):
    t0 = time.time()
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'noplaylist': True,
        'default_search': 'ytsearch1'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            res = ydl.extract_info(f"ytsearch1:{query}", download=False)
            dt = time.time() - t0
            if 'entries' in res and res['entries']:
                v = res['entries'][0]
            else:
                v = res
            return {
                'id': v.get('id'),
                'title': v.get('title'),
                'duration': v.get('duration'),
                'thumbnail': v.get('thumbnail'),
                'audio_url': v.get('url'),
                'elapsed': round(dt, 2)
            }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    for q in ['gulabi sadi', 'kesariya', 'believer']:
        info = test_search(q)
        print(f"Query: {q} | ID: {info.get('id')} | Time: {info.get('elapsed')}s | HasAudioUrl: {bool(info.get('audio_url'))}")
        if info.get('audio_url'):
            print(f"  URL prefix: {info['audio_url'][:70]}...")
