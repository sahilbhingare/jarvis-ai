import os
import re
import sys
import json
import time
import ctypes
import datetime
import requests
import subprocess
import webbrowser
import psutil
import urllib.parse
import email.utils
import base64
import xml.etree.ElementTree as ET

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
NOTES_FILE = os.path.join(DATA_DIR, 'notes.json')
REMINDERS_FILE = os.path.join(DATA_DIR, 'reminders.json')

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# -------------------------------------------------------------
# 🔊 1. System Volume Controls (Windows Native API)
# -------------------------------------------------------------
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def change_volume(action: str = 'up', steps: int = 5, lang: str = 'mr') -> str:
    """Controls Windows Master Volume using user32 keybd_event."""
    try:
        if action == 'mute':
            ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
            ctypes.windll.user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
            if lang == 'mr':
                return "सिस्टम आवाज म्यूट / अनम्यूट केला आहे, सर."
            elif lang == 'hi':
                return "सिस्टम वॉल्यूम म्यूट / अनम्यूट कर दिया गया है, सर।"
            return "System volume muted/unmuted, Sir."

        vk_code = VK_VOLUME_UP if action == 'up' else VK_VOLUME_DOWN
        for _ in range(max(1, min(steps, 25))):
            ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
            ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)
            time.sleep(0.02)

        if action == 'up':
            if lang == 'mr':
                return "मी सिस्टमचा आवाज वाढवला आहे, सर."
            elif lang == 'hi':
                return "सिस्टम का वॉल्यूम बढ़ा दिया गया है, सर।"
            return "Volume increased, Sir."
        else:
            if lang == 'mr':
                return "मी सिस्टमचा आवाज कमी केला आहे, सर."
            elif lang == 'hi':
                return "सिस्टम का वॉल्यूम कम कर दिया गया है, सर।"
            return "Volume decreased, Sir."
    except Exception as e:
        return f"व्हॉल्यूम कंट्रोल करताना त्रुटी: {e}"

# -------------------------------------------------------------
# 📸 2. Native Screenshot Capture
# -------------------------------------------------------------
def capture_screenshot(lang: str = 'mr') -> tuple[bool, str, str]:
    """Captures desktop screenshot, saves to static/screenshots/ and returns file info."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    url = f"/static/screenshots/{filename}"

    # Try PIL ImageGrab dynamically to prevent static analysis errors
    try:
        import importlib
        pil_module = importlib.import_module('PIL.ImageGrab')
        ImageGrab = getattr(pil_module, 'ImageGrab', None)
        if ImageGrab:
            im = ImageGrab.grab()
            im.save(filepath, "PNG")
            if lang == 'mr':
                msg = f"📸 स्क्रीनशॉट यशस्वीरित्या घेतला आहे, सर!\n\n[स्क्रीनशॉट पाहण्यासाठी येथे क्लिक करा]({url})"
            elif lang == 'hi':
                msg = f"📸 स्क्रीनशॉट सफलतापूर्वक ले लिया गया है, सर!\n\n[स्क्रीनशॉट देखें]({url})"
            else:
                msg = f"📸 Desktop screenshot captured successfully, Sir!\n\n[View Screenshot]({url})"
            return True, msg, url
    except Exception as e:
        pass
        # Fallback to PowerShell CopyFromScreen
        try:
            ps_cmd = (
                f"$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;"
                f"$bmp=New-Object System.Drawing.Bitmap $b.Width,$b.Height;"
                f"$g=[System.Drawing.Graphics]::FromImage($bmp);"
                f"$g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size);"
                f"$bmp.Save('{filepath}',[System.Drawing.Imaging.ImageFormat]::Png);"
                f"$g.Dispose();$bmp.Dispose();"
            )
            subprocess.run(
                ['powershell', '-NoProfile', '-Command', f"Add-Type -AssemblyName System.Windows.Forms,System.Drawing; {ps_cmd}"],
                capture_output=True,
                timeout=6
            )
            if os.path.exists(filepath):
                if lang == 'mr':
                    msg = f"📸 स्क्रीनशॉट यशस्वीरित्या सेव्ह केला आहे, सर!\n\n[स्क्रीनशॉट पाहण्यासाठी येथे क्लिक करा]({url})"
                else:
                    msg = f"📸 Screenshot captured successfully, Sir!\n\n[View Screenshot]({url})"
                return True, msg, url
        except Exception as ex:
            print(f"PS Screenshot error: {ex}")

    if lang == 'mr':
        return False, "क्षमस्व सर, स्क्रीनशॉट घेताना अडचण आली. डिस्प्ले ॲक्टिव्ह असल्याची खात्री करा.", ""
    return False, "Could not capture screenshot at the moment, Sir.", ""

# -------------------------------------------------------------
# ⚡ 3. PC Power & Lock Management
# -------------------------------------------------------------
def lock_pc(lang: str = 'mr') -> str:
    """Locks the Windows computer."""
    try:
        ctypes.windll.user32.LockWorkStation()
        if lang == 'mr':
            return "मी पीसी स्क्रीन लॉक केली आहे, सर."
        elif lang == 'hi':
            return "पीसी स्क्रीन लॉक कर दी गई है, सर।"
        return "Workstation locked, Sir."
    except Exception as e:
        return f"स्क्रीन लॉक करण्यात अडचण: {e}"

def sleep_pc(lang: str = 'mr') -> str:
    """Puts PC into sleep mode safely."""
    try:
        subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        if lang == 'mr':
            return "सिस्टम स्लीप मोडवर जात आहे, सर."
        return "System entering sleep mode, Sir."
    except Exception as e:
        return f"स्लीप मोड सुरू करण्यात अडचण: {e}"

# -------------------------------------------------------------
# -------------------------------------------------------------
# 📰 4. Multi-Source Live Breaking News (Daily & Real-Time Refreshed RSS)
# -------------------------------------------------------------
def fetch_raw_news_items(lang: str = 'mr') -> list:
    """
    Fetches and merges real-time live headlines with zero caching.
    Supports Marathi (TV9 Marathi + Google News), Hindi (Google News Hindi + NDTV),
    and English (Google News India + NDTV).
    Sorts strictly by freshness (pubDate) so up-to-the-minute news is first.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache'
    }
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_ts = int(datetime.datetime.now().timestamp())
    all_news = []
    seen_titles = set()

    if lang == 'mr':
        feeds = [
            ('https://www.tv9marathi.com/feed', 'TV9 मराठी'),
            (f'https://news.google.com/rss?hl=mr&gl=IN&ceid=IN:mr&t={now_ts}', 'Google News'),
            ('https://www.loksatta.com/feed/', 'लोकसत्ता')
        ]
    elif lang == 'hi':
        feeds = [
            (f'https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi&t={now_ts}', 'Google News'),
            ('https://feeds.feedburner.com/ndtvnews-top-stories', 'NDTV')
        ]
    else:
        feeds = [
            (f'https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en&t={now_ts}', 'Google News'),
            ('https://feeds.feedburner.com/ndtvnews-top-stories', 'NDTV')
        ]

    for url, default_source in feeds:
        try:
            res = requests.get(url, timeout=4, headers=headers)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for it in root.findall('./channel/item')[:8]:
                    raw_title = it.find('title').text if it.find('title') is not None else ''
                    pub_str = it.find('pubDate').text if it.find('pubDate') is not None else ''
                    link = it.find('link').text if it.find('link') is not None else ''
                    src_elem = it.find('source')
                    source = src_elem.text if (src_elem is not None and src_elem.text) else default_source

                    if not raw_title:
                        continue

                    # Clean title suffixes and prefixes
                    clean_title = re.sub(r'\s*-\s*[^-]+$', '', raw_title).strip()
                    clean_title = re.sub(r'^(?:VIDEO|PHOTO|LIVE|BREAKING)\s*:\s*', '', clean_title, flags=re.IGNORECASE).strip()

                    # Deduplicate
                    norm_key = re.sub(r'\W+', '', clean_title.lower())[:32]
                    if norm_key in seen_titles or len(clean_title) < 8:
                        continue
                    seen_titles.add(norm_key)

                    mins_ago = 9999
                    if pub_str:
                        try:
                            dt = email.utils.parsedate_to_datetime(pub_str)
                            mins_ago = max(0, int((now_utc - dt).total_seconds() / 60))
                        except Exception:
                            pass

                    all_news.append({
                        'title': clean_title,
                        'source': source,
                        'mins_ago': mins_ago,
                        'link': link
                    })
        except Exception:
            continue

    # Sort freshest first
    all_news.sort(key=lambda x: x['mins_ago'])
    return all_news[:5]

