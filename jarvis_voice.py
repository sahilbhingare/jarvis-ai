import os
import re
import hashlib
import asyncio
import edge_tts
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
os.makedirs(CACHE_DIR, exist_ok=True)

DEFAULT_EN_VOICE = os.getenv('VOICE_EN', 'en-US-ChristopherNeural')
DEFAULT_MR_VOICE = os.getenv('VOICE_MR', 'mr-IN-AarohiNeural')
DEFAULT_HI_VOICE = os.getenv('VOICE_HI', 'hi-IN-MadhurNeural')

MARATHI_HINTS = [
    'आहे', 'नाही', 'काय', 'कसे', 'कसं', 'होय', 'नमस्कार', 'मित्र', 'मित्रा', 
    'झाले', 'झाला', 'केले', 'पाहिजे', 'सांग', 'सांगा', 'करा', 'उघड', 'लावा',
    'महाराज', 'शिवराय', 'छत्रपती', 'स्वराज्य', 'माहिती', 'तारीख', 'वेळ', 'हवामान',
    'कसा', 'कोण', 'कधी', 'कुठे', 'किल्ला', 'किल्ले', 'दुर्ग'
]

HINDI_HINTS = [
    'है', 'नहीं', 'क्या', 'कैसे', 'नमस्ते', 'दोस्त', 'बताओ', 'करो', 'खोलो', 'गाना', 'सुनाओ', 'मौसम', 'किसने', 'किले', 'जानकारी'
]

def clean_text_for_speech(text: str) -> str:
    """Removes markdown symbols, URLs, emojis and formatting so TTS sounds natural and fast."""
    if not text:
        return ''

    # If text has an embedded player or special cards, only announce introductory sentence
    special_tags = [
        '[HANUMAN_CHALISA_PLAYER]', '[SHIVRAYA_AARTI_PLAYER]', '[AARTI_PLAYER]',
        '[MUSIC_PLAYER:', '[YOUTUBE_INLINE:', '[YOUTUBE:', '[WEATHER_CARD:', '[CHANGE_THEME:'
    ]
    for tag in special_tags:
        if tag in text:
            intro_part = text.split(tag)[0].strip()
            if intro_part:
                text = intro_part
            else:
                text = text.replace(tag, '')

    # Clean any remnant tokens
    text = re.sub(r'\[(WEATHER_CARD|LIVE_NEWS_CARD|DINVISHESH_CARD|CHANGE_THEME|YOUTUBE_INLINE|MUSIC_PLAYER)[^\]]*\]', '', text)

    # Remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    # Remove inline code
    text = re.sub(r'`[^`]*`', '', text)
    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove markdown headers and bullets
    text = re.sub(r'^[#*>-]\s*', '', text, flags=re.MULTILINE)
    # Remove markdown links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove raw URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove emojis
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = re.sub(r'[\u2600-\u27bf]', '', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # For natural speech performance, if text is very lengthy (> 700 chars),
    # keep the first ~650 characters ending at a sentence so TTS generates instantly
    # while the full text is displayed on the UI!
    if len(text) > 700:
        # Find clean sentence ending boundary
        cutoff = text[:650]
        last_period = max(cutoff.rfind('.'), cutoff.rfind('।'), cutoff.rfind('!'), cutoff.rfind('?'), cutoff.rfind('\n'))
        if last_period > 300:
            text = cutoff[:last_period + 1]
        else:
            text = cutoff + "..."

    return text

def detect_voice(text: str, preferred_lang: str = None) -> str:
    """Determines the most appropriate neural voice based on text or preferred_lang."""
    if preferred_lang in ['en', 'en-US', 'en-IN']:
        return DEFAULT_EN_VOICE
    if preferred_lang in ['hi', 'hi-IN']:
        return DEFAULT_HI_VOICE
    if preferred_lang in ['mr', 'mr-IN']:
        return DEFAULT_MR_VOICE

    # Check for Devanagari characters
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', text))
    if has_devanagari:
        for word in MARATHI_HINTS:
            if word in text:
                return DEFAULT_MR_VOICE
        for word in HINDI_HINTS:
            if word in text:
                return DEFAULT_HI_VOICE
        return DEFAULT_MR_VOICE

    return DEFAULT_EN_VOICE

async def generate_speech_file(text: str, voice: str = None, preferred_lang: str = None) -> str:
    """Generates an MP3 file using Edge TTS and returns the relative static URL path."""
    cleaned = clean_text_for_speech(text)
    if not cleaned:
        return ''

    # If voice argument was passed as a language code ('mr', 'hi', 'en')
    if voice in ['mr', 'mr-IN', 'marathi']:
        preferred_lang = 'mr'
        voice = DEFAULT_MR_VOICE
    elif voice in ['hi', 'hi-IN', 'hindi']:
        preferred_lang = 'hi'
        voice = DEFAULT_HI_VOICE
    elif voice in ['en', 'en-US', 'en-IN', 'english']:
        preferred_lang = 'en'
        voice = DEFAULT_EN_VOICE

    if not voice:
        voice = detect_voice(cleaned, preferred_lang)

    # Use hash of text + voice as filename cache key
    hash_key = hashlib.md5(f'{cleaned}_{voice}'.encode('utf-8')).hexdigest()
    filename = f'{hash_key}.mp3'
    filepath = os.path.join(CACHE_DIR, filename)

    # Check if a valid, non-empty audio file exists
    if os.path.exists(filepath):
        if os.path.getsize(filepath) > 1000:
            return f'/static/audio/{filename}'
        else:
            # Corrupted / 0-byte file: remove it
            try:
                os.remove(filepath)
            except Exception:
                pass

    try:
        communicate = edge_tts.Communicate(cleaned, voice)
        await communicate.save(filepath)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
            return f'/static/audio/{filename}'
    except Exception as e:
        print(f'Edge TTS error with voice {voice}: {e}')
        # Cleanup failed file
        if os.path.exists(filepath) and os.path.getsize(filepath) < 500:
            try: os.remove(filepath)
            except Exception: pass

        # Fallback to English voice if non-English failed
        if voice != DEFAULT_EN_VOICE:
            try:
                communicate = edge_tts.Communicate(cleaned, DEFAULT_EN_VOICE)
                await communicate.save(filepath)
                if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
                    return f'/static/audio/{filename}'
            except Exception as ex:
                print(f'Fallback voice also failed: {ex}')

    return ''

def speak_sync(text: str, voice: str = None, preferred_lang: str = None) -> str:
    """Synchronous wrapper for generate_speech_file.
    Uses a dedicated event loop per call to be thread-safe inside Flask.
    """
    try:
        # Create a brand-new event loop so this works safely from any Flask thread
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(generate_speech_file(text, voice, preferred_lang))
        finally:
            loop.close()
    except Exception as e:
        print(f"speak_sync error: {e}")
        return ''

if __name__ == '__main__':
    url = speak_sync('Testing English voice. Hello, this is Jarvis speaking.')
    print(f'Test voice generated: {url}')
