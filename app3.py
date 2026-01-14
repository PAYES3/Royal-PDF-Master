import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- ADSTERRA LOGIC ---
def inject_ad_scripts():
    social_bar_script = """
    <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    """
    components.html(social_bar_script, height=0)

def show_banner_ad():
    ad_code = """
    <div style="text-align:center; margin: 10px 0;">
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    components.html(ad_code, height=110)

inject_ad_scripts()

# --- PAYMENT CONFIG ---
gpay_number = "7094914276"
upi_url = f"upi://pay?pa={gpay_number}@okicici&pn=Royal%20PDF%20Product&cu=INR"

# --- SIDEBAR ---
st.sidebar.title("🛠️ Menu")
app_mode = st.sidebar.radio("Go To", ["Merge PDFs", "Split PDF", "Organize Pages", "👑 Premium Plan"])

st.sidebar.markdown("---")

# --- ADDED: COFFEE BUTTON ---
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: black; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; border: 2px solid black;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- PAGES ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Premium Upgrade")
    st.write("Unlock all features and remove ads.")
    st.markdown(f'''
        <a href="{upi_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #34a853; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 20px;">
                🚀 Pay ₹99 via GPay
            </div>
        </a>
    ''', unsafe_allow_html=True)

else:
    show_banner_ad()
    st.title(f"🚀 {app_mode}")
    
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("Merge"):
            merged_doc = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc:
                    merged_doc.insert_pdf(doc)
            st.download_button("Download", data=merged_doc.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("Split"):
            doc = fitz.open(stream=file.getvalue(), filetype="pdf")
            for i in range(len(doc)):
                new_pdf = fitz.open()
                new_pdf.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Download Page {i+1}", data=new_pdf.tobytes(), file_name=f"page_{i+1}.pdf")
