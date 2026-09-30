#!/usr/bin/env python3
"""
AI Receptionist Demo — "Bright Smile Dental" (Sydney)
Offline rule-based brain + optional Gemini free-tier key (GEMINI_API_KEY env).
Usage:
    python3 receptionist.py            # interactive chat
    python3 receptionist.py --demo     # scripted demo conversation (for Loom recording)
Zero dependencies (stdlib only).
"""
import json
import os
import re
import sys
import time
import urllib.request

CLINIC = "Bright Smile Dental"
HOURS = "Mon–Fri 8am–6pm, Sat 9am–2pm, Sun closed"
SERVICES = {
    "cleaning": "$149",
    "checkup": "$89",
    "filling": "from $180",
    "root canal": "from $900",
    "implant": "from $2,900",
    "whitening": "$399",
    "braces": "from $4,500",
}
SYSTEM_PROMPT = (
    f"You are the friendly AI receptionist for {CLINIC}, a dental clinic in Sydney. "
    f"Hours: {HOURS}. Services and prices: "
    + ", ".join(f"{k} {v}" for k, v in SERVICES.items())
    + ". Help callers book appointments, answer questions, and triage emergencies "
      "(severe pain/swelling/bleeding = urgent, offer same-day slot). "
      "Keep replies under 40 words, warm and professional. Never invent prices not listed."
)


def offline_reply(text):
    t = text.lower()
    if re.search(r"\b(hi|hello|hey|good (morning|afternoon|evening))\b", t):
        return f"Hello! Thanks for calling {CLINIC}. How can I help you today — booking, hours, or pricing?"
    if "hour" in t or "open" in t or "timing" in t:
        return f"We're open {HOURS}. Would you like to book a slot?"
    if "emergency" in t or "pain" in t or "swelling" in t or "bleeding" in t or "broke" in t or "chipped" in t:
        return "That sounds urgent — we keep same-day emergency slots. Can I book you in today at 3:30pm, or is morning better?"
    if "book" in t or "appointment" in t or "slot" in t or "saturday" in t or "sunday" in t or "monday" in t or "visit" in t:
        day = "Saturday" if "saturday" in t else ("Sunday" if "sunday" in t else "tomorrow")
        if "sunday" in t:
            return "We're closed Sundays — but I can book you Saturday 10:15am or Monday 9:00am. Which works?"
        return f"I can book you {day} — we have 10:15am and 2:45pm open. Which suits you? I'll just need your name and mobile."
    if "price" in t or "cost" in t or "much" in t or "charge" in t:
        for svc, price in SERVICES.items():
            if svc in t:
                return f"Our {svc} is {price}. Want me to book you in for one?"
        return "Checkups are $89, cleaning $149, whitening $399. Which treatment were you asking about?"
    if "where" in t or "location" in t or "address" in t or "park" in t:
        return "We're at 42 Pitt Street, Sydney CBD — 2 minutes from Wynyard station, with parking next door."
    if "human" in t or "person" in t or "dentist" in t and "talk" in t:
        return "Of course — I'll have our front-desk team call you back within 15 minutes. Your number please?"
    if "thank" in t or "bye" in t:
        return f"You're welcome! We look forward to seeing you at {CLINIC}. Have a great day!"
    return ("I can help with bookings, opening hours, prices, or directions. "
            "What did you need — or would you like me to have the clinic call you back?")


def gemini_reply(text, history):
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
        contents = [{"role": "user" if i % 2 == 0 else "model", "parts": [{"text": m}]}
                    for i, m in enumerate(history + [text])]
        payload = json.dumps({
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": contents,
            "generationConfig": {"maxOutputTokens": 120, "temperature": 0.7},
        }).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return None


def respond(text, history):
    ai = gemini_reply(text, history)
    return ai if ai else offline_reply(text)


DEMO_SCRIPT = [
    "Hi, do you have any appointments this Saturday?",
    "How much is a cleaning?",
    "I have really bad tooth pain since last night.",
    "Where are you located?",
    "Ok book me Saturday morning please.",
    "Thanks, bye!",
]


def run_demo():
    mode = "GEMINI (live AI)" if os.environ.get("GEMINI_API_KEY") else "OFFLINE (rule-based)"
    print(f"[{CLINIC} — AI Receptionist demo | brain: {mode}]\n")
    history = []
    for q in DEMO_SCRIPT:
        print(f"Caller: {q}")
        time.sleep(0.6)
        a = respond(q, history)
        history += [q, a]
        print(f"Agent:  {a}\n")
        time.sleep(0.6)
    print("— demo complete: booking captured, emergency triaged, zero missed calls —")


def run_chat():
    mode = "GEMINI (live AI)" if os.environ.get("GEMINI_API_KEY") else "OFFLINE (rule-based)"
    print(f"{CLINIC} — AI Receptionist  [brain: {mode}]  (type 'quit' to exit)\n")
    history = []
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAgent: Thanks for calling!")
            break
        if q.lower() in ("quit", "exit"):
            print("Agent: Thanks for calling!")
            break
        if not q:
            continue
        a = respond(q, history)
        history += [q, a]
        print(f"Agent: {a}\n")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_chat()
