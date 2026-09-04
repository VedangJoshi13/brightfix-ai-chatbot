import streamlit as st

# Set page config (WCAG-friendly)
st.set_page_config(
    page_title="BrightFix",
    page_icon="🔧",
    layout="centered"
)

# ----------- HOME PAGE UI -----------
st.markdown(
    """
    <style>
        .main-title {
            font-size: 48px;
            font-weight: 700;
            text-align: center;
            margin-bottom: -10px;
        }
        .subtitle {
            font-size: 20px;
            font-weight: 400;
            text-align: center;
            color: #5c5c5c;
            margin-bottom: 40px;
        }
        @media (max-width: 600px) {
            .main-title { font-size: 34px; }
            .subtitle { font-size: 16px; }
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="main-title">BrightFix</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Reliable Electrical Services for Your Home & Business</div>', unsafe_allow_html=True)

st.write("---")

# ----------- INTRO TEXT -----------
st.markdown(
    """
    ### Welcome to BrightFix ⚡  
    We provide high-quality electrical installation, repair, and support services across London.  
    Use the sidebar to navigate through different sections of our platform.

    ### 📌 What you can do here:
    - Chat with our AI support assistant  
    - Book an appointment  
    - View your stored bookings  
    - Explore our services and pricing  
    - Learn more about BrightFix  
    - Find our contact information  
    """
)

st.write("---")

st.markdown(
    """
    ### 💬 Start by opening **Chatbot** from the sidebar  
    Or explore our other pages to learn about our services.
    """
)
