import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master | Enterprise Edition", page_icon="📑", layout="wide")

# --- 🚀 STABLE AD ENGINE ---
def show_ad():
    # Entha change-um illama direct-ah iframe kulla script-ah vaikkurom
    # Idhu eppovume rendu vera vera components-ah irukuradhala error varaadhu
    ad_code = """
    <div style="text-align:center; background:#fff; padding:10px; border-radius:10px; border:1px solid #ddd;">
        <p style="font-size:10px; color:#aaa; margin-bottom:5px;">SPONSORED CONTENT</p>
        <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
        <div id="container-91c31c4db3f1171ac7807f880c080828"></div>
    </div>
    """
    components.html(ad_code, height=280)

# --- 💰 SIDEBAR ---
st.sidebar.title("📑 Royal PDF Master")
st.sidebar.caption("v2.5 Professional Edition")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])

st.sidebar.markdown("---")
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank">
        <div style="background:#FFDD00; color:black; padding:12px; border-radius:10px; text-align:center; font-weight:bold; border: 2px solid black;">
            ☕ Support Development
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Professional PDF Toolkit</h1>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Premium Subscription")
    st.info("Upgrade for an ad-free experience.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px; border:none; cursor:pointer;">Upgrade Now - ₹99</button></a>', unsafe_allow_html=True)

else:
    # 📢 1. HEADER AD
    show_ad()
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- TOOLS LOGIC ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple
