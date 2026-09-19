"""
=============================================================================
🎵 JARVIS AI - In-Page Zero-Redirect Music & Song Player Engine
=============================================================================
Provides seamless in-page music search, playback, and multiple-candidate
fallback without external redirects or opening external browser tabs.
=============================================================================
"""

import os
import re
import json
import base64
import random
import urllib.parse
import requests

# Curated high-energy trending fallback hits when query is generic (e.g. "गाणे वाजव", "play song")
TRENDING_SONGS = [
    {"query": "Gulabi Sadi Sanju Rathod", "title": "गुलाबी साडी (Gulabi Sadi) - Sanju Rathod"},
    {"query": "Kesariya Brahmastra", "title": "केसरिया (Kesariya) - Arijit Singh"},
    {"query": "Raja Shivaji Anthem Desh Music", "title": "राजा शिवछत्रपती ॲन्थम (Raja Shivaji Anthem)"},
    {"query": "Tauba Tauba Karan Aujla Bad Newz", "title": "तौबा तौबा (Tauba Tauba) - Karan Aujla"},
    {"query": "Believer Imagine Dragons", "title": "Believer - Imagine Dragons"},
    {"query": "Deva Deva Brahmastra Arijit Singh", "title": "देवा देवा (Deva Deva) - Arijit Singh"},
    {"query": "Shri Swami Samarth Tarak Mantra", "title": "श्री स्वामी समर्थ तारक मंत्र"},
    {"query": "Aarambh Hai Prachand Piyush Mishra", "title": "आरंभ है प्रचंड (Aarambh Hai Prachand)"}
]

# In-memory cache for fast repeated queries
MUSIC_CACHE = {}

def clean_song_query(query: str) -> str:
    """Removes common voice command filler words to get the pure song/artist name."""
    q = query.strip()
    
    # Common removal patterns in Marathi, Hindi, and English
    patterns = [
        r'^(?:मला|कृपया|जार्व्हिस|hey jarvis|jarvis)\s+',
        r'(?:गाणे|गाणं|गाणी|गाना|गीत|गाण)\s+(?:वाजव|लाव|ऐकव|सुरू कर|चालू कर|बजाओ|सुनाओ|चलाओ|लगाओ)',
        r'(?:वाजव|लाव|ऐकव|बजाओ|सुनाओ|चलाओ|लगाओ)\s+(?:गाणे|गाणं|गाणी|गाना|गीत)',
        r'(?:कोणतेही|कोणतंपण|काहीतरी|छान|नवीन|मस्त|एक|ek|kahi tari|chhan|navin)\s+(?:गाणे|गाणं|गाणी|गाना)',
        r'^(?:play\s+song|play\s+music|play|song\s+play\s+kar|song\s+play|music\s+play)\s*',
        r'\s+(?:song\s+play\s+kar|song\s+play|song\s+lav|song\s+vajav|song|music)$',
        r'^(?:गाणे\s+वाजव|गाणं\s+वाजव|गाणे\s+लाव|गाणं\s+लाव|गाना\s+बजाओ|गाना\s+सुनाओ|गाना\s+चलाओ)$',
        r'(?:ऑन\s+यूट्यूब|यूट्यूबवर|यूट्यूब\s+वर|on\s+youtube)'
    ]
    
    for p in patterns:
        q = re.sub(p, '', q, flags=re.IGNORECASE).strip()
        
    return q.strip()

