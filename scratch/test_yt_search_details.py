import requests
import re
import json
import urllib.parse

def search_youtube_videos(query, max_results=5):
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,mr;q=0.8,hi;q=0.7'
    }
    res = requests.get(url, headers=headers, timeout=5)
    vids = []
    
    # Try ytInitialData
    m = re.search(r'var ytInitialData = ({.*?});</script>', res.text)
    if m:
        try:
            data = json.loads(m.group(1))
            contents = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [])
            for section in contents:
                item_section = section.get('itemSectionRenderer', {}).get('contents', [])
                for item in item_section:
                    if 'videoRenderer' in item:
                        vr = item['videoRenderer']
                        vid = vr.get('videoId')
                        title = vr.get('title', {}).get('runs', [{}])[0].get('text', '')
                        length = vr.get('lengthText', {}).get('simpleText', '')
                        owner = vr.get('ownerText', {}).get('runs', [{}])[0].get('text', '')
                        badges = vr.get('badges', [])
                        # Check thumbnail
                        thumbs = vr.get('thumbnail', {}).get('thumbnails', [])
                        thumb = thumbs[-1]['url'] if thumbs else f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                        if vid and title:
                            vids.append({
                                'id': vid,
                                'title': title,
                                'duration': length,
                                'channel': owner,
                                'thumbnail': thumb
                            })
                        if len(vids) >= max_results:
                            break
                if len(vids) >= max_results:
                    break
        except Exception as e:
            pass
            
    if not vids:
        raw_vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
        seen = set()
        for v in raw_vids:
            if v not in seen:
                seen.add(v)
                vids.append({
                    'id': v,
                    'title': query,
                    'duration': '',
                    'channel': 'YouTube',
                    'thumbnail': f"https://img.youtube.com/vi/{v}/hqdefault.jpg"
                })
            if len(vids) >= max_results:
                break
    return vids

if __name__ == '__main__':
    for q in ['gulabi sadi song', 'kesariya', 'chhatrapati shivaji maharaj song']:
        res = search_youtube_videos(q, 3)
        print(f"\nQuery: {q} (Found {len(res)}):")
        for idx, v in enumerate(res):
            line = f"  {idx+1}. ID: {v['id']} | Duration: {v['duration']} | Title: {v['title'][:35]} | Channel: {v['channel']}"
            print(line.encode('ascii', 'replace').decode('ascii'))
