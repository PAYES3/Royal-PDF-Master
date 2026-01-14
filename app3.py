import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 MOBILE ADS LAYOUT (Old Method) ---
def show_mobile_ads():
    # Direct script for Mobile social bar and banner
    ad_code = """
    <div style="text-align:center; margin-bottom: 20px; min-height: 100px;">
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    components.html(ad_code, height=110)

# --- 💰 PAYMENT & PREMIUM ---
gpay_number = "7094914276"
upi_url = f"upi://pay?pa={gpay_number}@okicici&pn=Royal%20PDF%20Product&cu=INR"

# --- 🛠️ SIDEBAR NAVIGATION ---
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select a Tool", [
    "Merge PDFs", 
    "Split PDF", 
    "Organize/Delete Pages", 
    "Images to PDF", 
    "👑 Premium Plan"
])

st.sidebar.markdown("---")
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: black; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; border: 2px solid black;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🖼️ PDF PREVIEW LOGIC ---
def show_pdf_preview(file_bytes, key_prefix):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        st.write(f"🔍 **Preview (Total Pages: {len(doc)})**")
        num_previews = min(len(doc), 4)
        cols = st.columns(2)
        for i in range(num_previews):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8)) 
            img = Image.open(io.BytesIO(pix.tobytes()))
            cols[i % 2].image(img, use_container_width=True)
    except Exception as e:
        st.error(f"Preview error: {e}")

# --- 👑 PREMIUM PAGE ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.info("Upgrade for ₹99 to enjoy ad-free experience on mobile.")
    st.markdown(f'''
        <a href="{upi_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #34a853; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 20px;">
                🚀 Pay ₹99 via GPay
            </div>
        </a>
    ''', unsafe_allow_html=True)

# --- 🚀 MAIN TOOLS (Fixed Syntax & Colon) ---
else:
    show_mobile_ads() # Ad layout at top
    st.title(f"🚀 Royal PDF {app_mode}")

    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files:
            for idx, f in enumerate(files):
                with st.expander(f"📄 {f.name}"):
                    show_pdf_preview(f.getvalue(), f"merge_{idx}")
            if st.button("🔗 Merge All"):
                merged_doc = fitz.open()
                for f in files:
                    with fitz.open(stream=f.read(), file
