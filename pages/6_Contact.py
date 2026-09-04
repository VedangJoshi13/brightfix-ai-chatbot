import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Contact BrightFix", page_icon="📞")

st.title("📞 Contact BrightFix")
st.caption("We're here to help with all your electrical needs.")

st.write("---")

# ---------------- CONTACT INFO ----------------

st.markdown(
    """
    ### 📬 Get in Touch  

    You can reach BrightFix through the following contact details:

    **Phone:** +44 0200 123 456  
    **Email:** support@brightfix.com  
    **Address:** London, United Kingdom  
    """
)

st.write("---")

# ---------------- ADDITIONAL INFO ----------------

st.markdown(
    """
    ### 🧩 Need Assistance Right Now?

    Use the **Chatbot** (left sidebar) to:
    - Ask questions  
    - Get pricing details  
    - Understand services  
    - Start a booking  
    - Check availability  

    Our automated assistant is available 24/7 to guide you.
    """
)

st.write("---")

st.markdown(
    """
    ### 📅 Want to Book an Appointment?

    You can:
    - Chat with the bot to start a booking  
    - Or visit **View Bookings** to check stored appointments  
    """
)
