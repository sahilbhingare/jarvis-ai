import requests
import json

BASE_URL = "http://127.0.0.1:5000"

test_cases = [
    # Sahil's Education
    {"query": "sahil ch education", "lang": "mr", "check_text": "६९.८८%"},
    {"query": "साहिलचे शिक्षण काय आहे", "lang": "mr", "check_text": "Vyomx Tech Solution"},
    {"query": "sahil ka education batao", "lang": "hi", "check_text": "Vyomx Tech Solution"},
    {"query": "who is sahil and his education", "lang": "en", "check_text": "69.88%"},

    # Zero-Redirect In-Page Music
    {"query": "गाणे वाजव", "lang": "mr", "check_token": "[MUSIC_PLAYER:"},
    {"query": "गुलाबी साडी गाणं वाजव", "lang": "mr", "check_token": "[MUSIC_PLAYER:"},
    {"query": "play kesariya song", "lang": "mr", "check_token": "[MUSIC_PLAYER:"},
    {"query": "play believer", "lang": "en", "check_token": "[MUSIC_PLAYER:"},
    {"query": "गाना बजाओ", "lang": "hi", "check_token": "[MUSIC_PLAYER:"},

    # Media Stop Command
    {"query": "गाणे थांबव", "lang": "mr", "check_stop": True}
]

print("=========================================================")
print("[TEST] TESTING ZERO-REDIRECT MUSIC & SAHIL EDUCATION API")
print("=========================================================")

all_passed = True
for idx, tc in enumerate(test_cases, 1):
    payload = {
        "message": tc["query"],
        "lang": tc["lang"],
        "session_id": f"test-client-{idx}"
    }
    try:
        res = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=15)
        if res.status_code != 200:
            print(f"[FAIL] Test {idx}: HTTP {res.status_code}")
            all_passed = False
            continue

        data = res.json()
        resp_text = data.get("response", "")
        is_stop = data.get("is_stop", False)

        passed = True
        reason = ""

        if "check_text" in tc:
            if tc["check_text"] not in resp_text:
                passed = False
                reason = f"Missing text '{tc['check_text']}'"
        if "check_token" in tc:
            if tc["check_token"] not in resp_text:
                passed = False
                reason = f"Missing token '{tc['check_token']}'"
        if "check_stop" in tc:
            if not is_stop:
                passed = False
                reason = "is_stop flag was False"

        status_sym = "PASS" if passed else f"FAIL ({reason})"
        clean_q = tc['query'].encode('ascii', 'replace').decode('ascii')
        print(f"[{status_sym}] Test {idx}: '{clean_q}' ({tc['lang']})")
        if not passed:
            all_passed = False
            print(f"   Response snippet: {resp_text[:100].encode('ascii', 'replace').decode('ascii')}")

    except Exception as e:
        print(f"[EXCEPTION] Test {idx}: {e}")
        all_passed = False

print("=========================================================")
if all_passed:
    print("[SUCCESS] ALL 10 TESTS PASSED PERFECTLY!")
else:
    print("[WARNING] SOME TESTS FAILED!")
print("=========================================================")
