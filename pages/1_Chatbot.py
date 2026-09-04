import streamlit as st
import json
import os
import uuid
import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(page_title="BrightFix Chatbot", page_icon="💬")

st.title("💬 BrightFix Support Chatbot")
st.caption("Your AI assistant for services, bookings, FAQs, and more.")

# -------------------
# LOAD ENV + SECRETS
# -------------------
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_JSON = os.getenv("FIREBASE_KEY")
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")

client = None
if OPENAI_KEY:
    client = OpenAI(api_key=OPENAI_KEY)

# -------------------
# FIREBASE INIT
# -------------------
db = None
try:
    fb_dict = None

    if FIREBASE_JSON:
        # Case 1: running on HuggingFace / env with JSON string
        fb_dict = json.loads(FIREBASE_JSON)
    elif FIREBASE_KEY_PATH and os.path.exists(FIREBASE_KEY_PATH):
        # Case 2: running locally with firebase-key.json file
        with open(FIREBASE_KEY_PATH, "r", encoding="utf-8") as f:
            fb_dict = json.load(f)

    if fb_dict is not None:
        if not firebase_admin._apps:
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)
        db = firestore.client()
    else:
        st.warning("Firebase credentials not found. Bookings will not save.")
except Exception as e:
    st.error(f"Firebase init error: {e}")


