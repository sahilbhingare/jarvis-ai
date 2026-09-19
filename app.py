import os
import sys
import re
import psutil
import requests
import threading
import time
import urllib.parse
from flask import Flask, render_template, request, jsonify, send_from_directory, Response, stream_with_context, send_file
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

from jarvis_actions import (
    handle_action, get_system_status, get_current_time,
    get_live_news, load_notes, add_note, clear_notes,
    load_reminders, check_due_reminders, clear_reminders,
    change_volume, capture_screenshot
)
from jarvis_brain import get_answer
from jarvis_voice import generate_speech_file, speak_sync
from jarvis_music import get_audio_stream_url
app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())



MAINTENANCE_MODE = False  # Set to False to open the website

@app.route('/')
def index():
    if MAINTENANCE_MODE:
        return render_template('maintenance.html')
    return render_template('index.html')

# -------------------------------------------------------------
# 💬 Core Chat API with Multi-turn Memory
# -------------------------------------------------------------
@app.route('/api/chat', methods=['POST'])
def chat():
    if MAINTENANCE_MODE:
        return jsonify({'status': 'error', 'message': 'Website is closed. J.A.R.V.I.S. is offline.'}), 503
        
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    lang = data.get('lang', 'mr').strip()
    persona = data.get('persona', 'ironman').strip()
    session_id = data.get('session_id', 'client-session-1').strip()
    image_b64 = data.get('image', None)
    user_name = data.get('user_name', 'Sir').strip()
    if not user_name:
        user_name = 'Sir'

    if not message and not image_b64:
        return jsonify({'status': 'error', 'message': 'Empty query'}), 400

    print(f"\n[JARVIS CHAT] Query: '{message}' | Lang: {lang} | Persona: {persona} | HasImage: {bool(image_b64)} | User: {user_name}")

    # 1. Check if query triggers a system action (Volume, Screenshot, Lock, News, Notes, Reminders, Apps, YouTube, etc.)
    is_action, action_response = handle_action(message, lang)

    if is_action:
        final_text = action_response
        # Personality touch on actions
        if persona == 'mavala' and not any(k in final_text for k in ['🚩', '[MUSIC', '[WEATHER', '[LIVE_NEWS']):
            final_text = f"🚩 जय भवानी! जय शिवाजी! {final_text}"
    else:
        # 2. Query Jarvis Brain (Shivaji Maharaj, Forts, Panchang, Hindu Dharma, Gemini AI, Wikipedia)
        final_text = get_answer(message, lang, session_id=session_id, image=image_b64, user_name=user_name)
        if persona == 'mavala' and not any(k in final_text for k in ['🚩', '[MUSIC', '[WEATHER']):
            final_text = f"🚩 {final_text}"
        elif persona == 'casual' and not any(k in final_text for k in ['[MUSIC', '[WEATHER']):
            if lang == 'mr' and not final_text.startswith('अरे'):
                final_text = f"मित्रा, {final_text}"


    # 2. Detect Aarti, Music and Stop/Pause commands
    raw_lower = message.lower()
    is_stop_cmd = any(k in raw_lower for k in [
        'आरती थांबव', 'गाणे थांबव', 'गाणं थांबव', 'आरती बंद कर', 'गाणं बंद कर', 'गाणे बंद कर',
        'गाणी थांबव', 'गाणी बंद कर', 'म्युझिक थांबव', 'म्युझिक बंद कर', 'ऑडिओ थांबव', 'ऑडिओ बंद कर',
        'गाना बंद करो', 'गाना रोको', 'संगीत थांबव', 'संगीत बंद कर',
        'stop music', 'pause music', 'stop song', 'pause song',
        'stop aarti', 'pause aarti', 'थांबव', 'बंद कर', 'stop', 'pause'
    ])

    # Check for music player token in response
    music_vid_match = re.search(r'\[MUSIC_PLAYER:([a-zA-Z0-9_-]+)\|', final_text)
    is_music = bool(music_vid_match) and not is_stop_cmd
    music_vid = music_vid_match.group(1) if music_vid_match else None

    is_hanuman_chalisa = ('[HANUMAN_CHALISA_PLAYER]' in final_text) or any(k in raw_lower for k in [
        'हनुमान चालीसा', 'श्री हनुमान चालीसा', 'हनुमान चालिसा', 'श्री हनुमान चालिसा',
        'maruti stotra', 'मारुती स्तोत्र', 'hanuman chalisa', 'shree hanuman chalisa',
        'shri hanuman chalisa', 'bajarangbali chalisa', 'बजरंगबली चालीसा', 'हनुमान स्तोत्र'
    ])
    is_shivraya_aarti = ('[SHIVRAYA_AARTI_PLAYER]' in final_text) or any(k in raw_lower for k in [
        'शिव शंकराचा', 'शिवशंकराचा', 'शिवरायांची आरती', 'शिवराय आरती',
        'शिवाजी महाराज आरती', 'छत्रपती शिवाजी महाराज आरती',
        'shiv shankaracha', 'shivraya aarti', 'shivaji maharaj aarti', 'shivaji aarti',
        'shivrayanchi', 'shivraya arati', 'shivrayanchi arati', 'shivrayanchi aarti',
        'shivrayachi aarti', 'shivrayachi arati'
    ])
    is_ganpati_aarti = ('[AARTI_PLAYER]' in final_text) or (not is_shivraya_aarti and not is_hanuman_chalisa and not is_music and any(k in raw_lower for k in [
        'गणपती बाप्पा आरती', 'गणपतीची आरती', 'गणपती आरती', 'sukhkarta', 'सुखकर्ता', 'ganpati aarti',
        'आरती लाव', 'आरती सुरू कर', 'आरती चालू कर', 'आरती वाजव', 'play aarti', 'bappa aarti',
        'आरती', 'aarti', 'arati', 'arti'
    ]))

    if is_hanuman_chalisa and not is_stop_cmd:
        # Directly serve authentic world-famous Shri Hanuman Chalisa (Hariharan / Gulshan Kumar)
        audio_url = '/static/audio/hanuman_chalisa.webm'
        is_aarti = True
        aarti_type = 'hanuman_chalisa'
        is_stop = False
    elif is_shivraya_aarti and not is_stop_cmd:
        # Directly serve authentic 'Shiv Shankaracha Tu Avatar' Aarti (Aadarsh Shinde)
        audio_url = '/static/audio/shivraya_aarti.webm'
        is_aarti = True
        aarti_type = 'shivraya'
        is_stop = False
    elif is_ganpati_aarti and not is_stop_cmd:
        # Directly serve authentic original Marathi Ganpati Aarti MP3 (Lata & Usha Mangeshkar)
        audio_url = '/static/audio/ganpati_aarti_original.mp3'
        is_aarti = True
        aarti_type = 'ganpati'
        is_stop = False
    elif is_music and not is_stop_cmd:
        # Directly stream the authentic music audio through high-speed Range proxy
        audio_url = f'/api/music/stream?v={music_vid}'
        is_aarti = False
        aarti_type = None
        is_stop = False
    elif is_stop_cmd:
        audio_url = None
        is_aarti = False
        aarti_type = None
        is_stop = True
    else:
        # 3. Generate Neural Voice MP3 synchronously — ensures audio is ready before response
        from jarvis_voice import speak_sync
        audio_url = speak_sync(final_text, preferred_lang=lang) or None
        is_aarti = False
        aarti_type = None
        is_stop = False

    print(f"[JARVIS REPLY] Text: {final_text[:60]}... | Audio: {audio_url} | Music: {is_music} | Aarti: {is_aarti} ({aarti_type}) | Stop: {is_stop}")

    return jsonify({
        'status': 'success',
        'query': message,
        'response': final_text,
        'audio_url': audio_url,
        'is_action': is_action,
        'is_aarti': is_aarti,
        'aarti_type': aarti_type,
        'is_music': is_music,
        'music_vid': music_vid,
        'is_stop': is_stop,
        'lang': lang,
        'session_id': session_id
    })

# -------------------------------------------------------------
# 🎤 Dynamic TTS Endpoint (Reduces Chat Latency)
# -------------------------------------------------------------
@app.route('/api/tts', methods=['GET'])
def tts_stream():
    text = request.args.get('text', '').strip()
    lang = request.args.get('lang', 'mr').strip()
    
    if not text:
        return '', 400
        
    audio_path_url = speak_sync(text, preferred_lang=lang)
    
    if audio_path_url and audio_path_url.startswith('/static/audio/'):
        filename = audio_path_url.replace('/static/audio/', '')
        filepath = os.path.join(app.root_path, 'static', 'audio', filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='audio/mpeg')
            
    return '', 500

# -------------------------------------------------------------
# 🎵 In-Page Music Direct Audio Stream Proxy (100% Zero Redirect & Error 150 Bypass)
# -------------------------------------------------------------
@app.route('/api/music/check', methods=['GET'])
def music_check():
    """Quick check if a YouTube video is embeddable."""
    vid = request.args.get('v', '').strip()
    if not vid or len(vid) != 11:
        return jsonify({'embeddable': False}), 400
    try:
        import requests as req
        r = req.get(
            f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json',
            timeout=4
        )
        return jsonify({'embeddable': r.status_code == 200})
    except Exception:
        return jsonify({'embeddable': True})  # assume ok if check fails


@app.route('/api/music/stream', methods=['GET', 'HEAD'])
def music_stream():
    """
    Streams high-fidelity direct audio with HTTP Range partial content support.
    Completely eliminates YouTube embed restrictions (Error 150/101) and browser redirect.
    """
    vid = request.args.get('v', '').strip()
    q = request.args.get('q', '').strip()
    if not vid:
        return jsonify({'status': 'error', 'message': 'Missing video id'}), 400

    direct_url = get_audio_stream_url(vid, fallback_query=q)
    if not direct_url:
        return jsonify({'status': 'error', 'message': 'Could not extract audio stream'}), 404

    range_header = request.headers.get('Range', None)
    req_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*'
    }
    if range_header:
        req_headers['Range'] = range_header

    try:
        # Handle HEAD request quickly for Safari/Android metadata fetching
        if request.method == 'HEAD':
            upstream = requests.head(direct_url, headers=req_headers, timeout=12)
            resp_headers = {}
            for h in ['Content-Type', 'Content-Length', 'Accept-Ranges']:
                val = upstream.headers.get(h)
                if val: resp_headers[h] = val
            return Response(status=upstream.status_code, headers=resp_headers)

        upstream = requests.get(direct_url, headers=req_headers, stream=True, timeout=12)
        
        def generate():
            for chunk in upstream.iter_content(chunk_size=65536):
                if chunk:
                    yield chunk

        resp_headers = {}
        for h in ['Content-Type', 'Content-Range', 'Content-Length', 'Accept-Ranges', 'ETag', 'Last-Modified']:
            val = upstream.headers.get(h)
            if val:
                resp_headers[h] = val

        if 'Accept-Ranges' not in resp_headers:
            resp_headers['Accept-Ranges'] = 'bytes'
        if 'Content-Type' not in resp_headers:
            resp_headers['Content-Type'] = 'audio/mp4'

        return Response(
            stream_with_context(generate()),
            status=upstream.status_code,
            headers=resp_headers
        )
    except Exception as e:
        print(f"[MUSIC STREAM PROXY ERROR] {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# -------------------------------------------------------------
# ⏰ Reminders API & Polling
# -------------------------------------------------------------
@app.route('/api/reminders/due', methods=['GET'])
def get_due_reminders_api():
    """Polls for reminders that are due right now."""
    due = check_due_reminders()
    if due:
        for r in due:
            # Generate speech voice for the reminder announcement
            msg_text = f"सर, आपल्यासाठी रिमाइंड आहे: {r.get('message', '')}"
            r['audio_url'] = speak_sync(msg_text, preferred_lang='mr')
    return jsonify({
        'status': 'success',
        'due_reminders': due
    })

@app.route('/api/reminders', methods=['GET', 'DELETE'])
def reminders_api():
    if request.method == 'GET':
        return jsonify({'status': 'success', 'reminders': load_reminders()})
    elif request.method == 'DELETE':
        clear_reminders()
        return jsonify({'status': 'success', 'message': 'All reminders cleared'})

# -------------------------------------------------------------
# 📝 Notes API
# -------------------------------------------------------------
@app.route('/api/notes', methods=['GET', 'POST', 'DELETE'])
def notes_api():
    if request.method == 'GET':
        return jsonify({'status': 'success', 'notes': load_notes()})
    elif request.method == 'POST':
        data = request.get_json() or {}
        text = data.get('text', '').strip()
        if text:
            msg = add_note(text, lang=data.get('lang', 'mr'))
            return jsonify({'status': 'success', 'message': msg, 'notes': load_notes()})
        return jsonify({'status': 'error', 'message': 'Empty note text'}), 400
    elif request.method == 'DELETE':
        clear_notes()
        return jsonify({'status': 'success', 'message': 'All notes cleared'})

# -------------------------------------------------------------
# 📰 Live News API
# -------------------------------------------------------------
@app.route('/api/news', methods=['GET'])
def news_api():
    lang = request.args.get('lang', 'mr')
    news_text = get_live_news(lang)
    return jsonify({'status': 'success', 'news': news_text})

# -------------------------------------------------------------
# 🔊 Volume & Screenshot Direct APIs
# -------------------------------------------------------------
@app.route('/api/volume', methods=['POST'])
def volume_api():
    data = request.get_json() or {}
    action = data.get('action', 'up')
    steps = int(data.get('steps', 5))
    msg = change_volume(action, steps, lang=data.get('lang', 'mr'))
    return jsonify({'status': 'success', 'message': msg})

@app.route('/api/screenshot', methods=['POST'])
def screenshot_api():
    data = request.get_json() or {}
    lang = data.get('lang', 'mr')
    success, msg, url = capture_screenshot(lang)
    return jsonify({'status': 'success' if success else 'error', 'message': msg, 'url': url})

# -------------------------------------------------------------
# ⚙️ Status & Settings API
# -------------------------------------------------------------
@app.route('/api/status', methods=['GET'])
def system_status():
    has_gemini = bool(os.getenv("GEMINI_API_KEY", "").strip())
    battery = psutil.sensors_battery()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()

    telemetry = {
        'battery_percent': battery.percent if battery else None,
        'power_plugged': battery.power_plugged if battery else None,
        'cpu_percent': round(cpu_percent, 1),
        'ram_percent': round(ram.percent, 1)
    }

    return jsonify({
        'status': 'online',
        'gemini_configured': has_gemini,
        'time': get_current_time('mr'),
        'diagnostics': get_system_status('mr'),
        'telemetry': telemetry
    })

@app.route('/api/settings', methods=['POST'])
def update_settings():
    data = request.get_json() or {}
    api_key = data.get('gemini_api_key', '').strip()
    
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key
        # Update .env file
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            new_lines = []
            found = False
            for line in lines:
                if line.startswith('GEMINI_API_KEY='):
                    new_lines.append(f"GEMINI_API_KEY={api_key}\n")
                    found = True
                else:
                    new_lines.append(line)
            if not found:
                new_lines.append(f"GEMINI_API_KEY={api_key}\n")
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return jsonify({'status': 'success', 'message': 'Gemini API Key saved successfully!'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
            
    return jsonify({'status': 'error', 'message': 'No API key provided'}), 400

@app.route('/api/local-ip', methods=['GET'])
def get_local_network_info():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    port = int(os.getenv('PORT', 5000))
    return jsonify({
        'status': 'success',
        'ip': ip,
        'port': port,
        'url': f"http://{ip}:{port}"
    })

def cleanup_old_screenshots():
    """Background task to delete screenshots older than 24 hours."""
    while True:
        try:
            screenshots_dir = os.path.join(os.path.dirname(__file__), 'static', 'screenshots')
            if os.path.exists(screenshots_dir):
                now = time.time()
                for filename in os.listdir(screenshots_dir):
                    filepath = os.path.join(screenshots_dir, filename)
                    if os.path.isfile(filepath):
                        # If file is older than 24 hours (86400 seconds)
                        if os.stat(filepath).st_mtime < now - 86400:
                            os.remove(filepath)
                            print(f"[SECURITY] Auto-deleted old screenshot: {filename}")
        except Exception as e:
            print(f"[SECURITY] Screenshot cleanup error: {e}")
        time.sleep(3600)  # Check every hour

if __name__ == '__main__':
    # Start background cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_screenshots, daemon=True)
    cleanup_thread.start()

    port = int(os.getenv('PORT', 5000))
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    print(f"===========================================================")
    print(f"   J.A.R.V.I.S. VOICE ASSISTANT ONLINE (V3.0 MEGA UPGRADE)")
    print(f"   Local PC:    http://127.0.0.1:{port}")
    print(f"   Wi-Fi/Phone: http://{local_ip}:{port}")
    print(f"===========================================================")
    app.run(host='0.0.0.0', port=port, debug=False)
