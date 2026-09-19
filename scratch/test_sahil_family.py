import requests

BASE_URL = "http://127.0.0.1:5000"

test_cases = [
    {"query": "sahil chi family vishayi sang", "lang": "mr", "checks": ["Ashok Bhingare", "Sunita", "Rohan"]},
    {"query": "family vishayi sang", "lang": "mr", "checks": ["Ashok Bhingare", "Sunita", "Rohan"]},
    {"query": "ashok bhingare kon ahet", "lang": "mr", "checks": ["Ashok Bhingare", "vadil"]},
    {"query": "rohan kon ahe", "lang": "mr", "checks": ["Rohan", "bhau"]},
    {"query": "sunita kon ahet", "lang": "mr", "checks": ["Sunita", "aai"]},
    {"query": "tell me about sahil's family", "lang": "en", "checks": ["Ashok Bhingare", "Sunita", "Rohan"]},
    {"query": "sahil ke pita kon hai", "lang": "hi", "checks": ["Ashok Bhingare"]}
]

print("=========================================================")
print("[TEST] TESTING SAHIL FAMILY API RESPONSES")
print("=========================================================")

all_passed = True
for idx, tc in enumerate(test_cases, 1):
    payload = {
        "message": tc["query"],
        "lang": tc["lang"],
        "session_id": f"test-family-{idx}"
    }
    try:
        res = requests.post(f"{BASE_URL}/api/chat", json=payload, timeout=10)
        if res.status_code != 200:
            print(f"[FAIL] Test {idx}: HTTP {res.status_code}")
            all_passed = False
            continue

        resp_text = res.json().get("response", "")
        clean_q = tc['query'].encode('ascii', 'replace').decode('ascii')
        
        # Check all expected substrings (case-insensitive check for english names or devanagari)
        missing = []
        for chk in tc["checks"]:
            if chk.lower() == "vadil":
                if "वडील" not in resp_text and "father" not in resp_text.lower():
                    missing.append(chk)
            elif chk.lower() == "bhau":
                if "भाऊ" not in resp_text and "brother" not in resp_text.lower() and "भाई" not in resp_text:
                    missing.append(chk)
            elif chk.lower() == "aai":
                if "आई" not in resp_text and "mother" not in resp_text.lower() and "माता" not in resp_text:
                    missing.append(chk)
            elif chk.lower() not in resp_text.lower() and chk not in resp_text:
                missing.append(chk)

        if not missing:
            print(f"[PASS] Test {idx}: '{clean_q}' ({tc['lang']})")
        else:
            print(f"[FAIL] Test {idx}: '{clean_q}' -> Missing: {missing}")
            print(f"       Response snippet: {resp_text[:100].encode('ascii', 'replace').decode('ascii')}")
            all_passed = False

    except Exception as e:
        print(f"[EXCEPTION] Test {idx}: {e}")
        all_passed = False

print("=========================================================")
if all_passed:
    print("[SUCCESS] ALL FAMILY TESTS PASSED PERFECTLY!")
else:
    print("[WARNING] SOME TESTS FAILED!")
print("=========================================================")