# -------------------
# LOAD FAQ DATA
# -------------------
def load_faqs():
    try:
        with open("data/faqs.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

FAQS = load_faqs()

# -------------------
# FAQ SEARCH
# -------------------
def get_faq_answer(user_input):
    if not user_input:
        return None

    text = user_input.lower()
    for faq in FAQS:
        q = faq["question"].lower()
        if q in text:
            return faq["answer"]

        for word in q.split():
            if len(word) > 4 and word in text:
                return faq["answer"]

    return None

# -------------------
# TOOLS
# -------------------
def get_opening_hours():
    return {
        "mon_fri": "10 AM – 6 PM",
        "sat": "10 AM – 2 PM",
        "sun": "Closed"
    }

def lookup_products(max_price=None, feature=None, category=None):
    catalog = [
        {"name": "BreezeX Fan", "price": 1499, "features": ["3-speed"], "category": "fan"},
        {"name": "CoolFlow Fan", "price": 2199, "features": ["5-speed", "timer"], "category": "fan"},
        {"name": "BrightLite LED 25W", "price": 399, "features": ["warm-white"], "category": "bulb"},
    ]
    results = []
    for item in catalog:
        if max_price and item["price"] > max_price:
            continue
        if feature and feature not in item["features"]:
            continue
        if category and item["category"] != category:
            continue
        results.append(item)
    return results

# -------------------
# SAVE BOOKING
# -------------------
def save_booking(name, date, time, service):
    appt = {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "date": date,
        "time": time,
        "service": service,
        "created_at": datetime.datetime.now().isoformat()
    }

    try:
        if db:
            db.collection("appointments").document(appt["id"]).set(appt)
    except Exception as e:
        st.error(f"Error saving to Firestore: {e}")

    return appt

# -------------------
# INTENT DETECTION
# -------------------
def detect_intent(text: str):
    text = text.lower()

    if "book" in text or "appointment" in text or "schedule" in text:
        return "booking"

    if "opening" in text and "hours" in text:
        return "hours"

    product_keywords = ["fan", "fans", "bulb", "bulbs"]
    shopping_verbs = ["recommend", "suggest", "find", "show", "options", "under", "price"]

    if any(k in text for k in product_keywords) and any(v in text for v in shopping_verbs):
        return "product"

    return "faq"

# -------------------
# GPT FALLBACK
# -------------------
def llm_reply(history, user_input):
    if client is None:
        return "AI model not available. Try asking about services, products, or bookings."

    messages = [
       {
    "role": "system",
    "content": """
You are BrightFix AI Assistant, an AI-powered customer support
assistant for an electrical services SME.

You can:
- Answer questions about household electrical services.
- Provide general electrical product guidance.
- Explain lighting options such as LED bulbs and energy-efficient lighting.
- Answer general questions about fans, switches, wiring and electrical inspections.
- Help users understand BrightFix services and pricing.
- Assist users with appointment-related questions.

For questions outside electrical services, electrical products,
home electrical maintenance, or BrightFix services, politely explain
that you can only assist with BrightFix and electrical-related queries.

Do not provide instructions for dangerous electrical work.
Recommend a qualified electrician when professional intervention
is appropriate.
"""
}
    ] + history + [{"role": "user", "content": user_input}]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI error: {e}"

# -------------------
# SESSION STATE
# -------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "booking_in_progress" not in st.session_state:
    st.session_state.booking_in_progress = False
if "booking_step" not in st.session_state:
    st.session_state.booking_step = 0
if "booking_data" not in st.session_state:
    st.session_state.booking_data = {}

# Chat bubble UI style
st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 80%;
}
.bot-msg {
    background-color: #EEEEEE;
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 10px;
    max-width: 80%;
}
</style>
""", unsafe_allow_html=True)

def render_user(msg):
    st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)

def render_bot(msg):
    st.markdown(f"<div class='bot-msg'>{msg}</div>", unsafe_allow_html=True)

# -------------------
# DISPLAY HISTORY
# -------------------
for msg in st.session_state.history:
    if msg["role"] == "user":
        render_user(msg["content"])
    else:
        render_bot(msg["content"])

# -------------------
# CHAT INPUT
# -------------------
user_input = st.chat_input("Type your message here...")

if user_input:

    # Log + show user message
    st.session_state.history.append({"role": "user", "content": user_input})
    render_user(user_input)

    # -------------------
    # MULTI-STEP BOOKING FLOW
    # -------------------
    if st.session_state.booking_in_progress:
        step = st.session_state.booking_step
        data = st.session_state.booking_data

        if step == 1:
            data["name"] = user_input
            st.session_state.booking_step = 2
            reply = "Great! What date would you like? (YYYY-MM-DD)"

        elif step == 2:
            data["date"] = user_input
            st.session_state.booking_step = 3
            reply = "Good. What time works for you? (e.g., 14:00)"

        elif step == 3:
            data["time"] = user_input
            st.session_state.booking_step = 4
            reply = "Almost done! What service do you need?"

        elif step == 4:
            data["service"] = user_input
            appt = save_booking(
                data["name"],
                data["date"],
                data["time"],
                data["service"]
            )
            reply = (
                f"✅ Booking confirmed!\n\n"
                f"**Name:** {appt['name']}\n"
                f"**Date:** {appt['date']}\n"
                f"**Time:** {appt['time']}\n"
                f"**Service:** {appt['service']}\n"
                f"**Reference ID:** {appt['id']}"
            )

            # Reset booking flow
            st.session_state.booking_in_progress = False
            st.session_state.booking_step = 0
            st.session_state.booking_data = {}

        st.session_state.history.append({"role": "assistant", "content": reply})
        render_bot(reply)
        st.stop()

    # -------------------
    # NORMAL INTENT HANDLING
    # -------------------
    intent = detect_intent(user_input)

    if intent == "hours":
        hours = get_opening_hours()
        reply = (
            "Here are our opening hours:\n"
            f"- Mon–Fri: {hours['mon_fri']}\n"
            f"- Sat: {hours['sat']}\n"
            f"- Sun: {hours['sun']}"
        )

    elif intent == "product":
        products = lookup_products(max_price=2000, feature="3-speed", category="fan")
        reply = "Here are our available fans:\n" + "\n".join([f"- {p['name']} (₹{p['price']})" for p in products])

    elif intent == "booking":
        st.session_state.booking_in_progress = True
        st.session_state.booking_step = 1
        st.session_state.booking_data = {}
        reply = "Sure! Let's book an appointment. What's your name?"

    else:
        faq_ans = get_faq_answer(user_input)
        reply = faq_ans if faq_ans else llm_reply(st.session_state.history, user_input)

    st.session_state.history.append({"role": "assistant", "content": reply})
    render_bot(reply)
