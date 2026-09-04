import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="BrightFix Pricing", page_icon="💷")

st.title("💷 Pricing")
st.caption("Transparent and affordable service pricing from BrightFix.")

st.write("---")

# ---------------- PRICING TABLE ----------------

pricing = {
    "Fan Installation": "£40 – £60",
    "Wiring Issue Fixing": "£50 – £90 (depending on severity)",
    "LED Bulb Replacement": "£10 per bulb (labour included)",
    "Switchboard Repair": "£60 – £120",
    "Household Electrical Inspection": "£80 – £150",
}

st.markdown(
    """
    ### 📌 Our Standard Pricing (GBP)

    Below are the estimated costs for the services offered by BrightFix.  
    Final pricing may vary based on job complexity, parts required, or location.
    """
)

for service, price in pricing.items():
    st.markdown(f"**• {service}:** {price}")

st.write("---")

# ---------------- NOTES ----------------
st.markdown(
    """
    ### ℹ️ Additional Notes  
    - All work is carried out by certified electrical technicians.  
    - Emergency callouts may incur additional charges.  
    - Quotes are provided upfront before work begins.  
    - Discounts available for multi-service bookings.  
    """
)

st.write("---")

st.markdown(
    """
    If you’re unsure about which service you need, feel free to use the  
    **Chatbot** from the sidebar for assistance or booking.
    """
)
