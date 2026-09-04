import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="BrightFix Services", page_icon="🛠")

st.title("🛠 Services Offered")
st.caption("Professional electrical services provided by BrightFix.")

st.write("---")

# ---------------- SERVICES CONTENT ----------------

services = [
    "🔧 **Fan Installation** — Complete installation of ceiling and wall-mounted fans.",
    "🔌 **Wiring Issue Fixing** — Troubleshooting and repairing electrical wiring faults.",
    "💡 **LED Bulb Replacement** — Energy-efficient LED bulb fitting and replacement.",
    "📟 **Switchboard Repair** — Switch repair, replacement, and safety diagnostics.",
    "🏠 **Household Electrical Inspection** — Full home electrical system inspection.",
]

st.markdown(
    """
    ### Our Core Services  
    At BrightFix, we provide reliable and affordable electrical solutions for homes and businesses.
    Below are the key services we offer:
    """
)

for s in services:
    st.markdown(f"- {s}")

st.write("---")

st.markdown(
    """
    ### Why Choose BrightFix?  
    - ✔ Certified and experienced technicians  
    - ✔ High-quality repair and installation  
    - ✔ Affordable pricing  
    - ✔ Safe, reliable electrical work  
    - ✔ Trusted across London  
    """
)
