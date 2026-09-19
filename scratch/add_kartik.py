import sys

def update_jarvis_brain():
    with open('jarvis_brain.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Insert in system prompt
    target_sys = "            f\"Special Fact about Yogesh: Yogesh Bhasar (योगेश भासार) is Sahil's (साहिल) friend (मित्र). If asked about Yogesh Bhasar, clearly state that he is Sahil's friend (तो साहिलचा मित्र आहे). \"\n"
    kartik_sys = "            f\"Special Fact about Kartik: Kartik Mohite (कार्तिक मोहिते) is Sahil's (साहिल) friend (मित्र). If asked about Kartik Mohite, clearly state that he is Sahil's friend (तो साहिलचा मित्र आहे). \"\n"
    if target_sys in content and kartik_sys not in content:
        content = content.replace(target_sys, target_sys + kartik_sys)

    # Insert in if checks
    target_if = "        return \"He is **Sahil's friend**, Sir! 🤝\"\n"
    kartik_if = """
    # 0.1.06 🧑‍🤝‍🧑 Check "कार्तिक मोहिते" Intent
    kartik_kw = [
        'kartik mohite', 'kartik', 'कार्तिक मोहिते', 'कार्तिक',
        'kartik kon', 'kartik kon aahe', 'kartik kon ahe', 'kartik kaun', 'who is kartik',
        'कार्तिक कोण', 'कार्तिक कोण आहे', 'कार्तिक कोण आहेत', 'kartik badal', 'कार्तिक बद्दल',
        'kartik vishayi', 'कार्तिक विषयी'
    ]
    if any(kk in q_lower for kk in kartik_kw):
        if target_lang == 'mr':
            return "तो **साहिलचा मित्र (फ्रेंड)** आहे, सर! 🤝"
        elif target_lang == 'hi':
            return "वह **साहिल का दोस्त (मित्र)** है, सर! 🤝"
        return "He is **Sahil's friend**, Sir! 🤝"
"""

    idx = content.find('yogesh_kw =')
    if idx != -1 and "kartik_kw =" not in content:
        next_return = content.find(target_if, idx)
        if next_return != -1:
            insert_pos = next_return + len(target_if)
            content = content[:insert_pos] + kartik_if + content[insert_pos:]

    with open('jarvis_brain.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('jarvis_brain.py updated')

def update_jarvis_actions():
    with open('jarvis_actions.py', 'r', encoding='utf-8') as f:
        content = f.read()

    target_if = "        return True, \"He is **Sahil's friend**, Sir! 🤝\"\n"
    kartik_if = """
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
"""
    idx = content.find('yogesh_triggers =')
    if idx != -1 and "kartik_triggers =" not in content:
        next_return = content.find(target_if, idx)
        if next_return != -1:
            insert_pos = next_return + len(target_if)
            content = content[:insert_pos] + kartik_if + content[insert_pos:]

    with open('jarvis_actions.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('jarvis_actions.py updated')

update_jarvis_brain()
update_jarvis_actions()
