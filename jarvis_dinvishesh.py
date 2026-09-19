import os
import re
import sys
import json
import base64
import datetime
import requests
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

MONTHS_MR = ['', 'जानेवारी', 'फेब्रुवारी', 'मार्च', 'एप्रिल', 'मे', 'जून', 'जुलै', 'ऑगस्ट', 'सप्टेंबर', 'ऑक्टोबर', 'नोव्हेंबर', 'डिसेंबर']
MONTHS_HI = ['', 'जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
DAYS_MR = ['सोमवार', 'मंगळवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']
DAYS_HI = ['सोमवार', 'मंगलवार', 'बुधवार', 'गुरुवार', 'शुक्रवार', 'शनिवार', 'रविवार']

DEV_TO_LATIN = {'०': '0', '१': '1', '२': '2', '३': '3', '४': '4', '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'}

MONTH_MAP = {
    # Marathi
    'जानेवारी': 1, 'फेब्रुवारी': 2, 'मार्च': 3, 'एप्रिल': 4, 'मे': 5, 'जून': 6,
    'जुलै': 7, 'ऑगस्ट': 8, 'सप्टेंबर': 9, 'ऑक्टोबर': 10, 'नोव्हेंबर': 11, 'डिसेंबर': 12,
    # Hindi
    'जनवरी': 1, 'फरवरी': 2, 'फ़रवरी': 2, 'मार्च': 3, 'अप्रैल': 4, 'मई': 5, 'जून': 6,
    'जुलाई': 7, 'अगस्त': 8, 'सितंबर': 9, 'सितम्बर': 9, 'अक्टूबर': 10, 'नवंबर': 11, 'दिसंबर': 12,
    # English
    'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
    'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
    'august': 8, 'aug': 8, 'september': 9, 'sept': 9, 'sep': 9,
    'october': 10, 'oct': 10, 'november': 11, 'nov': 11, 'december': 12, 'dec': 12
}

SPECIAL_DAYS = {
    'महाराष्ट्र दिन': (5, 1),
    'कामगार दिन': (5, 1),
    'स्वातंत्र्य दिन': (8, 15),
    'independence day': (8, 15),
    'प्रजासत्ताक दिन': (1, 26),
    'republic day': (1, 26),
    'शिवजयंती': (2, 19),
    'shiv jayanti': (2, 19),
    'गांधी जयंती': (10, 2),
    'gandhi jayanti': (10, 2),
    'शिक्षक दिन': (9, 5),
    'teachers day': (9, 5),
    'महाराष्ट्र दिन': (5, 1),
    'maharashtra din': (5, 1),
    'कामगार दिन': (5, 1),
    'kamgar din': (5, 1),
    'स्वातंत्र्य दिन': (8, 15),
    'swatantrya din': (8, 15),
    'independence day': (8, 15),
    'प्रजासत्ताक दिन': (1, 26),
    'prajasattak din': (1, 26),
    'republic day': (1, 26),
    'शिवजयंती': (2, 19),
    'shiv jayanti': (2, 19),
    'shivjayanti': (2, 19),
    'गांधी जयंती': (10, 2),
    'gandhi jayanti': (10, 2),
    'शिक्षक दिन': (9, 5),
    'shikshak din': (9, 5),
    'teachers day': (9, 5),
    'बालदिन': (11, 14),
    'bal din': (11, 14),
    'childrens day': (11, 14),
    'संविधान दिन': (11, 26),
    'samvidhan din': (11, 26),
    'constitution day': (11, 26),
    'विज्ञान दिन': (2, 28),
    'vidnyan din': (2, 28),
    'science day': (2, 28),
    'महिला दिन': (3, 8),
    'mahila din': (3, 8),
    'womens day': (3, 8),
    'योग दिन': (6, 21),
    'yoga day': (6, 21),
    'आंबेडकर जयंती': (4, 14),
    'ambedkar jayanti': (4, 14),
}

def normalize_text(text: str) -> str:
    """Replaces Devanagari digits with ASCII digits and lowercases."""
    for d, l in DEV_TO_LATIN.items():
        text = text.replace(d, l)
    return text.lower()

def extract_dinvishesh_date(text: str, base_date: datetime.datetime = None) -> datetime.datetime:
    """
    Dynamically extracts a target date from user query.
    Supports relative dates ('काल', 'उद्या', 'परवा', 'आज', 'yesterday', 'tomorrow'),
    named special days ('महाराष्ट्र दिन', 'स्वातंत्र्य दिन', etc.),
    and explicit dates ('15 ऑगस्ट', '26 जानेवारी', '20 September', '15/08', '20-09-2026').
    Defaults to current system date if none found.
    """
    now = base_date or datetime.datetime.now()
    if not text:
        return now

    norm = normalize_text(text)

    # 1. Relative dates
    if any(k in norm for k in ['कालचा', 'कालचे', 'कालची', 'काल', 'kalcha', 'kalche', 'kalchi', 'kal ka', 'yesterday', 'बीता हुआ कल']):
        return now - datetime.timedelta(days=1)
    if any(k in norm for k in ['उद्याचा', 'उद्याचे', 'उद्याची', 'उद्या', 'udyacha', 'udyache', 'udyachi', 'udya', 'tomorrow', 'आने वाला कल', 'aane wala kal']):
        return now + datetime.timedelta(days=1)
    if any(k in norm for k in ['परवाचा', 'परवाचे', 'परवा', 'parvacha', 'parva', 'day after tomorrow']):
        return now + datetime.timedelta(days=2)
    if any(k in norm for k in ['आजचा', 'आजचे', 'आजची', 'आज', 'today', 'aajcha', 'aajche', 'aaj ka', 'aaj']):
        return now

    # 2. Named special days
    for s_name, (m, d) in SPECIAL_DAYS.items():
        if s_name in norm:
            try:
                return datetime.datetime(now.year, m, d)
            except Exception:
                pass

    # 3. Explicit Day + Month name (e.g. "15 ऑगस्ट", "15th August", "26 जानेवारी", "20 सप्टेंबर 2026")
    months_pattern = "|".join(sorted(MONTH_MAP.keys(), key=lambda x: -len(x)))

    # Pattern 1: Day first -> 15 ऑगस्ट 2026 / 15th August 2026
    m1 = re.search(rf'(\b\d{{1,2}})\s*(?:st|nd|rd|th|वे|वा|वी|चा|चे|ची|ला|रोजी)?\s*({months_pattern})\s*(?:चा|चे|ची)?\s*(\d{{4}})?', norm)
    if m1:
        day_val = int(m1.group(1))
        month_str = m1.group(2)
        year_val = int(m1.group(3)) if m1.group(3) else now.year
        month_val = MONTH_MAP.get(month_str)
        if month_val and 1 <= day_val <= 31:
            try:
                return datetime.datetime(year_val, month_val, day_val)
            except ValueError:
                pass

    # Pattern 2: Month first -> ऑगस्ट 15, August 15 2026
    m2 = re.search(rf'({months_pattern})\s*(\b\d{{1,2}})\s*(?:st|nd|rd|th|वे|वा|वी|चा|चे|ची|ला|रोजी)?\s*(\d{{4}})?', norm)
    if m2:
        month_str = m2.group(1)
        day_val = int(m2.group(2))
        year_val = int(m2.group(3)) if m2.group(3) else now.year
        month_val = MONTH_MAP.get(month_str)
        if month_val and 1 <= day_val <= 31:
            try:
                return datetime.datetime(year_val, month_val, day_val)
            except ValueError:
                pass

    # Pattern 3: Numeric date DD/MM/YYYY or DD-MM-YYYY or DD.MM.YYYY
    m3 = re.search(r'(\b\d{1,2})[./\-](\d{1,2})(?:[./\-](\d{2,4}))?\b', norm)
    if m3:
        d_val = int(m3.group(1))
        m_val = int(m3.group(2))
        y_val = int(m3.group(3)) if m3.group(3) else now.year
        if y_val < 100:
            y_val += 2000
        if 1 <= d_val <= 31 and 1 <= m_val <= 12:
            try:
                return datetime.datetime(y_val, m_val, d_val)
            except ValueError:
                pass

    # Default to current dynamic system date
    return now

def get_cached_dinvishesh(cache_key: str):
    cache_file = os.path.join(DATA_DIR, f"dinvishesh_{cache_key}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                content = data.get('content', '')
                # Ensure no stale/corrupted legacy year 2024 is served for 2026
                if '2024' in content and '2026' in cache_key:
                    return None
                return content
        except Exception:
            return None
    return None

def save_cached_dinvishesh(cache_key: str, date_label: str, lang: str, content: str):
    cache_file = os.path.join(DATA_DIR, f"dinvishesh_{cache_key}.json")
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                'date': date_label,
                'lang': lang,
                'content': content,
                'created_at': datetime.datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving dinvishesh cache: {e}")

def fetch_wikipedia_onthisday(month: int, day: int) -> dict:
    """Fallback to official Wikipedia On This Day API."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/feed/onthisday/all/{month:02d}/{day:02d}"
        headers = {'User-Agent': 'JarvisAI/3.0 (contact@jarvis.ai)'}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Wikipedia onthisday error: {e}")
    return {}

def format_wikipedia_fallback(wiki_data: dict, lang: str, target_dt: datetime.datetime) -> str:
    """Formats Wikipedia data into structured Marathi, Hindi, or English text."""
    events = wiki_data.get('events', [])[:3]
    births = wiki_data.get('births', [])[:3]
    deaths = wiki_data.get('deaths', [])[:2]

    today_dt = datetime.datetime.now()
    is_today = (target_dt.date() == today_dt.date())
    is_yesterday = (target_dt.date() == (today_dt - datetime.timedelta(days=1)).date())
    is_tomorrow = (target_dt.date() == (today_dt + datetime.timedelta(days=1)).date())

    if lang == 'mr':
        date_str = f"{DAYS_MR[target_dt.weekday()]}, {target_dt.day} {MONTHS_MR[target_dt.month]} {target_dt.year}"
        prefix = "आजचा दिनविशेष" if is_today else ("कालचा दिनविशेष" if is_yesterday else ("उद्याचा दिनविशेष" if is_tomorrow else f"{target_dt.day} {MONTHS_MR[target_dt.month]} चा दिनविशेष"))
        out = [f"📜 **{prefix} ({date_str}):**\n"]
        out.append("🏛️ **महत्त्वाच्या ऐतिहासिक घटना:**")
        for e in events:
            out.append(f"• **{e.get('year', '')}**: {e.get('text', '')}")
        out.append("\n🎂 **जन्म / जयंती:**")
        for b in births:
            out.append(f"• **{b.get('year', '')}**: {b.get('text', '')}")
        if deaths:
            out.append("\n🕯️ **स्मृतीदिन / पुण्यतिथी:**")
            for d in deaths:
                out.append(f"• **{d.get('year', '')}**: {d.get('text', '')}")
        return "\n".join(out)
    elif lang == 'hi':
        date_str = f"{DAYS_HI[target_dt.weekday()]}, {target_dt.day} {MONTHS_HI[target_dt.month]} {target_dt.year}"
        prefix = "आज का दिनविशेष" if is_today else ("कल का दिनविशेष" if is_yesterday else ("आने वाले कल का दिनविशेष" if is_tomorrow else f"{target_dt.day} {MONTHS_HI[target_dt.month]} का दिनविशेष"))
        out = [f"📜 **{prefix} - इतिहास के झरोखे से ({date_str}):**\n"]
        out.append("🏛️ **प्रमुख ऐतिहासिक घटनाएँ:**")
        for e in events:
            out.append(f"• **{e.get('year', '')}**: {e.get('text', '')}")
        out.append("\n🎂 **जन्म / जयंती:**")
        for b in births:
            out.append(f"• **{b.get('year', '')}**: {b.get('text', '')}")
        if deaths:
            out.append("\n🕯️ **स्मृति दिवस / पुण्यतिथि:**")
            for d in deaths:
                out.append(f"• **{d.get('year', '')}**: {d.get('text', '')}")
        return "\n".join(out)
    else:
        date_str = target_dt.strftime("%A, %d %B %Y")
        prefix = "Today in History" if is_today else ("Yesterday in History" if is_yesterday else ("Tomorrow in History" if is_tomorrow else f"History on {target_dt.strftime('%d %B %Y')}"))
        out = [f"📜 **{prefix} - Daily Chronicles ({date_str}):**\n"]
        out.append("🏛️ **Major Historical Events:**")
        for e in events:
            out.append(f"• **{e.get('year', '')}**: {e.get('text', '')}")
        out.append("\n🎂 **Notable Births:**")
        for b in births:
            out.append(f"• **{b.get('year', '')}**: {b.get('text', '')}")
        if deaths:
            out.append("\n🕯️ **Notable Deaths:**")
            for d in deaths:
                out.append(f"• **{d.get('year', '')}**: {d.get('text', '')}")
        return "\n".join(out)

def get_dinvishesh(lang: str = 'mr', target_date: datetime.datetime = None, query_text: str = '') -> str:
    """
    Returns authentic, deeply researched Dinvishesh (Today in History)
    for the exact target date (daily dynamic calendar date or user-specified date)
    in Marathi ('mr'), Hindi ('hi'), or English ('en').
    """
    if target_date is None and query_text:
        now = extract_dinvishesh_date(query_text)
    else:
        now = target_date or datetime.datetime.now()

    cache_key = f"{now.strftime('%Y_%m_%d')}_{lang}"

    # 1. Check instant cache (0.001s response)
    cached = get_cached_dinvishesh(cache_key)
    if cached:
        return cached

    month_mr = MONTHS_MR[now.month]
    month_hi = MONTHS_HI[now.month]
    day_num = now.day

    today_dt = datetime.datetime.now()
    is_today = (now.date() == today_dt.date())
    is_yesterday = (now.date() == (today_dt - datetime.timedelta(days=1)).date())
    is_tomorrow = (now.date() == (today_dt + datetime.timedelta(days=1)).date())

    if lang == 'mr':
        date_label = f"{day_num} {month_mr}"
        full_date_label = f"{DAYS_MR[now.weekday()]}, {day_num} {month_mr} {now.year}"
        date_context = "आजची तारीख" if is_today else ("कालची तारीख" if is_yesterday else ("उद्याची तारीख" if is_tomorrow else "विशिष्ट तारीख"))
        prompt = f"""तुम्ही जार्व्हिस (J.A.R.V.I.S.) आहात.
तारीख: {full_date_label} ({date_context}: {day_num} {month_mr}, वर्ष: {now.year}).
कृपया {full_date_label} या दिवसाचा अधिकृत, समृद्ध आणि प्रेरणादायी 'दिनविशेष' (Today in History) मराठीत सांगा.

खालील ४ विभाग अत्यंत आकर्षक व नेमक्या बुलेट पॉईंट्समध्ये द्या:
१. 🌟 **विशेष दिन / जागतिक दिन** (या तारखेचे महत्त्वाचे राष्ट्रीय किंवा आंतरराष्ट्रीय दिन)
२. 🏛️ **महत्त्वाच्या ऐतिहासिक घटना** (भारत व जगातील या दिवशी घडलेल्या ऐतिहासिक घडामोडी - वर्ष/सालासह)
३. 🎂 **जन्म / जयंती** (महान व्यक्ती, क्रांतिकारक, समाजसुधारक, वैज्ञानिक, साहित्यिक, खेळाडू यांचे जन्म - वर्ष/सालासह)
४. 🕯️ **स्मृतीदिन / पुण्यतिथी** (या दिवशी झालेल्या महान व्यक्तींच्या पुण्यतिथी - वर्ष/सालासह)

नियम:
- परिचयाच्या सुरुवातीला चालू तारीख "{full_date_label}" चाच स्पष्ट उल्लेख करा (उदा. "तारीख: {full_date_label}").
- भाषेचा दर्जा दर्जेदार व शुद्ध मराठी असावा.
- महाराष्ट्रातील आणि भारतातील ऐतिहासिक घटना व व्यक्तींना अग्रस्थान द्या.
- प्रत्येक मुद्द्यामध्ये वर्ष (साल) ठळकपणे लिहा."""
    elif lang == 'hi':
        date_label = f"{day_num} {month_hi}"
        full_date_label = f"{DAYS_HI[now.weekday()]}, {day_num} {month_hi} {now.year}"
        date_context = "आज की तारीख" if is_today else ("कल की तारीख" if is_yesterday else ("आने वाले कल की तारीख" if is_tomorrow else "तारीख"))
        prompt = f"""आप जार्विस (J.A.R.V.I.S.) हैं।
तारीख: {full_date_label} ({date_context}: {day_num} {month_hi}, वर्ष: {now.year}).
कृपया {full_date_label} का संपूर्ण और प्रामाणिक 'दिनविशेष' (आज का इतिहास - Today in History) हिंदी में बताइए।

निम्नलिखित ४ अनुभाग स्पष्ट व आकर्षक बुलेट पॉइंट्स में दें:
१. 🌟 **विशेष दिवस** (राष्ट्रीय या अंतर्राष्ट्रीय दिवस)
२. 🏛️ **प्रमुख ऐतिहासिक घटनाएँ** (भारत और विश्व की प्रमुख ऐतिहासिक घटनाएँ - वर्ष सहित)
३. 🎂 **जन्म / जयंती** (महान हस्तियों, स्वतंत्रता सेनानियों, वैज्ञानिकों, साहित्यकारों के जन्म - वर्ष सहित)
४. 🕯️ **पुण्यतिथि / स्मृति दिवस** (वर्ष सहित)

नियम:
- परिचय में स्पष्ट रूप से "{full_date_label}" लिखें।
- भारत और विश्व के इतिहास को प्राथमिकता दें और प्रामाणिक तथ्य दें।"""
    else:
        date_label = now.strftime("%d %B")
        full_date_label = now.strftime("%A, %d %B %Y")
        date_context = "Today's Date" if is_today else ("Yesterday's Date" if is_yesterday else ("Tomorrow's Date" if is_tomorrow else "Target Date"))
        prompt = f"""You are JARVIS.
Date: {full_date_label} ({date_context}: {day_num} {now.strftime('%B')}, Year: {now.year}).
Please provide a comprehensive and inspiring 'Today in History' (Dinvishesh) for {full_date_label} in English.

Structure into 4 clear, well-presented sections:
1. 🌟 **Special Observance / International Day**
2. 🏛️ **Major Historical Events** (Significant events in India and world history with year)
3. 🎂 **Notable Births & Anniversaries** (Great personalities, scientists, leaders with year)
4. 🕯️ **Notable Deaths & Memorials** (With year)

Rules:
- Mention the exact date and year "{full_date_label}" in the opening.
- Give prominent focus to important Indian and global milestones. Keep it crisp, accurate and inspiring."""

    content = None
    api_key = os.getenv('GEMINI_API_KEY', '').strip()

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            # Try fast active models
            for model_name in ['gemini-flash-lite-latest', 'gemini-3.6-flash', 'gemini-flash-latest']:
                try:
                    res = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if res and res.text:
                        content = res.text.strip()
                        break
                except Exception:
                    continue
        except Exception as e:
            print(f"Dinvishesh Gemini error: {e}")

    # Fallback to Wikipedia On-This-Day if Gemini is offline or slow
    if not content:
        wiki_data = fetch_wikipedia_onthisday(now.month, now.day)
        if wiki_data:
            content = format_wikipedia_fallback(wiki_data, lang, now)

    if not content:
        if lang == 'mr':
            content = f"📜 **दिनविशेष ({full_date_label}):**\n\nया दिवसाचा इतिहास संकलित करताना तात्पुरती अडचण आली, सर. कृपया थोड्या वेळाने पुन्हा विचारा."
        elif lang == 'hi':
            content = f"📜 **दिनविशेष ({full_date_label}):**\n\nइस तारीख के इतिहास की जानकारी संकलित करने में समस्या आ रही है, सर।"
        else:
            content = f"📜 **History Chronicles ({full_date_label}):**\n\nUnable to retrieve historical archives for this date at the moment, Sir."

    # Encode card payload
    card_info = {
        'date_label': full_date_label,
        'lang': lang,
        'short_date': date_label,
        'year': now.year,
        'month': now.month,
        'day': now.day
    }
    b64_info = base64.b64encode(json.dumps(card_info, ensure_ascii=False).encode('utf-8')).decode('utf-8')
    card_token = f"\n\n[DINVISHESH_CARD:{full_date_label}|{lang}|{b64_info}]"

    full_response = content + card_token

    # Cache response specifically for this date & year
    save_cached_dinvishesh(cache_key, full_date_label, lang, full_response)
    return full_response

if __name__ == '__main__':
    print("--- Test Dynamic Dates ---")
    today_dt = datetime.datetime.now()
    print("Today:", today_dt.strftime("%Y-%m-%d"))
    
    test_queries = [
        "आजचा दिनविशेष",
        "कालचा दिनविशेष सांग",
        "उद्याचा दिनविशेष",
        "15 ऑगस्टचा दिनविशेष काय आहे",
        "२६ जानेवारीचा दिनविशेष सांग",
        "महाराष्ट्र दिनविशेष",
        "who was born on 20 september"
    ]
    for q in test_queries:
        dt = extract_dinvishesh_date(q, today_dt)
        print(f"Query: '{q}' -> Extracted Date: {dt.strftime('%Y-%m-%d')}")
