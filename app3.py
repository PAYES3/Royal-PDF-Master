import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 DOUBLE AD ENGINE ---
def show_top_ad():
    # Box 1: Top Ad
    ad_html = """
    <div style="background-color: #ffffff; border: 1px solid #eee; border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 10px;">
        <p style="font-size: 10px; color: #bbb;">ADVERTISEMENT (TOP)</p>
        <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
        <div id="container-91c31c4db3f1171ac7807f880c080828"></div>
    </div>
    """
    components.html(ad_html, height=260)

def show_bottom_ad():
    # Box 2: Bottom Ad (Wrapping in a different div to avoid ID conflict)
    ad_html = """
    <div style="background-color: #ffffff; border: 1px solid #eee; border-radius: 10px; padding: 10px; text-align: center; margin-top: 10px;">
        <p style="font-size: 10px; color: #bbb;">RECOMMENDED FOR YOU</p>
        <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
        <div id="container-footer-91c31c4db3f1171ac7807f880c080828">
            <script>
                (function() {
                    var s = document.createElement('script');
                    s.src = 'https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js';
                    s.async = true;
                    document.getElementById('container-footer-91c31c4db3f1171ac7807f880c080828').appendChild(s);
                })();
            </script>
        </div>
    </div>
    """
    components.html(ad_html, height=260)

# --- 💰 SIDEBAR ---
st.sidebar.title("📑 Royal PDF Master")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])

# --- 🚀 MAIN APP ---
st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Professional PDF Toolkit</h1>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Royal Premium")
    # Premium logic...
else:
    # 📢 1. TOP AD CALL
    show_top_ad()
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- TOOLS LOGIC (Simplified for view) ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload files", type="pdf", accept_multiple_files=True)
        if files and st.button("Merge Now"):
            # merge logic...
            st.success("Merged!")

    # ... (Other tool logics)

    # 📢 2. BOTTOM AD CALL
    st.write("---")
    show_bottom_ad()

# --- PROFESSIONAL FOOTER ---
st.markdown("---")
st.caption("© 2026 Royal PDF Master | Privacy Policy | Secure Processing")