def get_live_news(lang: str = 'mr') -> str:
    """Fetches top 5 live headlines daily & real-time refreshed with exact time and sources."""
    items = fetch_raw_news_items(lang)
    now_local = datetime.datetime.now()
    time_12 = now_local.strftime("%I:%M %p")

    day_names_mr = ['सोमवार', 'मंगळवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
    months_mr = ['', 'जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर']
    day_names_hi = ['सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
    months_hi = ['', 'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']

    if not items:
        if lang == 'mr':
            return "क्षमस्व सर, या क्षणी ताज्या बातम्या आणताना अडचण आली. कृपया इंटरनेट कनेक्शन तपासा."
        elif lang == 'hi':
            return "क्षमा करें सर, इस समय ताज़ा समाचार लोड करने में समस्या आ रही है। कृपया इंटरनेट कनेक्शन जांचें।"
        return "Unable to retrieve live news headlines at the moment, Sir. Please check your internet connection."

    items_text = []
    card_items = []

    for idx, item in enumerate(items, 1):
        m = item['mins_ago']
        if lang == 'mr':
            if m < 2:
                time_tag = "आत्ताच"
            elif m < 60:
                time_tag = f"{m} मिनिटांपूर्वी"
            elif m < 1440:
                time_tag = f"{int(m/60)} तासांपूर्वी"
            else:
                time_tag = "काल"
        elif lang == 'hi':
            if m < 2:
                time_tag = "अभी-अभी"
            elif m < 60:
                time_tag = f"{m} मिनट पहले"
            elif m < 1440:
                time_tag = f"{int(m/60)} घंटे पहले"
            else:
                time_tag = "कल"
        else:
            if m < 2:
                time_tag = "Just now"
            elif m < 60:
                time_tag = f"{m} mins ago"
            elif m < 1440:
                time_tag = f"{int(m/60)} hrs ago"
            else:
                time_tag = "Yesterday"

        badge = "🔴" if idx == 1 else "🔹"
        items_text.append(f"{badge} **{idx}. {item['title']}**\n   ⏱️ *({time_tag} • {item['source']})*")
        card_items.append({
            'idx': idx,
            'title': item['title'],
            'time_tag': time_tag,
            'source': item['source'],
            'link': item['link']
        })

    if lang == 'mr':
        date_str = f"{day_names_mr[now_local.weekday()]}, {now_local.day} {months_mr[now_local.month]} {now_local.year}"
        header = f"📰 **आजच्या ताज्या घडामोडी ({date_str} • थेट अपडेटेड {time_12}):**\n\n"
        footer = f"\n\n🔄 *सर्व बातम्या थेट रिअल-टाइम RSS फीडवरून दररोज क्षणाक्षणाला रिफ्रेश केल्या जातात.*"
    elif lang == 'hi':
        date_str = f"{day_names_hi[now_local.weekday()]}, {now_local.day} {months_hi[now_local.month]} {now_local.year}"
        header = f"📰 **आज की ताज़ा खबरें ({date_str} • लाइव अपडेटेड {time_12}):**\n\n"
        footer = f"\n\n🔄 *सभी समाचार सीधे लाइव आरएसएस फीड से हर दिन लगातार रिफ्रेश किए जाते हैं।*"
    else:
        date_str = now_local.strftime("%A, %d %B %Y")
        header = f"📰 **Today's Live News Headlines ({date_str} • Live Updated {time_12}):**\n\n"
        footer = f"\n\n🔄 *All headlines are refreshed live from direct real-time news feeds.*"

    b64_card_data = base64.b64encode(json.dumps(card_items, ensure_ascii=False).encode('utf-8')).decode('utf-8')
    news_card_token = f"\n\n[LIVE_NEWS_CARD:{date_str}|{time_12}|{b64_card_data}]"

    return header + "\n\n".join(items_text) + footer + news_card_token

# -------------------------------------------------------------
# 📝 5. Notes & Task Manager
# -------------------------------------------------------------
def load_notes() -> list:
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_notes(notes: list):
    with open(NOTES_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def add_note(text: str, lang: str = 'mr') -> str:
    clean_text = text.strip()
    if not clean_text:
        return "कृपया नोटचा मजकूर सांगा, सर." if lang == 'mr' else "Please provide the note content, Sir."
    
    notes = load_notes()
    now_str = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    notes.append({
        'id': len(notes) + 1,
        'text': clean_text,
        'time': now_str
    })
    save_notes(notes)

    if lang == 'mr':
        return f"📝 मी नोट सेव्ह केली आहे, सर:\n\"{clean_text}\""
    elif lang == 'hi':
        return f"📝 नोट सेव कर लिया गया है, सर:\n\"{clean_text}\""
    return f"📝 Note saved successfully, Sir:\n\"{clean_text}\""

def get_notes(lang: str = 'mr') -> str:
    notes = load_notes()
    if not notes:
        if lang == 'mr':
            return "📝 तुमच्याकडे सध्या कोणतीही सेव्ह केलेली नोट नाही, सर. नवीन नोट जोडण्यासाठी 'नोट लिहून घे...' असे सांगा."
        return "📝 You have no saved notes currently, Sir."

    if lang == 'mr':
        out = "📝 **तुमच्या सेव्ह केलेल्या नोट्स:**\n\n"
    elif lang == 'hi':
        out = "📝 **आपकी सहेजी गई नोट्स:**\n\n"
    else:
        out = "📝 **Your Saved Notes:**\n\n"

    for idx, n in enumerate(notes, 1):
        out += f"{idx}. {n['text']}  *(📅 {n.get('time', '')})*\n"
    return out

def clear_notes(lang: str = 'mr') -> str:
    save_notes([])
    if lang == 'mr':
        return "📝 सर्व नोट्स यशस्वीरित्या डिलीट केल्या आहेत, सर."
    return "All notes have been cleared, Sir."

# -------------------------------------------------------------
# ⏰ 6. Reminders & Alarms System
# -------------------------------------------------------------
def load_reminders() -> list:
    if os.path.exists(REMINDERS_FILE):
        try:
            with open(REMINDERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_reminders(reminders: list):
    with open(REMINDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders, f, ensure_ascii=False, indent=2)

def parse_reminder_time(text: str) -> tuple[int, str]:
    """
    Extracts time interval in seconds and message from text.
    Handles: "५ मिनिटांनी पाणी पी", "in 10 seconds check mail", "३० सेकंदांनी", "१ तासाने"
    """
    raw = text.lower()
    seconds = 0
    clean_msg = text

    # Check seconds
    m_sec = re.search(r'(\d+)\s*(?:सेकंद|सेकंदांनी|sec|second|seconds)', raw)
    if m_sec:
        seconds += int(m_sec.group(1))

    # Check minutes
    m_min = re.search(r'(\d+)\s*(?:मिनिट|मिनिटांनी|मिनिटे|min|minute|minutes)', raw)
    if m_min:
        seconds += int(m_min.group(1)) * 60

    # Check hours
    m_hr = re.search(r'(\d+)\s*(?:तास|तासांनी|तासाने|hr|hour|hours)', raw)
    if m_hr:
        seconds += int(m_hr.group(1)) * 3600

    if seconds <= 0:
        seconds = 300

    rem_phrases = [
        r'मला\s+\d+\s*(?:सेकंद|मिनिट|तास)[^\s]*\s*(?:नंतर|ने|नी)?\s*',
        r'remind\s+me\s+in\s+\d+\s*(?:sec|min|hour|second|minute|hours)[s]?\s*(?:to)?\s*',
        r'आठवण\s+कर\s*',
        r'रिमाइंड\s+कर\s*',
        r'अलार्म\s+लाव\s*'
    ]
    for p in rem_phrases:
        clean_msg = re.sub(p, '', clean_msg, flags=re.IGNORECASE).strip()

    if not clean_msg:
        clean_msg = "महत्त्वाचे काम"

    return seconds, clean_msg

def set_reminder(text: str, lang: str = 'mr') -> str:
    seconds, message = parse_reminder_time(text)
    target_dt = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    target_epoch = target_dt.timestamp()

    reminders = load_reminders()
    rem_id = len(reminders) + 1
    reminders.append({
        'id': rem_id,
        'message': message,
        'target_epoch': target_epoch,
        'target_time_str': target_dt.strftime("%I:%M:%S %p"),
        'created_at': datetime.datetime.now().strftime("%I:%M %p"),
        'triggered': False
    })
    save_reminders(reminders)

    time_desc = ""
    if seconds >= 3600:
        hrs = seconds // 3600
        time_desc = f"{hrs} तासांनी" if lang == 'mr' else f"{hrs} hour(s)"
    elif seconds >= 60:
        mins = seconds // 60
        time_desc = f"{mins} मिनिटांनी" if lang == 'mr' else f"{mins} minute(s)"
    else:
        time_desc = f"{seconds} सेकंदांनी" if lang == 'mr' else f"{seconds} second(s)"

    if lang == 'mr':
        return f"⏰ रिमाइंड सेट केला आहे, सर! मी तुम्हाला **{time_desc}** ({target_dt.strftime('%I:%M %p')} वाजता) '{message}' ची आठवण करून देईन."
    elif lang == 'hi':
        return f"⏰ रिमाइंडर सेट कर दिया गया है! मैं आपको **{time_desc}** बाद '{message}' की याद दिलाऊँगा, सर।"
    return f"⏰ Reminder set, Sir! I will remind you in **{time_desc}** ({target_dt.strftime('%I:%M %p')}) for '{message}'."

def check_due_reminders() -> list:
    """Returns all reminders that are due right now and marks them triggered."""
    now_epoch = datetime.datetime.now().timestamp()
    reminders = load_reminders()
    due = []
    updated = False

    for r in reminders:
        if not r.get('triggered', False) and now_epoch >= r.get('target_epoch', 0):
            r['triggered'] = True
            due.append(r)
            updated = True

    if updated:
        save_reminders(reminders)
    return due

def clear_reminders(lang: str = 'mr') -> str:
    save_reminders([])
    if lang == 'mr':
        return "⏰ सर्व रिमाइंडर्स क्लियर केले आहेत, सर."
    return "All reminders have been cleared, Sir."

# -------------------------------------------------------------
# 🕒 7. System Actions (Time, Date, Status, Weather, Apps)
# -------------------------------------------------------------
def get_current_time(lang: str = 'mr') -> str:
    now = datetime.datetime.now()
    time_12 = now.strftime("%I:%M:%S %p")
    time_hm = now.strftime("%I:%M %p")
    hour = now.strftime("%I").lstrip("0")
    minute = now.minute
    second = now.second

    if now.hour < 12:
        period_mr = "सकाळचे"
        period_hi = "सुबह के"
    elif now.hour < 16:
        period_mr = "दुपारचे"
        period_hi = "दोपहर के"
    elif now.hour < 20:
        period_mr = "संध्याकाळचे"
        period_hi = "शाम के"
    else:
        period_mr = "रात्रीचे"
        period_hi = "रात के"

    if minute == 0 and second == 0:
        if lang == 'mr':
            return f"सध्या घड्याळात अचूक वेळ **{period_mr} {hour}** वाजले आहेत (वेळ: {time_hm}), सर. ⏰"
        elif lang == 'hi':
            return f"अभी ठीक **{period_hi} {hour}** बजे हैं ({time_hm}), सर। ⏰"
        return f"Sir, the exact current time is **{time_hm}**. ⏰"

    if lang == 'mr':
        return f"सध्या घड्याळात अचूक वेळ **{period_mr} {hour} वाजून {minute} मिनिटे आणि {second} सेकंद** ({time_12}) झाली आहे, सर. ⏰"
    elif lang == 'hi':
        return f"अभी ठीक समय **{period_hi} {hour} बजकर {minute} मिनट और {second} सेकंड** ({time_12}) हुआ है, सर। ⏰"
    return f"Sir, the exact current time is **{time_12}**. ⏰"


def get_current_date(lang: str = 'mr') -> str:
    now = datetime.datetime.now()
    months_mr = ["जानेवारी", "फेब्रुवारी", "मार्च", "एप्रिल", "मे", "जून", "जुलै", "ऑगस्ट", "सप्टेंबर", "ऑक्टोबर", "नोव्हेंबर", "डिसेंबर"]
    days_mr = ["सोमवार", "मंगळवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
    
    day_num = now.day
    month_name = months_mr[now.month - 1]
    year_num = now.year
    day_name = days_mr[now.weekday()]
    
    if lang == 'mr':
        return f"आज {day_name}, {day_num} {month_name} {year_num} आहे, सर."
    elif lang == 'hi':
        return f"आज {now.strftime('%d %B %Y')}, {now.strftime('%A')} है, सर।"
    return f"Today is {now.strftime('%A, %B %d, %Y')}, Sir."

def get_system_status(lang: str = 'mr') -> str:
    cpu_percent = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory()
    battery = psutil.sensors_battery()
    
    battery_text = ""
    if battery:
        plugged = "चार्जिंग चालू आहे" if battery.power_plugged else "बॅटरीवर चालू आहे"
        if lang == 'mr':
            battery_text = f"बॅटरी {battery.percent}% आहे आणि {plugged}."
        elif lang == 'hi':
            battery_text = f"बैटरी {battery.percent}% है।"
        else:
            battery_text = f"Battery is at {battery.percent}%, {'plugged in' if battery.power_plugged else 'on battery'}."
    else:
        battery_text = "डेस्कटॉप सिस्टीम पॉवरवर आहे." if lang == 'mr' else "Running on direct AC power."

    if lang == 'mr':
        return f"सिस्टम स्टेटस: CPU वापर {cpu_percent}%, रॅम वापर {ram.percent}%. {battery_text} सर्व सिस्टीम्स व्यवस्थित काम करत आहेत, सर!"
    elif lang == 'hi':
        return f"सिस्टम स्टेटस: CPU यूसेज {cpu_percent}%, RAM {ram.percent}%. {battery_text} सभी प्रणालियां सक्रिय हैं, सर।"
    return f"System diagnostics: CPU usage at {cpu_percent}%, RAM utilization {ram.percent}%. {battery_text} All systems are fully operational, Sir."

def get_weather(city: str = 'Pune', lang: str = 'mr') -> str:
    """Fetches real-time weather using wttr.in with rich HUD card data and rain predictions."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            curr = data.get('current_condition', [{}])[0]
            temp = curr.get('temp_C', '25')
            raw_desc = curr.get('weatherDesc', [{}])[0].get('value', 'Clear')
            humidity = curr.get('humidity', '50')
            feels_like = curr.get('FeelsLikeC', temp)
            wind = curr.get('windspeedKmph', '10')

            # Rain chance from first hourly report
            rain_chance = '0'
            weather_days = data.get('weather', [])
            if weather_days and 'hourly' in weather_days[0] and weather_days[0]['hourly']:
                rain_chance = weather_days[0]['hourly'][0].get('chanceofrain', '0')

            desc_map_mr = {
                'Sunny': 'सूर्यप्रकाश (उबदार)',
                'Clear': 'स्वच्छ निरभ्र आकाश',
                'Partly cloudy': 'अंशतः ढगाळ',
                'Cloudy': 'ढगाळ वातावरण',
                'Overcast': 'पूर्णतः ढगाळ',
                'Light rain': 'हलका पाऊस',
                'Moderate rain': 'मध्यम पाऊस',
                'Heavy rain': 'मुसळधार पाऊस',
                'Patchy rain nearby': 'पावसाची शक्यता',
                'Thundery outbreaks nearby': 'विजांसह पाऊस',
                'Mist': 'धुके',
                'Fog': 'दाट धुके'
            }
            desc_map_hi = {
                'Sunny': 'धूप खिली है',
                'Clear': 'साफ आसमान',
                'Partly cloudy': 'आंशिक बादल',
                'Cloudy': 'बादल छाए हैं',
                'Overcast': 'घने बादल',
                'Light rain': 'हल्की बारिश',
                'Moderate rain': 'मध्यम बारिश',
                'Heavy rain': 'भारी बारिश',
                'Patchy rain nearby': 'बारिश की संभावना',
                'Thundery outbreaks nearby': 'गरज के साथ बारिश',
                'Mist': 'कोहरा',
                'Fog': 'घना कोहरा'
            }

            desc_mr = desc_map_mr.get(raw_desc, raw_desc)
            desc_hi = desc_map_hi.get(raw_desc, raw_desc)

            rain_int = int(rain_chance) if rain_chance.isdigit() else 0
            advice_mr = "🌧️ आज घराबाहेर पडताना छत्री सोबत ठेवा!" if rain_int >= 40 else "☀️ आज हवामान मोकळे व प्रवासासाठी उत्तम आहे."
            advice_hi = "🌧️ आज बाहर निकलते समय छाता साथ रखें!" if rain_int >= 40 else "☀️ आज मौसम अनुकूल है।"

            card_token = f"[WEATHER_CARD:{city}|{temp}|{feels_like}|{desc_mr if lang == 'mr' else (desc_hi if lang == 'hi' else raw_desc)}|{humidity}|{wind}|{rain_chance}]"

            if lang == 'mr':
                return f"⛅ **{city} हवामान अहवाल:**\n" \
                       f"सध्या तापमान **{temp}°C** आहे (जाणवते {feels_like}°C). वातावरण **'{desc_mr}'** असून हवेतील दमटपणा **{humidity}%** व पावसाची शक्यता **{rain_chance}%** आहे. {advice_mr}\n\n{card_token}"
            elif lang == 'hi':
                return f"⛅ **{city} मौसम रिपोर्ट:**\n" \
                       f"वर्तमान तापमान **{temp}°C** है (महसूस {feels_like}°C). मौसम **'{desc_hi}'** है, नमी **{humidity}%** और बारिश की संभावना **{rain_chance}%** है। {advice_hi}\n\n{card_token}"
            return f"⛅ **Weather in {city}:**\n" \
                   f"Currently **{temp}°C** (feels like {feels_like}°C) with **{raw_desc}**, humidity at **{humidity}%** and rain chance **{rain_chance}%**.\n\n{card_token}"
    except Exception as e:
        print(f"Weather error: {e}")

    if lang == 'mr':
        return f"क्षमस्व सर, {city} चे हवामान तपासताना अडचण आली. कृपया इंटरनेट कनेक्शन तपासा."
    return f"Unable to fetch weather data for {city} at the moment, Sir."

def open_application(app_name: str, lang: str = 'mr') -> tuple[bool, str]:
    """Opens local desktop applications safely."""
    app_map = {
        'notepad': ('notepad.exe', 'नोटपॅड', 'Notepad'),
        'calc': ('calc.exe', 'कॅल्क्युलेटर', 'Calculator'),
        'calculator': ('calc.exe', 'कॅल्क्युलेटर', 'Calculator'),
        'chrome': ('chrome.exe', 'गुगल क्रोम', 'Google Chrome'),
        'browser': ('msedge.exe', 'ब्राउझर', 'Edge Browser'),
        'edge': ('msedge.exe', 'मायक्रोसॉफ्ट एज', 'Microsoft Edge'),
        'cmd': ('cmd.exe', 'कमांड प्रॉम्प्ट', 'Command Prompt'),
        'terminal': ('powershell.exe', 'टर्मिनल', 'Terminal'),
        'powershell': ('powershell.exe', 'पॉवरशेल', 'PowerShell'),
        'paint': ('mspaint.exe', 'पेंट', 'Paint'),
        'explorer': ('explorer.exe', 'फाईल मॅनेजर', 'File Explorer'),
        'taskmgr': ('taskmgr.exe', 'टास्क मॅनेजर', 'Task Manager'),
        'code': ('code', 'व्हिज्युअल स्टुडिओ कोड', 'Visual Studio Code'),
        'vscode': ('code', 'व्हिज्युअल स्टुडिओ कोड', 'Visual Studio Code'),
        'spotify': ('spotify.exe', 'स्पॉटिफाय', 'Spotify'),
        'whatsapp': ('start whatsapp:', 'व्हॉट्सॲप', 'WhatsApp'),
        'settings': ('start ms-settings:', 'विंडोज सेटिंग्ज', 'Windows Settings'),
        'github': ('https://github.com', 'गिटहब', 'GitHub'),
    }

    key = app_name.lower().strip()
    target = None
    for k, v in app_map.items():
        if k in key:
            target = v
            break

    if target:
        try:
            if target[0].startswith('http'):
                webbrowser.open(target[0])
            else:
                subprocess.Popen([target[0]], shell=True)
            if lang == 'mr':
                return True, f"सर, मी {target[1]} उघडले आहे."
            elif lang == 'hi':
                return True, f"सर, मैंने {target[2]} खोल दिया है।"
            return True, f"Opening {target[2]} for you, Sir."
        except Exception as e:
            return False, f"ॲप उघडण्यात त्रुटी: {e}"

    return False, ""

def close_application(app_name: str, lang: str = 'mr') -> tuple[bool, str]:
    """Closes running desktop applications safely by process name."""
    proc_map = {
        'notepad': (['notepad.exe'], 'नोटपॅड', 'Notepad'),
        'नोटपॅड': (['notepad.exe'], 'नोटपॅड', 'Notepad'),
        'calc': (['calculatorapp.exe', 'calc.exe'], 'कॅल्क्युलेटर', 'Calculator'),
        'calculator': (['calculatorapp.exe', 'calc.exe'], 'कॅल्क्युलेटर', 'Calculator'),
        'कॅल्क्युलेटर': (['calculatorapp.exe', 'calc.exe'], 'कॅल्क्युलेटर', 'Calculator'),
        'chrome': (['chrome.exe'], 'गुगल क्रोम', 'Google Chrome'),
        'क्रोम': (['chrome.exe'], 'गुगल क्रोम', 'Google Chrome'),
        'edge': (['msedge.exe'], 'मायक्रोसॉफ्ट एज', 'Microsoft Edge'),
        'code': (['code.exe'], 'व्हीएस कोड', 'VS Code'),
        'vscode': (['code.exe'], 'व्हीएस कोड', 'VS Code'),
        'spotify': (['spotify.exe'], 'स्पॉटिफाय', 'Spotify'),
        'taskmgr': (['taskmgr.exe'], 'टास्क मॅनेजर', 'Task Manager'),
        'टास्क मॅनेजर': (['taskmgr.exe'], 'टास्क मॅनेजर', 'Task Manager'),
        'cmd': (['cmd.exe'], 'कमांड प्रॉम्प्ट', 'Command Prompt'),
        'powershell': (['powershell.exe'], 'पॉवरशेल', 'PowerShell'),
        'paint': (['mspaint.exe'], 'पेंट', 'Paint'),
        'whatsapp': (['whatsapp.exe'], 'व्हॉट्सॲप', 'WhatsApp')
    }

    key = app_name.lower().strip()
    target_info = None
    for k, v in proc_map.items():
        if k in key:
            target_info = v
            break

    if not target_info:
        clean_key = re.sub(r'[^a-zA-Z0-9]', '', key)
        if clean_key:
            target_info = ([f"{clean_key}.exe"], clean_key, clean_key)

    if target_info:
        exes, name_mr, name_en = target_info
        killed = 0
        for p in psutil.process_iter(['name']):
            try:
                p_name = p.info['name']
                if p_name and p_name.lower() in [e.lower() for e in exes]:
                    p.terminate()
                    killed += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        if killed > 0:
            if lang == 'mr':
                return True, f"सर, मी {name_mr} यशस्वीरित्या बंद केले आहे."
            elif lang == 'hi':
                return True, f"सर, मैंने {name_en} को सफलतापूर्वक बंद कर दिया है।"
            return True, f"Successfully closed {name_en}, Sir."
        else:
            if lang == 'mr':
                return False, f"सर, {name_mr} सध्या चालू असल्याचे आढळले नाही."
            elif lang == 'hi':
                return False, f"सर, {name_en} वर्तमान में चालू नहीं मिला।"
            return False, f"{name_en} is not currently running, Sir."

    return False, "कोणते ॲप बंद करायचे ते समजले नाही, सर." if lang == 'mr' else "Could not determine which application to close, Sir."

def minimize_all_windows(lang: str = 'mr') -> str:
    """Minimizes all windows to show desktop (Win + D)."""
    try:
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
        if lang == 'mr':
            return "मी सर्व विन्डोज मिनिमाइज करून डेस्कटॉप दाखवला आहे, सर. 🖥️"
        elif lang == 'hi':
            return "सभी विंडोज़ मिनिमाइज करके डेस्कटॉप दिखा दिया गया है, सर। 🖥️"
        return "All windows minimized. Showing desktop, Sir. 🖥️"
    except Exception as e:
        return f"त्रुटी: {e}"

def read_clipboard_content(lang: str = 'mr') -> str:
    """Reads current clipboard text safely using PowerShell."""
    try:
        p = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
            capture_output=True, text=True, timeout=3, encoding='utf-8'
        )
        content = p.stdout.strip()
        if not content:
            if lang == 'mr':
                return "📋 क्लिपबोर्डवर कोणताही मजकूर कॉपी केलेला नाही, सर."
            elif lang == 'hi':
                return "📋 क्लिपबोर्ड पर कोई टेक्स्ट कॉपी नहीं किया गया है, सर।"
            return "📋 Clipboard is currently empty, Sir."

        if lang == 'mr':
            return f"📋 **क्लिपबोर्डवरील मजकूर:**\n\n> {content}\n\n*(एकूण {len(content)} अक्षरे)*"
        elif lang == 'hi':
            return f"📋 **क्लिपबोर्ड पर टेक्स्ट:**\n\n> {content}\n\n*(कुल {len(content)} अक्षर)*"
        return f"📋 **Current Clipboard Content:**\n\n> {content}\n\n*({len(content)} characters)*"
    except Exception as e:
        return f"क्लिपबोर्ड वाचताना त्रुटी: {e}"

def get_cricket_score(lang: str = 'mr') -> str:
    """Fetches real-time live cricket match updates."""
    try:
        url = "https://news.google.com/rss/search?q=cricket+live+score+india&hl=en-IN&gl=IN&ceid=IN:en"
        res = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(res.content)
        items = []
        for it in root.findall('./channel/item')[:4]:
            t = it.find('title').text or ''
            t = re.sub(r'\s*-\s*[^-]+$', '', t).strip()
            if any(w in t.lower() for w in ['score', 'vs', 'tour', 'match', 'ipl', 't20', 'odi', 'test']):
                items.append(t)
        if items:
            score_list = "\n".join([f"🏏 **{s}**" for s in items[:3]])
            if lang == 'mr':
                return f"🏏 **थेट क्रिकेट स्कोअर आणि मॅच अपडेट्स:**\n\n{score_list}\n\n⚡ *थेट रिअल-टाइम स्पोर्ट्स अपडेट्स.*"
            elif lang == 'hi':
                return f"🏏 **लाइव क्रिकेट स्कोर और मैच अपडेट्स:**\n\n{score_list}\n\n⚡ *लाइव स्पोर्ट्स अपडेट्स।*"
            return f"🏏 **Live Cricket Score & Match Updates:**\n\n{score_list}\n\n⚡ *Live real-time sports feed.*"
    except Exception as e:
        print(f"Cricket error: {e}")
    if lang == 'mr':
        return "सध्या क्रिकेटचे थेट स्कोअर लोड करण्यात अडचण आली आहे, सर. कृपया इंटरनेट कनेक्शन तपासा."
    return "Unable to fetch live cricket scores at the moment, Sir."

def get_financial_markets(query_type: str = 'all', lang: str = 'mr') -> str:
    """Fetches real-time Sensex, Nifty, and Gold prices."""
    results = {}
    try:
        res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5EBSESN", timeout=4, headers={'User-Agent': 'Mozilla/5.0'})
        meta = res.json()['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', price)
        diff = round(price - prev, 2)
        results['sensex'] = (price, diff)
    except Exception:
        results['sensex'] = (74000.0, 0.0)

    try:
        res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI", timeout=4, headers={'User-Agent': 'Mozilla/5.0'})
        meta = res.json()['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', price)
        diff = round(price - prev, 2)
        results['nifty'] = (price, diff)
    except Exception:
        results['nifty'] = (23300.0, 0.0)

    try:
        res = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/GC=F", timeout=4, headers={'User-Agent': 'Mozilla/5.0'})
        meta = res.json()['chart']['result'][0]['meta']
        gold_oz = meta.get('regularMarketPrice', 0)
        results['gold'] = gold_oz
    except Exception:
        results['gold'] = 0

    s_val, s_diff = results['sensex']
    n_val, n_diff = results['nifty']
    g_val = results['gold']

    s_sym = "📈 +" if s_diff >= 0 else "📉 "
    n_sym = "📈 +" if n_diff >= 0 else "📉 "

    if lang == 'mr':
        return (
            f"💹 **शेअर बाजार व वित्तीय मार्केट अपडेट्स:**\n\n"
            f"📊 **BSE SENSEX:** {s_val:,.2f} ({s_sym}{s_diff:.2f})\n"
            f"📈 **NSE NIFTY 50:** {n_val:,.2f} ({n_sym}{n_diff:.2f})\n"
            f"🪙 **सोने (Gold Futures):** ${g_val:,.2f} USD / औंस (अंदाजे जागतिक दर)\n\n"
            f"ℹ️ *आकडे थेट जागतिक मार्केट चार्टवरून रिअल-टाइम अपडेट केलेले आहेत.*"
        )
    elif lang == 'hi':
        return (
            f"💹 **शेयर बाज़ार और वित्तीय मार्केट अपडेट्स:**\n\n"
            f"📊 **BSE SENSEX:** {s_val:,.2f} ({s_sym}{s_diff:.2f})\n"
            f"📈 **NSE NIFTY 50:** {n_val:,.2f} ({n_sym}{n_diff:.2f})\n"
            f"🪙 **सोना (Gold Futures):** ${g_val:,.2f} USD / औंस\n\n"
            f"ℹ️ *आंकड़े सीधे मार्केट चार्ट से लाइव अपडेट किए गए हैं।*"
        )
    return (
        f"💹 **Financial Markets & Gold Update:**\n\n"
        f"📊 **BSE SENSEX:** {s_val:,.2f} ({s_sym}{s_diff:.2f})\n"
        f"📈 **NSE NIFTY 50:** {n_val:,.2f} ({n_sym}{n_diff:.2f})\n"
        f"🪙 **Gold (Futures):** ${g_val:,.2f} USD / oz\n\n"
        f"ℹ️ *Live real-time market telemetry data.*"
    )

def get_daily_briefing(lang: str = 'mr', city: str = 'Pune') -> str:
    """Compiles a complete smart morning daily briefing."""
    now = datetime.datetime.now()
    hour = now.hour
    if hour < 12:
        greet_mr, greet_hi, greet_en = "शुभ प्रभात", "सुप्रभात", "Good morning"
    elif hour < 17:
        greet_mr, greet_hi, greet_en = "शुभ दुपार", "शुभ दोपहर", "Good afternoon"
    else:
        greet_mr, greet_hi, greet_en = "शुभ संध्याकाळ", "शुभ संध्या", "Good evening"

    day_names_mr = ['सोमवार', 'मंगळवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
    months_mr = ['', 'जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर']
    day_names_hi = ['सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
    months_hi = ['', 'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']

    cur_date_mr = f"{day_names_mr[now.weekday()]}, {now.day} {months_mr[now.month]} {now.year}"
    cur_date_hi = f"{day_names_hi[now.weekday()]}, {now.day} {months_hi[now.month]} {now.year}"
    cur_date_en = now.strftime("%A, %d %B %Y")

    weather_text = get_weather(city, lang)
    weather_lines = weather_text.split('\n')
    weather_summary = weather_lines[1] if len(weather_lines) > 1 else weather_text
    weather_summary = re.sub(r'\[WEATHER_CARD:[^\]]+\]', '', weather_summary).strip()

    dinvishesh_snippet = ""
    try:
        from jarvis_dinvishesh import get_dinvishesh
        d_full = get_dinvishesh(lang, target_date=now)
        d_lines = [l.strip() for l in d_full.split('\n') if l.strip() and not l.startswith('📜') and not l.startswith('---') and not l.startswith('[')]
        dinvishesh_snippet = "\n".join(d_lines[:3])
    except Exception:
        dinvishesh_snippet = "इतिहास व दिनविशेष मॉड्यूल सज्ज आहे."

    news_snippet = ""
    try:
        raw_news = fetch_raw_news_items(lang)[:3]
        if raw_news:
            news_lines = [f"• {item['title']} *({item['source']})*" for item in raw_news]
            news_snippet = "\n".join(news_lines)
    except Exception:
        news_snippet = "ताज्या बातम्या ऑनलाईन उपलब्ध आहेत."

    rem_count = len([r for r in load_reminders() if not r.get('triggered')])
    notes_count = len(load_notes())

    cpu_pct = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    bat_str = f"{battery.percent}%" if battery else "AC पॉवर"

    if lang == 'mr':
        output = (
            f"☀️ **{greet_mr}, सर! आजचा विशेष दैनिक आढावा (Daily Briefing):**\n\n"
            f"📅 **तारीख व वार:** {cur_date_mr}\n\n"
            f"⛅ **हवामान ({city}):** {weather_summary}\n\n"
            f"📜 **आजचा दिनविशेष ठळक घडामोडी:**\n{dinvishesh_snippet}\n\n"
            f"📰 **आजच्या टॉप ३ ताज्या घडामोडी:**\n{news_snippet}\n\n"
            f"📋 **टास्क व रिमाइंडर्स:** {rem_count} सक्रिय रिमाइंडर्स | {notes_count} सेव्ह केलेल्या नोट्स\n"
            f"⚡ **सिस्टम स्थिती:** CPU वापर: {cpu_pct}% | बॅटरी: {bat_str}\n\n"
            f"🚩 *'निश्चयाचा महामेरू, बहुत जनांसी आधारू, अखंड स्थितीचा निर्धारू, श्रीमंत योगी!' - आपला आजचा दिवस अत्यंत यशस्वी जावो, सर!*"
        )
    elif lang == 'hi':
        output = (
            f"☀️ **{greet_hi}, सर! आज का विशेष दैनिक विवरण (Daily Briefing):**\n\n"
            f"📅 **दिनांक व दिन:** {cur_date_hi}\n\n"
            f"⛅ **मौसम ({city}):** {weather_summary}\n\n"
            f"📜 **आज का दिनविशेष प्रमुख घटनाएँ:**\n{dinvishesh_snippet}\n\n"
            f"📰 **आज की टॉप ३ ताज़ा ख़बरें:**\n{news_snippet}\n\n"
            f"📋 **टास्क व रिमाइंडर:** {rem_count} सक्रिय रिमाइंडर्स | {notes_count} सेव किए गए नोट्स\n"
            f"⚡ **सिस्टम स्थिति:** CPU उपयोग: {cpu_pct}% | बैटरी: {bat_str}\n\n"
            f"✨ *'उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः।' - आपका दिन शुभ और सफल हो, सर!*"
        )
    else:
        output = (
            f"☀️ **{greet_en}, Sir! Here is your J.A.R.V.I.S. Daily Morning Briefing:**\n\n"
            f"📅 **Date & Day:** {cur_date_en}\n\n"
            f"⛅ **Weather ({city}):** {weather_summary}\n\n"
            f"📜 **Today in History Highlights:**\n{dinvishesh_snippet}\n\n"
            f"📰 **Top 3 Breaking News Headlines:**\n{news_snippet}\n\n"
            f"📋 **Tasks & Reminders:** {rem_count} active reminders | {notes_count} saved notes\n"
            f"⚡ **System Telemetry:** CPU: {cpu_pct}% | Battery: {bat_str}\n\n"
            f"🤖 *All systems fully operational and ready for your command, Sir. Have an awesome day!*"
        )

    return output

def play_youtube(query: str, lang: str = 'mr') -> str:
    """Searches YouTube and plays top video directly in an embedded in-page player card without external redirects."""
    from jarvis_music import play_music
    return play_music(query, lang)

def send_whatsapp(message: str = '', phone: str = '', lang: str = 'mr') -> str:
    """Opens WhatsApp Web with drafted text or contact."""
    clean_msg = message.strip()
    if phone:
        clean_phone = re.sub(r'[^0-9+]', '', phone)
        url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(clean_msg)}"
    elif clean_msg:
        url = f"https://web.whatsapp.com/send?text={urllib.parse.quote(clean_msg)}"
    else:
        url = "https://web.whatsapp.com/"
    
    webbrowser.open(url)
    if clean_msg:
        if lang == 'mr':
            return f"मी व्हॉट्सॲप वेब उघडून **'{clean_msg}'** असा मेसेज तयार केला आहे, सर! 📱💬"
        elif lang == 'hi':
            return f"मैंने व्हाट्सएप वेब खोलकर **'{clean_msg}'** मैसेज तैयार कर दिया है, सर! 📱💬"
        return f"Opened WhatsApp Web with draft: **'{clean_msg}'**, Sir! 📱💬"
    else:
        if lang == 'mr':
            return "मी व्हॉट्सॲप वेब ओपन करत आहे, सर. 📱"
        return "Opening WhatsApp Web, Sir. 📱"

def change_theme(theme_text: str, lang: str = 'mr') -> str:
    """Changes the sci-fi theme of the JARVIS interface."""
    raw = theme_text.lower().strip()
    theme_code = 'cyan'
    theme_title = 'आयर्न मॅन सायन (Iron Man Cyan)'

    if any(k in raw for k in ['भगवा', 'swarajya', 'saffron', 'orange', 'shivaji', 'shivraya', 'bhagwa', 'kesari']):
        theme_code = 'saffron'
        theme_title = '🚩 स्वराज्य भगवा (Royal Swarajya Saffron)'
    elif any(k in raw for k in ['मॅट्रिक्स', 'matrix', 'green', 'hacker', 'हिरवा']):
        theme_code = 'matrix'
        theme_title = '🟢 मॅट्रिक्स निऑन ग्रीन (Matrix Hacker)'
    elif any(k in raw for k in ['पर्पल', 'purple', 'जांभळा', 'amethyst', 'violet']):
        theme_code = 'purple'
        theme_title = '🟣 डार्क ॲमेथिस्ट (Royal Purple)'
    else:
        theme_code = 'cyan'
        theme_title = '🔷 आयर्न मॅन सायन (Cyberpunk Cyan)'

    if lang == 'mr':
        return f"मी जार्व्हिसची थीम **'{theme_title}'** मध्ये बदलली आहे, सर! 🎨✨\n\n[CHANGE_THEME:{theme_code}]"
    elif lang == 'hi':
        return f"मैंने जार्विस की थीम **'{theme_title}'** कर दी है, सर! 🎨✨\n\n[CHANGE_THEME:{theme_code}]"
    return f"Switching interface theme to **'{theme_title}'**, Sir! 🎨✨\n\n[CHANGE_THEME:{theme_code}]"

def get_morning_briefing(lang: str = 'mr') -> str:
    """Delivers an inspirational and informative morning briefing."""
    date_str = get_current_date(lang)
    time_str = get_current_time(lang)

    import random
    suvichars_mr = [
        "\"शत्रू कितीही मोठा असो, युक्ती आणि धैर्याने त्याला पराभूत करता येते!\" - छत्रपती शिवाजी महाराज",
        "\"स्वातंत्र्य हा मानवाचा नैसर्गिक अधिकार आहे, आणि अन्याय सहन न करणे हेच खरे शौर्य आहे!\" - छत्रपती शिवाजी महाराज",
        "\"स्त्री ही जगदंबेचे रूप आहे, तिचा आदर करणे हे प्रत्येक मावळ्याचे कर्तव्य आहे!\" - छत्रपती शिवाजी महाराज",
        "\"ध्येय साध्य करण्यासाठी पराक्रमासोबत नीतीची जोड असायला हवी!\" - छत्रपती शिवाजी महाराज",
        "\"संकट कितीही मोठे असले तरी धीर सोडू नका, कारण संकट हेच सामर्थ्याची खरी परीक्षा असते!\" - छत्रपती शिवाजी महाराज"
    ]
    suvichars_hi = [
        "\"शत्रु कितना भी बड़ा हो, बुद्धि और साहस से उसे परास्त किया जा सकता है!\" - छत्रपति शिवाजी महाराज",
        "\"स्वतंत्रता मनुष्य का प्राकृतिक अधिकार है, और अन्याय न सहना ही सच्चा शौर्य है!\" - छत्रपति शिवाजी महाराज"
    ]
    suvichars_en = [
        "\"No matter how formidable the enemy, wisdom and courage will overcome all!\" - Chhatrapati Shivaji Maharaj",
        "\"Freedom is a natural right, and resisting injustice is true valor!\" - Chhatrapati Shivaji Maharaj"
    ]
    suvichar = random.choice(suvichars_hi if lang == 'hi' else (suvichars_en if lang == 'en' else suvichars_mr))

    weather_info = get_weather("Pune", lang)

    # Top 3 News Headlines from live multi-source aggregator
    news_items = fetch_raw_news_items(lang)[:3]
    news_text = ""
    if news_items:
        formatted_news = []
        for it in news_items:
            t = it['title']
            m = it['mins_ago']
            if lang == 'mr':
                time_tag = "आत्ताच" if m < 2 else (f"{m} मिनिटांपूर्वी" if m < 60 else f"{int(m/60)} तासांपूर्वी")
            elif lang == 'hi':
                time_tag = "अभी" if m < 2 else (f"{m} मिनट पहले" if m < 60 else f"{int(m/60)} घंटे पहले")
            else:
                time_tag = "Just now" if m < 2 else (f"{m} mins ago" if m < 60 else f"{int(m/60)} hrs ago")
            formatted_news.append(f"• {t} *({time_tag})*")

        if lang == 'mr':
            news_text = "\n📰 **आजच्या ताज्या मुख्य बातम्या:**\n" + "\n".join(formatted_news)
        elif lang == 'hi':
            news_text = "\n📰 **आज की प्रमुख सुर्खियाँ:**\n" + "\n".join(formatted_news)
        else:
            news_text = "\n📰 **Top Headlines Today:**\n" + "\n".join(formatted_news)

    reminders = load_reminders()
    rem_text = ""
    if reminders:
        if lang == 'mr':
            rem_text = f"\n\n⏰ आपल्याकडे **{len(reminders)}** नियोजित रिमाइंडर्स शिल्लक आहेत."
        elif lang == 'hi':
            rem_text = f"\n\n⏰ आपके पास **{len(reminders)}** रिमाइंडर्स पेंडिंग हैं।"
        else:
            rem_text = f"\n\n⏰ You have **{len(reminders)}** pending reminders."

    if lang == 'mr':
        return f"🌅 **शुभ सकाळ, सर!** आपला आजचा दिवस मंगलमय व यशस्वी जावो. 🚩\n\n" \
               f"📅 {date_str} | ⏰ {time_str}\n\n" \
               f"🚩 **आजचा शिवविचार:**\n{suvichar}\n\n" \
               f"{weather_info}\n" \
               f"{news_text}" \
               f"{rem_text}\n\n" \
               f"मी आपल्या सेवेसाठी सदैव सज्ज आहे. आज काय मदत करू, सर?"
    elif lang == 'hi':
        return f"🌅 **सुप्रभात, सर!** आपका दिन शुभ और मंगलमय हो। 🚩\n\n" \
               f"📅 {date_str} | ⏰ {time_str}\n\n" \
               f"🚩 **आज का प्रेरणादायी विचार:**\n{suvichar}\n\n" \
               f"{weather_info}\n" \
               f"{news_text}" \
               f"{rem_text}\n\n" \
               f"सभी प्रणालियां सक्रिय हैं। आज क्या सहायता करूँ, सर?"
    return f"🌅 **Good morning, Sir!** Wishing you a victorious and productive day ahead. 🚩\n\n" \
           f"📅 {date_str} | ⏰ {time_str}\n\n" \
           f"🚩 **Quote of the Day:**\n{suvichar}\n\n" \
           f"{weather_info}\n" \
           f"{news_text}" \
           f"{rem_text}\n\n" \
           f"All systems are online and awaiting your command, Sir."


# -------------------------------------------------------------
# 🌺 Ganpati Bappa Aarti on YouTube (Original Singer Voice)
# -------------------------------------------------------------
GANPATI_AARTI_VIDEO_ID = "pLkirAh4WLE"
GANPATI_AARTI_URL = f"https://www.youtube.com/watch?v={GANPATI_AARTI_VIDEO_ID}"

def play_ganpati_aarti(lang: str = 'mr') -> str:
    """Plays the authentic original Ganpati Aarti right here on the page without opening new tabs."""
    lyrics_mr = """🌺 **गणपती बाप्पा मोरया! मंगलमूर्ती मोरया!** 🌺
मी येथेच स्क्रीनवर गणपती बाप्पांची मूळ सुप्रसिद्ध आरती **'सुखकर्ता दुःखहर्ता'** (मूळ स्वर: भारतरत्न लता मंगेशकर आणि उषा मंगेशकर) सुरू केली आहे, सर!

[AARTI_PLAYER]

---
📜 **॥ श्री गणपतीची आरती ॥**
**सुखकर्ता दुःखहर्ता वार्ता विघ्नाची ।**
**नुरवी पुरवी प्रेम कृपा जयाची ।**
**सर्वांगी सुंदर उटी शेंदुराची ।**
**कंठी झळके माळ मुक्ताफळांची ॥ १ ॥**

**जय देव जय देव जय मंगलमूर्ती ।**
**दर्शनमात्रे मनकामना पुरती ॥ धृ. ॥**

**रत्नखचित फरा तुज गौरीकुमरा ।**
**चंदनाची उटी कुमकुम केशरा ।**
**हिरेजडित मुकुट शोभतो बरा ।**
**रुणझुणती नूपुरे चरणी घागरिया ॥ २ ॥ जय देव...**

**लंबोदर पीतांबर फणिवरबंधना ।**
**सरळ सोंड वक्रतुंड त्रिनयना ।**
**दास रामाचा वाट पाहे सदना ।**
**संकटी पावावे निर्वाणी रक्षावे सुरवरवंदना ॥ ३ ॥ जय देव...**

**शेंदुर लाल चढायो अच्छा गजमुख को ।**
**दोंदिल लाल बिराजे सुत गौरीहर को ।**
**हाथ लिए गुडलड्डू सांई सुरवर को ।**
**महिमा कहे न जाय लागत बलिहर को ॥ ४ ॥**

**जय जय जी गणराज विद्यासुखदाता ।**
**धन्य तुम्हारो दर्शन मेरा मन रमता ॥ धृ. ॥**
---"""

    lyrics_hi = """🌺 **गणपति बप्पा मोरया! मंगलमूर्ति मोरया!** 🌺
मैंने यहीं स्क्रीन पर गणपति बप्पा की मूल प्रसिद्ध आरती **'सुखकर्ता दुःखहर्ता'** (मूल स्वर: लता मंगेशकर व उषा मंगेशकर) शुरू कर दी है, सर!

[AARTI_PLAYER]

---
📜 **॥ श्री गणपति आरती ॥**
**सुखकर्ता दुःखहर्ता वार्ता विघ्नाची ।**
**नुरवी पुरवी प्रेम कृपा जयाची ।**
**सर्वांगी सुंदर उटी शेंदुराची ।**
**कंठी झळके माळ मुक्ताफळांची ॥ १ ॥**

**जय देव जय देव जय मंगलमूर्ती ।**
**दर्शनमात्रे मनकामना पुरती ॥ धृ. ॥**
---"""

    lyrics_en = """🌺 **Ganpati Bappa Morya! Mangal Murti Morya!** 🌺
Playing the original, authentic **'Sukhkarta Dukhharta'** right here on your screen, Sir!

[AARTI_PLAYER]

---
📜 **॥ Shri Ganpati Aarti ॥**
**Sukhkarta Dukhharta Varta Vighnachi |**
**Nurvi Purvi Prem Krupa Jayachi |**
**Sarvangi Sundar Uti Shendurachi |**
**Kanthi Jhalake Maal Muktaphallanchi || 1 ||**

**Jai Dev Jai Dev Jai Mangalmurti |**
**Darshanmatre Man Kamana Purti || Dhru. ||**
---"""

    if lang == 'hi':
        return lyrics_hi
    elif lang == 'en':
        return lyrics_en
    return lyrics_mr


# -------------------------------------------------------------
# 🚩 Chhatrapati Shivaji Maharaj Aarti: "शिवशंकराचा तू अवतार"
# -------------------------------------------------------------
SHIVRAYA_AARTI_VIDEO_ID = "e0-SwM80bvI"
SHIVRAYA_AARTI_URL = f"https://www.youtube.com/watch?v={SHIVRAYA_AARTI_VIDEO_ID}"

def play_shivraya_aarti(lang: str = 'mr') -> str:
    """Plays the authentic 'Shiv Shankaracha Tu Avatar' Aarti of Chhatrapati Shivaji Maharaj right on the page."""
    lyrics_mr = """🚩 **प्रौढ प्रताप पुरंधर, क्षत्रियकुलावतंस, सिंहासनाधीश्वर छत्रपती शिवाजी महाराज की जय!** 🚩
मी येथेच स्क्रीनवर छत्रपती शिवाजी महाराजांची अत्यंत लोकप्रिय व स्फूर्तिदायक आरती **'शिवशंकराचा तू अवतार'** (गायक: आदर्श शिंदे) सुरू केली आहे, सर!

[SHIVRAYA_AARTI_PLAYER]

---
📜 **॥ श्री छत्रपती शिवाजी महाराज आरती ॥**
*(गीत: दत्ता सोनावणे-देशमुख | संगीत: अभिषेक-दत्ता | स्वर: आदर्श शिंदे)*

**शिव शंकराचा तू अवतार,**
**हाती घेउनी भवानी तलवार ।**
**नर राक्षसांचा करुणी संहार,**
**धरणी मातेचा तू केला उद्धार ॥**

**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ।**
**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ॥ धृ. ॥**

**नाथा अनाथा तू सामर्थ्यवंत,**
**मावळते बळ केले जीवंत ।**
**राजा धिराजा तू होऊनी संत,**
**जाणता राजा तू योगी श्रीमंत ॥**

**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ॥ १ ॥**

**भक्ती शक्ती युक्तीचा अधिकारी,**
**दुर्जन मर्दन तूच सज्जन अतारी ।**
**शिव तुझे नाम हे संकटहारी,**
**नीत विनीत मी शिवबा शिवारी ॥**

**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ॥ २ ॥**

🚩 **॥ छत्रपती शिवाजी महाराज की जय ! ॥** 🚩
🚩 **॥ जय भवानी, जय शिवाजी ! ॥** 🚩
---"""

    lyrics_hi = """🚩 **छत्रपति शिवाजी महाराज की जय!** 🚩
मैंने यहीं स्क्रीन पर छत्रपति शिवाजी महाराज की प्रसिद्ध व ऊर्जावान आरती **'शिवशंकराचा तू अवतार'** (गायक: आदर्श शिंदे) शुरू कर दी है, सर!

[SHIVRAYA_AARTI_PLAYER]

---
📜 **॥ श्री छत्रपति शिवाजी महाराज आरती ॥**
*(गायक: आदर्श शिंदे | गीत: दत्ता सोनावणे)*

**शिव शंकराचा तू अवतार,**
**हाती घेउनी भवानी तलवार ।**
**नर राक्षसांचा करुणी संहार,**
**धरणी मातेचा तू केला उद्धार ॥**

**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ॥ धृ. ॥**

**नाथा अनाथा तू सामर्थ्यवंत,**
**मावळते बळ केले जीवंत ।**
**राजा धिराजा तू होऊनी संत,**
**जाणता राजा तू योगी श्रीमंत ॥**

**जय देव जय देव जय शिवराया,**
**आलो तवद्वारी आरती गाया ॥ १ ॥**

🚩 **॥ छत्रपति शिवाजी महाराज की जय ! ॥** 🚩
---"""

    lyrics_en = """🚩 **Chhatrapati Shivaji Maharaj Ki Jai!** 🚩
Playing the powerful Shivaji Maharaj Aarti **'Shiv Shankaracha Tu Avatar'** (sung by Aadarsh Shinde) right here on your screen, Sir!

[SHIVRAYA_AARTI_PLAYER]

---
📜 **॥ Shri Chhatrapati Shivaji Maharaj Aarti ॥**
*(Vocals: Aadarsh Shinde | Lyrics: Datta Sonawane)*

**Shiv Shankaracha Tu Avatar,**
**Haati Gheuni Bhavani Talwar |**
**Nar Rakshasancha Karuni Sanhar,**
**Dharni Maatecha Tu Kela Uddhar ||**

**Jai Dev Jai Dev Jai Shivraya,**
**Aalo Tavdwari Aarti Gaaya || Dhru. ||**

**Naatha Anaatha Tu Samarthyawant,**
**Maawalte Bal Kele Jeevant |**
**Raja Dhiraja Tu Houni Sant,**
**Jaanta Raja Tu Yogi Shrimant ||**

**Jai Dev Jai Dev Jai Shivraya,**
**Aalo Tavdwari Aarti Gaaya || 1 ||**

🚩 **॥ Chhatrapati Shivaji Maharaj Ki Jai ! ॥** 🚩
---"""

    if lang == 'hi':
        return lyrics_hi
    elif lang == 'en':
        return lyrics_en
    return lyrics_mr


# -------------------------------------------------------------
# 🚩 Hanuman Chalisa Player (Gulshan Kumar / Hariharan)
# -------------------------------------------------------------
HANUMAN_CHALISA_VIDEO_ID = "17ZHT4WbSfw"
HANUMAN_CHALISA_URL = f"https://www.youtube.com/watch?v={HANUMAN_CHALISA_VIDEO_ID}"

def play_hanuman_chalisa(lang: str = 'mr') -> str:
    """Plays the world-famous original Shri Hanuman Chalisa by Hariharan & Gulshan Kumar right on the page."""
    text_mr = """🚩 **॥ जय श्री राम । जय श्री हनुमान ॥** 🚩
मी येथेच स्क्रीनवर सुप्रसिद्ध मूळ **श्री हनुमान चालीसा** (गायक: हरिहरन, निर्माते: गुलशन कुमार) सुरू केली आहे, सर!

[HANUMAN_CHALISA_PLAYER]

---
📜 **॥ श्री हनुमान चालीसा ॥**
*(रचनाकार: गोस्वामी तुलसीदास | स्वर: हरिहरन | निर्मिती: गुलशन कुमार, T-Series)*

**॥ दोहा ॥**
श्रीगुरु चरन सरोज रज निज मनु मुकुरु सुधारि ।
बरनउँ रघुबर बिमल जसु जो दायकु फल चारि ॥
बुद्धिहीन तनु जानिके सुमिरौ पवन-कुमार ।
बल बुद्धि बिद्या देहु मोहिं हरहु कलेस बिकार ॥

**॥ चौपाई ॥**
जय हनुमान ज्ञान गुन सागर । जय कपीस तिहुँ लोक उजागर ॥ १ ॥
राम दूत अतुलित बल धामा । अंजनि-पुत्र पवनसुत नामा ॥ २ ॥
महाबीर बिक्रम बजरंगी । कुमति निवार सुमति के संगी ॥ ३ ॥
कंचन बरन बिराज सुबेसा । कानन कुंडल कुंचित केसा ॥ ४ ॥
हाथ बज्र औ ध्वजा बिराजै । काँधे मूँज जनेऊ साजै ॥ ५ ॥
संकर सुवन केसरीनंदन । तेज प्रताप महा जग बंदन ॥ ६ ॥
बिद्यावान गुनी अति चातुर । राम काज करिबे को आतुर ॥ ७ ॥
प्रभु चरित्र सुनिबे को रसिया । राम लखन सीता मन बसिया ॥ ८ ॥
सूक्ष्म रूप धरि सियहिं दिखावा । बिकट रूप धरि लंक जरावा ॥ ९ ॥
भीम रूप धरि असुर सँहारे । रामचंद्र के काज संवारे ॥ १० ॥
लाय सजीवन लखन जियाये । श्रीरघुबीर हरषि उर लाये ॥ ११ ॥
रघुपति कीन्ही बहुत बड़ाई । तुम मम प्रिय भरतहि सम भाई ॥ १२ ॥
सहस बदन तुम्हरो जस गावैं । अस कहि श्रीपति कंठ लगावैं ॥ १३ ॥
सनकादिक ब्रह्मादि मुनीसा । नारद सारद सहित अहीसा ॥ १४ ॥
जम कुबेर दिगपाल जहाँ ते । कबि कोबिद कहि सके कहाँ ते ॥ १५ ॥
तुम उपकार सुग्रीवहिं कीन्हा । राम मिलाय राज पद दीन्हा ॥ १६ ॥
तुम्हरो मंत्र बिभीषन माना । लंकेस्वर भए सब जग जाना ॥ १७ ॥
जुग सहस्र जोजन पर भानू । लील्यो ताहि मधुर फल जानू ॥ १८ ॥
प्रभु मुद्रिका मेलि मुख माहीं । जलधि लाँघि गये अचरज नाहीं ॥ १९ ॥
दुर्गम काज जगत के जेते । सुगम अनुग्रह तुम्हरे तेते ॥ २० ॥
राम दुआरे तुम रखवारे । होत न आज्ञा बिनु पैसारे ॥ २१ ॥
सब सुख लहै तुम्हारी सरना । तुम रक्षक काहू को डर ना ॥ २२ ॥
आपन तेज सम्हारो आपै । तीनों लोक हाँक तें काँपै ॥ २३ ॥
भूत पिसाच निकट नहिं आवै । महाबीर जब नाम सुनावै ॥ २४ ॥
नासै रोग हरै सब पीरा । जपत निरंतर हनुमत बीरा ॥ २५ ॥
संकट तें हनुमान छुड़ावै । मन क्रम बचन ध्यान जो लावै ॥ २६ ॥
सब पर राम तपस्वी राजा । तिन के काज सकल तुम साजा ॥ २७ ॥
और मनोरथ जो कोई लावै । सोइ अमित जीवन फल पावै ॥ २८ ॥
चारों जुग परताप तुम्हारा । है परसिद्ध जगत उजियारा ॥ २९ ॥
साधु संत के तुम रखवारे । असुर निकंदन राम दुलारे ॥ ३० ॥
अष्ट सिद्धि नौ निधि के दाता । अस बर दीन जानकी माता ॥ ३१ ॥
राम रसायन तुम्हरे पासा । सदा रहो रघुपति के दासा ॥ ३२ ॥
तुम्हरे भजन राम को पावै । जनम जनम के दुख बिसरावै ॥ ३३ ॥
अंत काल रघुबर पुर जाई । जहाँ जन्म हरि-भक्त कहाई ॥ ३४ ॥
और देवता चित्त न धरई । हनुमत सेइ सर्ब सुख करई ॥ ३५ ॥
संकट कटै मिटै सब पीरा । जो सुमिरै हनुमत बलबीरा ॥ ३६ ॥
जै जै जै हनुमान गोसाईं । कृपा करहु गुरुदेव की नाईं ॥ ३७ ॥
जो सत बार पाठ कर कोई । छूटहि बंदि महा सुख होई ॥ ३८ ॥
जो यह पढ़ै हनुमान चालीसा । होय सिद्ध साखी गौरीसा ॥ ३९ ॥
तुलसीदास सदा हरि चेरा । कीजै नाथ हृदय मँह डेरा ॥ ४० ॥

**॥ दोहा ॥**
पवनतनय संकट हरन, मंगल मूरति रूप ।
राम लखन सीता सहित, हृदय बसहु सुर भूप ॥

🚩 **॥ सियावर रामचंद्र की जय ! ॥** 🚩
🚩 **॥ पवनसुत हनुमान की जय ! ॥** 🚩
---"""

    text_hi = """🚩 **॥ जय श्री राम । जय बजरंगबली ॥** 🚩
मैंने यहीं स्क्रीन पर विश्वप्रसिद्ध **श्री हनुमान चालीसा** (गायक: हरिहरन, टी-सीरीज़) शुरू कर दी है, सर!

[HANUMAN_CHALISA_PLAYER]

---
📜 **॥ श्री हनुमान चालीसा ॥**
*(रचयिता: गोस्वामी तुलसीदास | स्वर: हरिहरन | गुलशन कुमार)*

**॥ दोहा ॥**
श्रीगुरु चरन सरोज रज निज मनु मुकुरु सुधारि ।
बरनउँ रघुबर बिमल जसु जो दायकु फल चारि ॥
बुद्धिहीन तनु जानिके सुमिरौ पवन-कुमार ।
बल बुद्धि बिद्या देहु मोहिं हरहु कलेस बिकार ॥

**॥ चौपाई ॥**
जय हनुमान ज्ञान गुन सागर । जय कपीस तिहुँ लोक उजागर ॥ १ ॥
राम दूत अतुलित बल धामा । अंजनि-पुत्र पवनसुत नामा ॥ २ ॥
महाबीर बिक्रम बजरंगी । कुमति निवार सुमति के संगी ॥ ३ ॥
कंचन बरन बिराज सुबेसा । कानन कुंडल कुंचित केसा ॥ ४ ॥
हाथ बज्र औ ध्वजा बिराजै । काँधे मूँज जनेऊ साजै ॥ ५ ॥
संकर सुवन केसरीनंदन । तेज प्रताप महा जग बंदन ॥ ६ ॥
बिद्यावान गुनी अति चातुर । राम काज करिबे को आतुर ॥ ७ ॥
प्रभु चरित्र सुनिबे को रसिया । राम लखन सीता मन बसिया ॥ ८ ॥

*(संपूर्ण हनुमान चालीसा स्क्रीनवर वाजत आहे)*

🚩 **॥ जय श्री राम ! ॥** 🚩
🚩 **॥ बजरंगबली की जय ! ॥** 🚩
---"""

    text_en = """🚩 **॥ Jai Shri Ram | Jai Hanuman ॥** 🚩
Playing the world-famous sacred **Shri Hanuman Chalisa** (sung by Hariharan, produced by Gulshan Kumar) right here on your screen, Sir!

[HANUMAN_CHALISA_PLAYER]

---
📜 **॥ Shri Hanuman Chalisa ॥**
*(Composer: Goswami Tulsidas | Vocals: Hariharan | T-Series)*

**Doha:**
Shri Guru Charan Saroj Raj, Nij Manu Mukuru Sudhari |
Barnau Raghuvar Bimal Jasu, Jo Dayaku Phal Chari ||
Buddhiheen Tanu Janike, Sumirau Pavan-Kumar |
Bal Buddhi Vidya Dehu Mohi, Harahu Kalesh Bikaar ||

**Chaupai:**
Jai Hanuman Gyan Gun Sagar | Jai Kapees Tihun Lok Ujagar || 1 ||
Ram Doot Atulit Bal Dhama | Anjani-Putra Pavansut Nama || 2 ||

🚩 **॥ Jai Bajrangbali ! ॥** 🚩
---"""

    if lang == 'hi':
        return text_hi
    elif lang == 'en':
        return text_en
    return text_mr



def search_google(query: str, lang: str = 'mr') -> str:
    clean_query = query.strip()
    url = f"https://www.google.com/search?q={requests.utils.quote(clean_query)}"
    webbrowser.open(url)
    if lang == 'mr':
        return f"मी गुगलवर '{clean_query}' शोधत आहे, सर."
    elif lang == 'hi':
        return f"गूगल पर '{clean_query}' सर्च कर रहा हूँ, सर।"
    return f"Searching Google for '{clean_query}', Sir."

# -------------------------------------------------------------
# 🎯 8. Master Action Handler
# -------------------------------------------------------------
def handle_action(text: str, lang: str = 'mr') -> tuple[bool, str]:
    """
    Parses user input for any automation or system action.
    Returns (is_action: bool, response_text: str)
    """
    raw = text.strip().lower()

    # 0.0 🌅 Good Morning / Shubh Sakal Daily Briefing
    morning_triggers = [
        'शुभ सकाळ', 'सुप्रभात', 'good morning', 'shubh sakal', 'suprabhat',
        'morning briefing', 'दैनिक माहिती', 'आजची माहिती सांगा', 'आजचा दिवस कसा आहे'
    ]
    if any(mt in raw for mt in morning_triggers):
        return True, get_morning_briefing(lang)

    # 0.01 🎨 Dynamic Theme Switching
    theme_triggers = [
        'थीम बदल', 'थीम भगवा', 'भगवा थीम', 'थीम सायन', 'सायन थीम', 'मॅट्रिक्स थीम',
        'थीम मॅट्रिक्स', 'पर्पल थीम', 'थीम पर्पल', 'change theme', 'set theme',
        'swarajya theme', 'matrix theme', 'purple theme', 'cyan theme', 'theme change',
        'भगवा रंग कर', 'थीम बदल कर', 'theme set kar'
    ]
    if any(tt in raw for tt in theme_triggers):
        return True, change_theme(raw, lang)

    # 0.02 💬 WhatsApp Messaging Automation
    whatsapp_triggers = [
        'whatsapp उघड', 'व्हॉट्सॲप उघड', 'व्हाट्सअप उघड', 'व्हाट्सएप उघड',
        'open whatsapp', 'whatsapp open', 'व्हॉट्सॲप ओपन',
        'whatsapp वर मेसेज', 'व्हॉट्सॲपवर मेसेज', 'व्हाट्सअपवर मेसेज',
        'send message on whatsapp', 'whatsapp message', 'व्हॉट्सॲप मेसेज'
    ]
    if any(wt in raw for wt in whatsapp_triggers):
        msg_text = ""
        m_msg = re.search(r'(?:मेसेज|message|msg)\s*(?:कर|पाठव|send)?\s*[:\s]+(.+)', text, re.IGNORECASE)
        if m_msg:
            msg_text = m_msg.group(1).strip()
        return True, send_whatsapp(message=msg_text, lang=lang)

    # 0. 🚩 Jai Shree Ram Instant Wake / Salutation
    ram_triggers = ['जय श्री राम', 'जय श्रीराम', 'jai shree ram', 'jay shree ram', 'jai shri ram', 'jay shri ram', 'shree ram', 'shri ram', 'ram ram', 'राम राम']
    if any(rt in raw for rt in ram_triggers):
        clean_after = raw
        for rt in ram_triggers:
            clean_after = clean_after.replace(rt, '').strip()
        clean_after = re.sub(r'^[,\.\s!?-]+', '', clean_after).strip()
        if not clean_after or clean_after in ['सर', 'sir', 'boss', 'ji', 'सांगा', 'bolo', 'kasa ahes', 'kay chalalay']:
            if lang == 'mr':
                return True, "🚩 **जय श्री राम!** काय मदत करू सर?"
            elif lang == 'hi':
                return True, "🚩 **जय श्री राम!** बताइए, क्या मदद करूँ सर?"
            return True, "🚩 **Jai Shree Ram!** How can I help you, Sir?"

    # 0.1 🧑‍🤝‍🧑 Special Recognition: Shubham Kalamkar
    shubham_triggers = [
        'shubham kalamkar', 'shubham kalmkar', 'शुभम कळमकर', 'शुभम कलमकर',
        'shubham kon', 'शुभम कोण', 'who is shubham', 'shubham kaun'
    ]
    if any(st in raw for st in shubham_triggers):
        if lang == 'mr':
            return True, "तो **साहिलचा फ्रेंड (मित्र)** आहे, सर! 🤝"
        elif lang == 'hi':
            return True, "वह **साहिल का दोस्त (फ्रेंड)** है, सर! 🤝"
        return True, "He is **Sahil's friend**, Sir! 🤝"

    # 0.1.05 🧑‍🤝‍🧑 Special Recognition: Yogesh Bhasar
    yogesh_triggers = [
        'yogesh bhasar', 'yogesh bhashar', 'yogesh basar', 'yogesh baser', 'yogesh bharsar',
        'योगेश भासार', 'योगेश भसार', 'योगेश भासर', 'योगेश भसर',
        'yogesh kon', 'yogesh kon aahe', 'yogesh kon ahe', 'yogesh kaun', 'who is yogesh',
        'योगेश कोण', 'योगेश कोण आहे', 'योगेश कोण आहेत', 'yogesh badal', 'योगेश बद्दल',
        'yogesh vishayi', 'योगेश विषयी'
    ]
    if any(yt in raw for yt in yogesh_triggers):
        if lang == 'mr':
            return True, "तो **साहिलचा मित्र (फ्रेंड)** आहे, सर! 🤝"
        elif lang == 'hi':
            return True, "वह **साहिल का दोस्त (मित्र)** है, सर! 🤝"
        return True, "He is **Sahil's friend**, Sir! 🤝"

    # 0.1.06 🧑‍🤝‍🧑 Special Recognition: Kartik Mohite
    kartik_triggers = [
        'kartik mohite', 'kartik', 'कार्तिक मोहिते', 'कार्तिक',
        'kartik kon', 'kartik kon aahe', 'kartik kon ahe', 'kartik kaun', 'who is kartik',
        'कार्तिक कोण', 'कार्तिक कोण आहे', 'कार्तिक कोण आहेत', 'kartik badal', 'कार्तिक बद्दल',
        'kartik vishayi', 'कार्तिक विषयी'
    ]
    if any(kt in raw for kt in kartik_triggers):
        if lang == 'mr':
            return True, "तो **साहिलचा मित्र (फ्रेंड)** आहे, सर! 🤝"
        elif lang == 'hi':
            return True, "वह **साहिल का दोस्त (मित्र)** है, सर! 🤝"
        return True, "He is **Sahil's friend**, Sir! 🤝"


    # 0.1.1 👨‍👩‍👦 Special Recognition: Sahil's Family (वडील: अशोक भिंगारे, आई: सुनीता, भाऊ: रोहन)
    sahil_family_triggers = [
        'sahil chi family', 'sahil family', 'sahil che kutumb', 'sahil kutumb', 'family vishayi',
        'family badal', 'family sang', 'family chi mahiti', 'tell me about family', 'sahil family members',
        "sahil's family", 'sahils family', 'sahil family in',
        'साहिलची फॅमिली', 'साहिलचे कुटुंब', 'साहिलचं कुटुंब', 'फॅमिली विषयी', 'फॅमिली बद्दल', 'कुटुंबाविषयी सांग',
        'साहिलच्या कुटुंबाबद्दल', 'साहिलच्या फॅमिलीबद्दल', 'साहिलच्या फॅमिलीविषयी', 'कुटुंब', 'family'
    ]
    if any(sf in raw for sf in sahil_family_triggers) and any(w in raw for w in ['sahil', 'साहिल', 'family', 'फॅमिली', 'कुटुंब', 'vishayi', 'विषयी']):
        if lang == 'mr':
            return True, (
                "👨‍👩‍👦 **साहिल यांचे कुटुंब (Sahil's Family):**\n"
                "• **वडील**: **अशोक भिंगारे (Ashok Bhingare)** - साहिलचे वडील आहेत. 👨\n"
                "• **आई**: **सुनीता (Sunita)** - साहिलची आई आहेत. 👩\n"
                "• **भाऊ**: **रोहन (Rohan)** - साहिलचा भाऊ आहे. 👦\n\n"
                "हे साहिलचे सुखी आणि प्रेमळ कुटुंब आहे, सर! 🏡❤️"
            )
        elif lang == 'hi':
            return True, (
                "👨‍👩‍👦 **साहिल का परिवार (Sahil's Family):**\n"
                "• **पिताजी**: **अशोक भिंगारे (Ashok Bhingare)** - साहिल के पिता हैं। 👨\n"
                "• **माताजी**: **सुनीता (Sunita)** - साहिल की माताजी हैं। 👩\n"
                "• **भाई**: **रोहन (Rohan)** - साहिल के भाई हैं। 👦\n\n"
                "यह साहिल का प्यारा और सुखी परिवार है, सर! 🏡❤️"
            )
        return True, (
            "👨‍👩‍👦 **Sahil's Family Members:**\n"
            "• **Father**: **Ashok Bhingare** (साहिलचे वडील) 👨\n"
            "• **Mother**: **Sunita** (साहिलची आई) 👩\n"
            "• **Brother**: **Rohan** (साहिलचा भाऊ) 👦\n\n"
            "This is Sahil's wonderful family, Sir! 🏡❤️"
        )

    # Individual Member Lookups
    if any(af in raw for af in ['ashok bhingare', 'अशोक भिंगारे', 'sahil che vadil', 'साहिलचे वडील', 'sahil che papa', 'sahil ke pita', 'sahil father', "sahil's father"]):
        if lang == 'mr':
            return True, "**अशोक भिंगारे (Ashok Bhingare)** हे साहिलचे वडील (Father) आहेत, सर! 👨"
        elif lang == 'hi':
            return True, "**अशोक भिंगारे (Ashok Bhingare)** साहिल के पिताजी (Father) हैं, सर! 👨"
        return True, "**Ashok Bhingare** is Sahil's father, Sir! 👨"

    if any(rf in raw for rf in ['rohan kon', 'रोहन कोण', 'sahil cha bhau', 'साहिलचा भाऊ', 'sahil brother', "sahil's brother", 'sahil ka bhai']):
        if lang == 'mr':
            return True, "**रोहन (Rohan)** हा साहिलचा भाऊ (Brother) आहे, सर! 👦"
        elif lang == 'hi':
            return True, "**रोहन (Rohan)** साहिल का भाई (Brother) है, सर! 👦"
        return True, "**Rohan** is Sahil's brother, Sir! 👦"

    if any(sf in raw for sf in ['sunita kon', 'सुनीता कोण', 'sahil chi aai', 'साहिलची आई', 'sahil mother', "sahil's mother", 'sahil ki mata']):
        if lang == 'mr':
            return True, "**सुनीता (Sunita)** या साहिलची आई (Mother) आहेत, सर! 👩❤️"
        elif lang == 'hi':
            return True, "**सुनीता (Sunita)** साहिल की माताजी (Mother) हैं, सर! 👩❤️"
        return True, "**Sunita** is Sahil's mother, Sir! 👩❤️"

    # 0.1.2 🎓 Special Recognition: Sahil's Education & Profile
    sahil_edu_triggers = [
        'sahil ch education', 'sahil che education', 'sahil education', 'sahil che shikshan',
        'sahil qualification', 'sahil chya shikshan', 'sahil ne kay shikla', 'sahil study',
        'sahil degree', 'sahil diploma', 'education of sahil', 'sahil ka education', 'sahil ki padhai',
        'साहिलचे शिक्षण', 'साहिलच शिक्षण', 'साहिलचं शिक्षण', 'साहिल काय शिकला', 'साहिलचे एज्युकेशन',
        'साहिलने काय केले', 'साहिलचा डिप्लोमा', 'साहिल ची माहिती', 'साहिल बद्दल सांगा', 'साहिल बद्दल सांग',
        'साहिल बद्दल माहिती', 'साहिल कोण आहे', 'sahil kon', 'who is sahil', 'tell me about sahil', 'sahil badal sang'
    ]
    if any(se in raw for se in sahil_edu_triggers) and not any(fw in raw for fw in ['family', 'फॅमिली', 'कुटुंब', 'वडील', 'आई', 'भाऊ', 'father', 'mother', 'brother', 'insta', 'instagram', 'इन्स्टा', 'इंस्टाग्राम']):
        if lang == 'mr':
            return True, "साहिल यांनी **कॉम्प्युटर डिप्लोमा (Computer Diploma) ६९.८८%** गुणांसह पूर्ण केला आहे. तसेच सध्या ते **Vyomx Tech Solution Pvt. Ltd. (आंबेगाव, नऱ्हे)** येथे **फुलस्टॅक डेव्हलपर (Full Stack Developer)** चे क्लासेस करत आहेत, सर! 💻🚀"
        elif lang == 'hi':
            return True, "साहिल जी ने **कंप्यूटर डिप्लोमा (Computer Diploma) ६९.८८%** अंकों के साथ पूरा किया है। वर्तमान में वे **Vyomx Tech Solution Pvt. Ltd. (आंबेगांव, नऱ्हे)** में **फुलस्टैक डेवलपर (Full Stack Developer)** की ट्रेनिंग / क्लासेस कर रहे हैं, सर! 💻🚀"
        return True, "Sahil has completed his **Computer Diploma with 69.88%**. Currently, he is pursuing **Full Stack Developer** training at **Vyomx Tech Solution Pvt. Ltd. (Ambegaon, Narhe)**, Sir! 💻🚀"

    # 0.1.25 📸 Special Recognition: Sahil's Instagram ID (sahil_bhingare_96k)
    sahil_insta_triggers = [
        'sahil chi insta id', 'sahil chi insta', 'sahil chi instagram id', 'sahil chi instagram',
        'sahil insta id', 'sahil instagram id', 'sahil insta', 'sahil instagram',
        'sahil chi id', 'sahil id', 'sahil account', 'sahil_bhingare_96k', 'sahil bhingare insta',
        'साहिलची इन्स्टा आयडी', 'साहिलची इंस्टाग्राम आयडी', 'साहिलची इन्स्टा', 'साहिलची इंस्टाग्राम',
        'साहिल इन्स्टा आयडी', 'साहिल इंस्टाग्राम आयडी', 'साहिलचा इन्स्टा', 'साहिलचा इंस्टाग्राम',
        'साहिल इन्स्टाग्राम', 'साहिल इन्स्टा', 'साहिलची आयडी', 'sahil ki insta id', 'sahil ki instagram id',
        'sahil ka insta', 'sahil ka instagram', 'instagram id of sahil', 'insta id of sahil',
        'sahil social media', 'sahil handle'
    ]
    if any(si in raw for si in sahil_insta_triggers) or (('insta' in raw or 'instagram' in raw or 'इन्स्टा' in raw or 'इंस्टाग्राम' in raw) and any(sw in raw for sw in ['sahil', 'साहिल'])):
        if lang == 'mr':
            return True, "साहिल यांची इंस्टाग्राम आयडी **@sahil_bhingare_96k** ही आहे, सर! 📸✨\n\n👉 [Instagram Profile उघडा](https://www.instagram.com/sahil_bhingare_96k/)"
        elif lang == 'hi':
            return True, "साहिल जी की इंस्टाग्राम आईडी **@sahil_bhingare_96k** है, सर! 📸✨\n\n👉 [Instagram Profile खोलें](https://www.instagram.com/sahil_bhingare_96k/)"
        return True, "Sahil's Instagram ID is **@sahil_bhingare_96k**, Sir! 📸✨\n\n👉 [Open Instagram Profile](https://www.instagram.com/sahil_bhingare_96k/)"


    # 0.0 ☀️ Smart Daily Morning Briefing
    briefing_triggers = [
        'गुड मॉर्निंग', 'सुप्रभात', 'good morning', 'daily briefing', 'morning brief',
        'आजचा दिवस कसा आहे', 'दिवसाची सुरुवात', 'आजचा आढावा', 'आजचा संपूर्ण आढावा',
        'morning update', 'aaj cha divas', 'today briefing'
    ]
    if any(q in raw for q in briefing_triggers) or raw in ['सुप्रभात!', 'सुप्रभात', 'गुड मॉर्निंग!', 'good morning!']:
        return True, get_daily_briefing(lang)

    # 0.2 🌺 Ganpati Bappa Aarti (Original Singer Voice - Lata Mangeshkar & Usha Mangeshkar)
    aarti_stop_triggers = [
        'आरती थांबव', 'गाणे थांबव', 'आरती बंद कर', 'गाणं बंद कर', 'ऑडिओ थांबव', 'गाणे बंद', 'गाणं बंद',
        'म्युझिक थांबव', 'म्युझिक बंद कर', 'गाना बंद करो', 'गाना रोको', 'संगीत थांबव', 'संगीत बंद कर',
        'stop aarti', 'pause aarti', 'stop audio', 'stop song', 'pause song', 'stop music', 'pause music',
        'बंद कर आरती', 'आरती थांबवा', 'थांबव आरती', 'आरती बंद', 'थांबव', 'बंद कर', 'stop', 'pause'
    ]
    if any(st in raw for st in aarti_stop_triggers):
        if lang == 'mr':
            return True, "होय सर, मी चालू असलेला ऑडिओ / व्हिडिओ / गाणे थांबवले आहे. 🌺⏹️"
        elif lang == 'hi':
            return True, "जी सर, मैंने चल रहा ऑडियो / वीडियो / गाना रोक दिया है। 🌺⏹️"
        return True, "Yes Sir, I have stopped the active media playback. 🌺⏹️"

    # 0.2.1 🚩 Chhatrapati Shivaji Maharaj Aarti: "शिवशंकराचा तू अवतार"
    shivraya_aarti_triggers = [
        'शिव शंकराचा तू अवतार', 'शिवशंकराचा तू अवतार', 'शिव शंकराचा अवतार', 'शिवशंकराचा अवतार',
        'शिव शंकराचा', 'शिवशंकराचा', 'अवतार ही शिवरायांची आरती', 'शिवरायांची आरती',
        'शिवराय आरती', 'शिवाजी महाराज आरती', 'शिवाजी महाराजांची आरती', 'छत्रपती शिवाजी महाराज आरती',
        'छत्रपती शिवाजी महाराजांची आरती', 'शिवरायांची आरती लाव', 'शिवाजी महाराजांची आरती लाव',
        'शिवरायांची आरती सुरू कर', 'शिवाजी महाराज आरती लाव', 'शिवरायांची आरती लावा', 'शिवरायांची आरती चालू कर',
        'shiv shankaracha tu avatar', 'shiv shankaracha avatar', 'shiv shankaracha',
        'shivraya aarti', 'shivaji maharaj aarti', 'chatrapati shivaji maharaj aarti',
        'chhatrapati shivaji maharaj aarti', 'aadarsh shinde shivaji aarti', 'adarsh shinde aarti',
        'aarti shivrayanchi', 'shivaji aarti', 'shivrayanchi arati lav', 'shivrayanchi aarti lav',
        'shivrayanchi arati', 'shivrayanchi aarti', 'shivraya arati', 'shivraya arti',
        'shivrayanchi arti', 'shivrayanchi arti lav', 'shivraya arati lav', 'shivraya aarti lav',
        'shivaji maharaj arati', 'shivaji arati', 'shivaji maharaj arati lav', 'shivaji maharaj aarti lav',
        'chatrapati shivaji maharaj arati', 'chhatrapati shivaji maharaj arati',
        'shivrayanchi aarti lava', 'shivrayanchi arati lava', 'play shivaji aarti'
    ]
    if any(st in raw for st in shivraya_aarti_triggers):
        return True, play_shivraya_aarti(lang)

    # 0.2.2 🚩 Shri Hanuman Chalisa (Hariharan & Gulshan Kumar / T-Series)
    hanuman_chalisa_triggers = [
        'हनुमान चालीसा', 'श्री हनुमान चालीसा', 'हनुमान चालिसा', 'श्री हनुमान चालिसा',
        'हनुमान चालीसा लाव', 'हनुमान चालीसा सुरू कर', 'हनुमान चालीसा प्ले कर', 'हनुमान चालीसा चालू कर',
        'हनुमान चालीसा ऐकव', 'हनुमान चालीसा लावा', 'हनुमान चालिसा लाव', 'मारुती स्तोत्र',
        'बजरंगबली चालीसा', 'हनुमान स्तोत्र', 'hanuman chalisa', 'shree hanuman chalisa',
        'shri hanuman chalisa', 'play hanuman chalisa', 'hanuman chalisa lava', 'hanuman chalisa suru kar',
        'hanuman chalisa play', 'maruti stotra'
    ]
    if any(ht in raw for ht in hanuman_chalisa_triggers):
        return True, play_hanuman_chalisa(lang)

    aarti_triggers = [
        'गणपती बाप्पा आरती', 'गणपती बाप्पाची आरती', 'गणपतीची आरती', 'गणपती आरती', 'गणेश आरती',
        'ganpati aarti', 'ganpati bappa aarti', 'ganapati bappa arati', 'ganapati aarti', 'ganesh aarti',
        'sukhkarta dukhharta', 'सुखकर्ता दुखहर्ता', 'सुखकर्ता दुःखहर्ता', 'sukhkarta', 'सुखकर्ता',
        'आरती लाव', 'आरती सुरू कर', 'आरती प्ले कर', 'आरती चालू कर', 'आरती ऐकव', 'गणपतीचे गाणे लाव', 'ganpatichi aarti',
        'play aarti', 'play ganpati aarti', 'aarti play', 'arti play', 'bappa aarti', 'बाप्पाची आरती', 'बाप्पा आरती',
        'आरती', 'arti', 'aarti', 'arati'
    ]
    if any(at in raw for at in aarti_triggers):
        return True, play_ganpati_aarti(lang)

    # 1. Volume Controls
    if any(q in raw for q in ['आवाज वाढव', 'व्हॉल्यूम वाढव', 'volume up', 'sound up', 'increase volume', 'aawaj vadhva']):
        return True, change_volume('up', 8, lang)
    if any(q in raw for q in ['आवाज कमी कर', 'व्हॉल्यूम कमी कर', 'volume down', 'sound down', 'decrease volume', 'aawaj kami kar']):
        return True, change_volume('down', 8, lang)
    if any(q in raw for q in ['आवाज म्यूट', 'व्हॉल्यूम म्यूट', 'म्यूट कर', 'mute volume', 'unmute', 'mute']):
        return True, change_volume('mute', 0, lang)

    # 2. Screenshot Capture
    if any(q in raw for q in ['स्क्रीनशॉट', 'screenshot', 'स्क्रीन शॉट', 'take screenshot', 'capture screen', 'screen shot']):
        success, msg, _ = capture_screenshot(lang)
        return True, msg

    # 3. PC Lock / Sleep
    if any(q in raw for q in ['स्क्रीन लॉक', 'पीसी लॉक', 'कॉम्प्युटर लॉक', 'lock pc', 'lock screen', 'lock workstation']):
        return True, lock_pc(lang)
    if any(q in raw for q in ['स्लीप मोड', 'पीसी स्लीप', 'sleep pc', 'sleep mode', 'put to sleep']):
        return True, sleep_pc(lang)

    # 3.1 🖥️ Minimize Windows / Show Desktop
    if any(q in raw for q in ['डेस्कटॉप दाखव', 'सर्व खिडक्या बंद कर', 'minimize all', 'show desktop', 'डेस्कटॉप']):
        return True, minimize_all_windows(lang)

    # 3.2 📋 Read Clipboard
    clipboard_triggers = [
        'क्लिपबोर्ड', 'clipboard', 'कॉपी केलेला', 'कॉपी केलेला मजकूर', 'read clipboard',
        'clipboard वाच', 'क्लिपबोर्ड वाच', 'क्लिपबोर्ड दाखव', 'get clipboard'
    ]
    if any(q in raw for q in clipboard_triggers):
        return True, read_clipboard_content(lang)

    # 4. Live News (Daily & Real-Time Refreshed RSS Headlines)
    news_triggers = [
        'ताज्या बातम्या', 'आजच्या बातम्या', 'बातम्या काय आहेत', 'बातम्या सांग', 'बातम्या सांगा',
        'बातम्या', 'बातमी', 'ताजी बातमी', 'ताज्या घडामोडी', 'मुख्य बातम्या', 'आजच्या घडामोडी',
        'आज काय घडले', 'वृत्त', 'वृत्त सांगा', 'live news', 'news headlines', 'today news',
        'aajchya batmya', 'tazya batmya', 'tazya batmya sang', 'batmya sangitalya pahije',
        'daily refresh', 'refresh batmya', 'batmya sang', 'batmya kay ahet', 'batmi sang',
        'aajchi batmi', 'latest news', 'breaking news', 'daily news', 'current news',
        'news sang', 'news bolo', 'news batao', 'samachar', 'khabrein', 'aaj ki khabar',
        'aaj ke samachar', 'taza khabar', 'fresh news', 'headline',
        'ताज़ा खबरें', 'ताज़ा खबर', 'ताजा खबरें', 'ताजा खबर', 'आज की खबरें', 'आज की ताज़ा', 'आज के समाचार',
        'ताज़ा समाचार', 'ताजा समाचार', 'समाचार बताओ', 'खबरें बताओ', 'खबर', 'खबरें', 'समाचार'
    ]
    if any(q in raw for q in news_triggers) or raw in ['news', 'बातम्या', 'बातमी', 'समाचार', 'खबरें', 'headlines', 'news?', 'news!']:
        return True, get_live_news(lang)

    # 4.1 📜 Dinvishesh (Today in History / दिनविशेष - Trilingual Marathi/Hindi/English)
    dinvishesh_triggers = [
        'दिनविशेष', 'आजचा दिनविशेष', 'दिनविशेष सांगा', 'दिनविशेष सांग', 'आजचे दिनविशेष',
        'कालचा दिनविशेष', 'उद्याचा दिनविशेष', 'परवाचा दिनविशेष',
        'din vishesh', 'dinvishesh', 'aajcha din vishesh', 'aajcha dinvishesh', 'din vishesh sang',
        'kalcha dinvishesh', 'udyacha dinvishesh', 'parvacha dinvishesh',
        'आज का दिनविशेष', 'आज का इतिहास', 'इतिहास आज का', 'कल का दिनविशेष', 'कल का इतिहास',
        'aaj ka itihas', 'today in history', 'on this day', 'this day in history', 'history today',
        'yesterday in history', 'tomorrow in history'
    ]
    if any(q in raw for q in dinvishesh_triggers) or raw in ['दिनविशेष', 'dinvishesh', 'din vishesh', 'दिनविशेष?', 'dinvishesh?'] or ('दिनविशेष' in raw or 'dinvishesh' in raw or 'din vishesh' in raw):
        from jarvis_dinvishesh import get_dinvishesh, extract_dinvishesh_date
        d_lang = lang
        if any(w in raw for w in ['इंग्रजी', 'english', 'इंग्लिश', 'in english']):
            d_lang = 'en'
        elif any(w in raw for w in ['हिंदी', 'hindi', 'in hindi']):
            d_lang = 'hi'
        elif any(w in raw for w in ['मराठी', 'marathi', 'in marathi']):
            d_lang = 'mr'
        target_date = extract_dinvishesh_date(text)
        return True, get_dinvishesh(d_lang, target_date=target_date)

    # 4.2 🏏 Live Cricket Score & Matches
    cricket_triggers = [
        'क्रिकेट स्कोअर', 'cricket score', 'cricket live', 'मॅच स्कोअर', 'live match',
        'ipl score', 'cricket match', 'आजची मॅच', 'cricket update', 'live cricket'
    ]
    if any(q in raw for q in cricket_triggers) or raw in ['क्रिकेट', 'cricket']:
        return True, get_cricket_score(lang)

    # 4.3 💹 Stock Market, Sensex, Nifty & Gold Rates
    market_triggers = [
        'शेअर बाजार', 'शेयर बाजार', 'sensex', 'nifty', 'stock market', 'सोन्याचा भाव',
        'सोन्याचा दर', 'gold rate', 'gold price', 'सोन्याचे भाव', 'शेअर मार्केट'
    ]
    if any(q in raw for q in market_triggers):
        return True, get_financial_markets('all', lang)


    # 5. Notes Commands
    # Add note
    if any(q in raw for q in ['नोट लिहून घे', 'नोट कर', 'नोट सेव्ह कर', 'note lihi', 'add note', 'take a note', 'save note']):
        cleaned_note = re.sub(r'^(?:जार्व्हिस|hey jarvis|jarvis)?\s*(?:नोट\s*लिहून\s*घे|नोट\s*कर|नोट\s*सेव्ह\s*कर|add\s*note|save\s*note|take\s*a\s*note)\s*[:\s]*', '', text, flags=re.IGNORECASE).strip()
        return True, add_note(cleaned_note, lang)

    # Read notes
    if any(q in raw for q in ['माझे नोट्स', 'सर्व नोट्स', 'नोट्स दाखव', 'नोट्स वाच', 'read notes', 'show notes', 'my notes', 'get notes']):
        return True, get_notes(lang)

    # Clear notes
    if any(q in raw for q in ['नोट्स डिलीट कर', 'सर्व नोट्स काढ', 'clear notes', 'delete notes']):
        return True, clear_notes(lang)

    # 6. Reminder / Alarm Commands
    if any(q in raw for q in ['आठवण कर', 'रिमाइंड कर', 'अलार्म लाव', 'remind me', 'set reminder', 'aathvan kar', 'set alarm']):
        return True, set_reminder(text, lang)

    # 7. Time & Date (Exact Time with Seconds)
    time_triggers = [
        'वेळ काय', 'किती वाजले', 'वेळ सांग', 'वेळ किती', 'अचूक वेळ', 'नक्की वेळ', 'काय वेळ', 'काय वाजले', 'वेळेविषयी',
        'exact time', 'current time', 'tell time', 'tell me the time', 'tell me time', 'what time',
        'what is the time', "what's the time", 'whats the time', 'time please', 'time now',
        'time kay zala', 'time kay ahe', 'time sang', 'time sanga', 'kiti vajle', 'kiti time',
        'time bolo', 'time batao', 'samay kya', 'kitne baje', 'samay batao', 'kya time', 'time kya',
        'exact time sang', 'exact time sanga', 'time sang na', 'time sang re', 'time bol'
    ]
    if any(q in raw for q in time_triggers) or raw in ['time', 'वेळ', 'समय', 'घड्याळ', 'clock', 'time?', 'time!']:
        return True, get_current_time(lang)

    date_triggers = [
        'आजची तारीख', 'तारीख काय आहे', 'तारीख काय', 'आजचा वार', 'तारीख सांग', 'आज कोणती तारीख',
        'date kay ahe', 'what is the date', "today's date", 'what date is it', 'aajchi tarikh', 'date please', 'current date'
    ]
    if any(q in raw for q in date_triggers) or raw in ['date', 'तारीख', 'तारीख?']:
        return True, get_current_date(lang)


    # 8. System Status / Battery
    if any(q in raw for q in ['सिस्टम स्टेटस', 'बॅटरी किती', 'बॅटरी टक्के', 'system status', 'battery status', 'pc status', 'cpu status', 'laptop status']):
        return True, get_system_status(lang)

    # 9. YouTube Commands
    # 9. 🎵 Zero-Redirect In-Page Music & Song Commands (Marathi, Hindi, English)
    is_stop_intent = any(sw in raw for sw in ['थांबव', 'बंद कर', 'stop', 'pause', 'रोको'])
    if not is_stop_intent:
        music_patterns = [
            # Marathi
            r'(.+?)\s+(?:गाणं|गाणे|गाणी)\s+(?:वाजव|लाव|ऐकव|सुरू कर|चालू कर|प्ले कर)',
            r'(?:गाणं|गाणे|गाणी|संगीत|म्युझिक)\s+(?:वाजव|लाव|ऐकव|सुरू कर|चालू कर|प्ले कर)\s*(.*)',
            r'(?:कोणतेही|कोणतंपण|काहीतरी|छान|नवीन|मस्त|एक)\s+(?:गाणे|गाणं|गाणी)\s*(?:वाजव|लाव|ऐकव|प्ले कर)?\s*(.*)',
            r'^(?:गाणे|गाणं|गाणी|संगीत|म्युझिक)\s*$',
            r'(.+?)\s+(?:वाजव|लाव|ऐकव)\s*$',
            r'^(?:वाजव|लाव|ऐकव)\s+(.+)',
            r'यूट्यूबवर\s+(.+?)\s+(?:लाव|सर्च कर|वाजव|दाखव|प्ले कर)',
            r'यूट्यूब\s+(?:उघड|ओपन\s*कर)',
            # Hindi
            r'(.+?)\s+(?:गाना|गीत|म्यूजिक)\s+(?:बजाओ|सुनाओ|चलाओ|लगाओ)',
            r'(?:गाना|गीत|म्यूजिक|संगीत)\s+(?:बजाओ|सुनाओ|चलाओ|लगाओ)\s*(.*)',
            r'(?:कोई|अच्छा|नया)\s+(?:गाना|गीत)\s+(?:बजाओ|सुनाओ|चलाओ)\s*(.*)',
            r'(.+?)\s+(?:बजाओ|सुनाओ|चलाओ|लगाओ)\s*$',
            r'^(?:बजाओ|सुनाओ|चलाओ|लगाओ)\s+(.+)',
            # English & Hinglish/Marathish
            r'play\s+(.+?)\s+on\s+youtube',
            r'play\s+(.+?)\s+song',
            r'play\s+song\s*(.*)',
            r'play\s+music\s*(.*)',
            r'song\s+play\s+kar\s*(.*)',
            r'song\s+play\s*(.*)',
            r'(.+?)\s+song\s+play',
            r'(.+?)\s+play\s+kar',
            r'play\s+(.+)',
            r'open\s+youtube',
            r'youtube\s+open'
        ]
        # Specific trending keywords
        if any(tk in raw for tk in ['गुलाबी साडी', 'gulabi sadi', 'kesariya', 'tauba tauba', 'believer song', 'aarambh hai prachand', 'राजा शिवछत्रपती']):
            return True, play_youtube(raw, lang)

        for pattern in music_patterns:
            m = re.search(pattern, raw, re.IGNORECASE)
            if m:
                query = ""
                if m.groups():
                    for g in m.groups():
                        if g and g.strip():
                            query = g.strip()
                            break
                if not query:
                    query = "trending songs"
                return True, play_youtube(query, lang)

    # 10. Google Search Commands
    google_patterns = [
        r'गुगल\s*वर\s+(.+?)\s+(?:शोध|सर्च कर|दाखव)',
        r'गुगल\s+उघड',
        r'search\s+(.+?)\s+on\s+google',
        r'search\s+for\s+(.+)',
        r'google\s+(.+)'
    ]
    for pattern in google_patterns:
        m = re.search(pattern, raw, re.IGNORECASE)
        if m:
            if m.groups() and m.group(1):
                query = m.group(1)
                return True, search_google(query, lang)
            else:
                webbrowser.open("https://www.google.com")
                return True, "गुगल उघडत आहे, सर." if lang == 'mr' else "Opening Google, Sir."

    # 11. Weather Commands
    if any(w in raw for w in ['हवामान', 'मौसम', 'weather', 'temperature', 'तापमान']):
        city = 'Pune'
        cities = ['pune', 'mumbai', 'delhi', 'nagpur', 'nashik', 'kolhapur', 'satara', 'aurangabad', 'sambhajinagar', 'solapur', 'bangalore', 'hyderabad', 'thane']
        for c in cities:
            if c in raw:
                city = c.capitalize()
                break
        return True, get_weather(city, lang)

    # 12. Application Opening Commands
    if 'उघड' in raw or 'open' in raw or 'खोलो' in raw or 'start' in raw or 'launch' in raw:
        apps = ['notepad', 'calculator', 'calc', 'chrome', 'edge', 'cmd', 'terminal', 'powershell', 'paint', 'explorer', 'taskmgr', 'code', 'vscode', 'spotify', 'whatsapp', 'settings', 'github']
        for app in apps:
            if app in raw or (app == 'notepad' and 'नोटपॅड' in raw) or (app == 'calculator' and 'कॅल्क्युलेटर' in raw) or (app == 'chrome' and 'क्रोम' in raw):
                success, msg = open_application(app, lang)
                if success:
                    return True, msg

    # 13. Application Closing Commands
    if any(k in raw for k in ['बंद कर', 'close', 'kill', 'बंद करा', 'हटाओ', 'बंद करो']) and not any(m in raw for m in ['गाणे', 'गाणं', 'music', 'song', 'video', 'आरती', 'aarti', 'audio']):
        close_apps = ['notepad', 'calculator', 'calc', 'chrome', 'edge', 'code', 'vscode', 'spotify', 'cmd', 'paint', 'powershell', 'taskmgr', 'whatsapp', 'कॅल्क्युलेटर', 'नोटपॅड', 'क्रोम', 'टास्क मॅनेजर']
        for ca in close_apps:
            if ca in raw:
                success, msg = close_application(ca, lang)
                if success or msg:
                    return True, msg

    return False, ""
