import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')

from jarvis_actions import handle_action
from jarvis_brain import get_answer

queries = [
    ('sahil chi insta id', 'mr'),
    ('sahil chi insta id magitlyavar', 'mr'),
    ('sahil insta id de', 'mr'),
    ('साहिलची इंस्टाग्राम आयडी काय आहे?', 'mr'),
    ('sahil instagram', 'mr'),
    ('tell me sahil\'s instagram id', 'en'),
    ('sahil ki insta id batao', 'hi'),
    ('who is sahil and his education', 'en'),
    ('sahil chi family vishayi sang', 'mr'),
    ('yogesh bhasar kon aahe', 'mr')
]

all_passed = True
print("=== TESTING SAHIL INSTAGRAM ID & REGRESSION CHECKS ===")
for q, lang in queries:
    is_action, act_resp = handle_action(q, lang)
    if is_action:
        ans = act_resp
    else:
        ans = get_answer(q, lang)
    
    print(f"\n[QUERY] '{q}' ({lang})")
    print(f"[REPLY] {ans}")

    if 'insta' in q.lower() or 'instagram' in q.lower() or 'इन्स्टाग्राम' in q:
        if 'sahil_bhingare_96k' in ans:
            print(">>> PASS: Found 'sahil_bhingare_96k'")
        else:
            print(">>> FAIL: Missing 'sahil_bhingare_96k'")
            all_passed = False
    elif 'education' in q.lower():
        if '69.88%' in ans:
            print(">>> PASS: Found education")
        else:
            print(">>> FAIL: Education missing")
            all_passed = False
    elif 'family' in q.lower():
        if 'अशोक भिंगारे' in ans or 'Ashok Bhingare' in ans:
            print(">>> PASS: Found family")
        else:
            print(">>> FAIL: Family missing")
            all_passed = False
    elif 'yogesh' in q.lower():
        if 'मित्र' in ans or 'friend' in ans:
            print(">>> PASS: Found friend Yogesh")
        else:
            print(">>> FAIL: Yogesh missing")
            all_passed = False

if all_passed:
    print("\nALL SAHIL INSTAGRAM AND REGRESSION TESTS PASSED! 📸🎉")
else:
    print("\nSOME TESTS FAILED!")
    sys.exit(1)
