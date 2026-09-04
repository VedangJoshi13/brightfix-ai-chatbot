import streamlit as st
import json
import os
from dotenv import load_dotenv

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="View Bookings - BrightFix", page_icon="📅")

st.title("📅 View Bookings")
st.caption("All appointments stored in the BrightFix system.")


# ---------------- LOAD env + FIREBASE ----------------
load_dotenv()

FIREBASE_JSON = os.getenv("FIREBASE_KEY")
FIREBASE_KEY_PATH = os.getenv("FIREBASE_KEY_PATH")
db = None

try:
    fb_dict = None

    # Streamlit Community Cloud
    if "firebase" in st.secrets:
        fb_dict = dict(st.secrets["firebase"])

    # Local environment JSON
    elif FIREBASE_JSON:
        fb_dict = json.loads(FIREBASE_JSON)

    # Local firebase-key.json file
    elif FIREBASE_KEY_PATH and os.path.exists(FIREBASE_KEY_PATH):
        with open(FIREBASE_KEY_PATH, "r", encoding="utf-8") as f:
            fb_dict = json.load(f)

    if fb_dict is not None:
        if not firebase_admin._apps:
            cred = credentials.Certificate(fb_dict)
            firebase_admin.initialize_app(cred)

        db = firestore.client()

    else:
        st.warning("Firebase credentials not found. Cannot load bookings.")

except Exception as e:
    st.error(f"Firebase error: {e}")



# ---------------- FETCH BOOKINGS ----------------
def fetch_bookings():
    """Returns all Firestore bookings sorted by date descending."""
    if db is None:
        return None

    try:
        docs = db.collection("appointments").stream()
        bookings = []

        for doc in docs:
            data = doc.to_dict()
            bookings.append(data)

        # Sort by date (descending)
        bookings.sort(key=lambda x: x.get("date", ""), reverse=True)

        return bookings

    except Exception as e:
        st.error(f"Error fetching bookings: {e}")
        return None


# ---------------- DISPLAY DATA ----------------
bookings = fetch_bookings()

if bookings is None:
    st.info("No bookings found or Firebase not connected.")
else:
    if len(bookings) == 0:
        st.info("No bookings stored yet.")
    else:
        st.success(f"Loaded {len(bookings)} bookings.")

        # Create a readable table
        table_data = []
        for b in bookings:
            table_data.append({
                "Name": b.get("name", ""),
                "Date": b.get("date", ""),
                "Time": b.get("time", ""),
                "Service": b.get("service", ""),
                "Reference ID": b.get("id", ""),
                "Created At": b.get("created_at", "")
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True,
        )


# ---------------- EXTRA UI ----------------
st.markdown("---")

st.markdown(
    """
    ### ℹ️ How this works  
    This page reads booking records directly from **Firebase Firestore**,  
    updated automatically whenever a new appointment is created via the chatbot.
    
    All bookings include:
    - Customer Name  
    - Appointment Date  
    - Time  
    - Service  
    - Reference ID  
    - Timestamp  
    """
)