def search_music_tracks(query: str, max_candidates: int = 4) -> list:
    """
    Searches YouTube for tracks matching query and extracts structured metadata:
    id, title, duration, channel/artist, and high-res thumbnail.
    """
    cleaned = clean_song_query(query)
    is_default = False
    
    if not cleaned or len(cleaned) < 2:
        chosen = random.choice(TRENDING_SONGS)
        cleaned = chosen['query']
        is_default = True

    cache_key = cleaned.lower()
    if cache_key in MUSIC_CACHE:
        return MUSIC_CACHE[cache_key]

    vids = []

    # Primary: use yt-dlp for accurate, exact song search
    try:
        import yt_dlp
        search_query = f'ytsearch{max_candidates}:{cleaned} official audio'
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)
            entries = result.get('entries', []) if result else []
            for entry in entries:
                if not entry:
                    continue
                vid = entry.get('id') or ''
                title = entry.get('title') or cleaned.title()
                duration_secs = entry.get('duration')
                if duration_secs:
                    mins, secs = divmod(int(duration_secs), 60)
                    duration = f"{mins}:{secs:02d}"
                else:
                    duration = 'HD'
                channel = entry.get('channel') or entry.get('uploader') or 'Official Music'
                thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                if vid and len(vid) == 11:
                    vids.append({'id': vid, 'title': title, 'duration': duration, 'channel': channel, 'thumbnail': thumb})
        print(f"[MUSIC ENGINE] yt-dlp found {len(vids)} results for: {cleaned}")
    except Exception as e:
        print(f"[MUSIC ENGINE] yt-dlp search failed, falling back to scrape: {e}")

    # Fallback: old YouTube HTML scraping
    if not vids:
        try:
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(cleaned + ' song')}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9,mr;q=0.8,hi;q=0.7'
            }
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
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
                                    thumbs = vr.get('thumbnail', {}).get('thumbnails', [])
                                    thumb = thumbs[-1]['url'] if thumbs else f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                                    if vid and title and len(vid) == 11:
                                        vids.append({'id': vid, 'title': title, 'duration': length or 'HD', 'channel': owner or 'Official Music', 'thumbnail': thumb})
                                    if len(vids) >= max_candidates:
                                        break
                            if len(vids) >= max_candidates:
                                break
                    except Exception as ex:
                        print(f"[MUSIC ENGINE] ytInitialData parse error: {ex}")
                if not vids:
                    raw_vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
                    seen = set()
                    for v in raw_vids:
                        if v not in seen:
                            seen.add(v)
                            vids.append({'id': v, 'title': cleaned.title(), 'duration': 'HD', 'channel': 'YouTube Music', 'thumbnail': f"https://img.youtube.com/vi/{v}/hqdefault.jpg"})
                        if len(vids) >= max_candidates:
                            break
        except Exception as e:
            print(f"[MUSIC ENGINE] Scrape fallback error: {e}")

    # Fallback to predefined top hits if network fails or search returns empty
    if not vids:
        backup_id = "B_6d3RBiEN0"  # Gulabi Sadi
        vids = [{
            'id': backup_id,
            'title': "गुलाबी साडी (Gulabi Sadi) - Official",
            'duration': "3:46",
            'channel': "Sanju Rathod",
            'thumbnail': f"https://img.youtube.com/vi/{backup_id}/hqdefault.jpg"
        }]

    MUSIC_CACHE[cache_key] = vids
    return vids

# In-memory direct audio stream cache
AUDIO_STREAM_CACHE = {}

def get_audio_stream_url(video_id: str, fallback_query: str = '') -> str:
    """
    Extracts high-quality direct audio playback URL for any YouTube video ID using yt_dlp.
    Cached in memory to ensure zero-latency re-requests and seeking.
    """
    if not video_id:
        return None
    if video_id in AUDIO_STREAM_CACHE:
        return AUDIO_STREAM_CACHE[video_id]

    import yt_dlp
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'socket_timeout': 10
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            url = info.get('url')
            if url:
                AUDIO_STREAM_CACHE[video_id] = url
                return url
    except Exception as e:
        print(f"[MUSIC AUDIO] Extraction by ID failed for {video_id}: {e}")

    # Fallback to search query if ID extraction had an issue
    if fallback_query:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                res = ydl.extract_info(f"ytsearch1:{fallback_query} audio", download=False)
                entries = res.get('entries', [])
                if entries and entries[0].get('url'):
                    url = entries[0]['url']
                    AUDIO_STREAM_CACHE[video_id] = url
                    return url
        except Exception as ex:
            print(f"[MUSIC AUDIO] Fallback query extraction failed: {ex}")

    return None

def play_music(query: str, lang: str = 'mr') -> str:
    """
    Generates the complete in-page Holographic Music Player response.
    Pre-warms the audio stream in background so playback starts instantly.
    Never redirects to external browser.
    """
    import threading
    candidates = search_music_tracks(query)
    primary = candidates[0]
    alternates = candidates[1:] if len(candidates) > 1 else []

    track_title = primary.get('title', 'Superhit Song')
    vid_id = primary.get('id', '')
    channel = primary.get('channel', 'Music')
    duration = primary.get('duration', 'HD')

    # Pre-warm direct audio URL in daemon thread
    if vid_id:
        threading.Thread(target=get_audio_stream_url, args=(vid_id, query), daemon=True).start()

    # Construct secure base64 JSON payload for frontend player card
    card_data = {
        "primary": primary,
        "alternates": alternates,
        "query": clean_song_query(query) or track_title,
        "audio_stream": f"/api/music/stream?v={vid_id}",
        "lang": lang
    }
    raw_json = json.dumps(card_data, ensure_ascii=False)
    b64_payload = base64.b64encode(raw_json.encode('utf-8')).decode('utf-8')

    token = f"[MUSIC_PLAYER:{vid_id}|{b64_payload}]"

    # Multilingual respectful voice response
    if lang == 'mr':
        msg = f"नक्कीच सर! मी थेट **'{track_title}'** सुरू केले आहे. आनंद घ्या! 🎵🎬\n\n{token}"
    elif lang == 'hi':
        msg = f"बिल्कुल सर! मैंने सीधे **'{track_title}'** शुरू कर दिया है। आनंद लीजिए! 🎵🎬\n\n{token}"
    else:
        msg = f"Playing **'{track_title}'** right now, Sir! Enjoy! 🎵🎬\n\n{token}"

    return msg

