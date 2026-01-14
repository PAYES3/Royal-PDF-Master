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
    # Social Bar Script
    social_bar_script = """
    <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    """
    components.html(social_bar_script, height=0)

def show_banner_ad():
    # Banner Ad Unit (Top of the page)
    ad_code = """
    <div style="text-align:center; margin: 10px 0;">
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    components.html(ad_code, height=110)

inject_ad_scripts()

# --- PAYMENT LINK ---
# Connects directly to your GPay number 7094914276
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF%20Product&cu=INR"

# --- SIDEBAR ---
st.sidebar.title("🛠️ Menu")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages"])

st.sidebar.markdown("---")

# Buy Me a Coffee Button (Sidebar-la eppovum theryum)
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: black; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; border: 2px solid black;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
show_banner_ad() # Real Ads show here
st.title(f"🚀 {app_mode}")

if app_mode == "Merge PDFs":
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files and st.button("Merge PDFs"):
        merged_doc = fitz.open()
        for f in files:
            with fitz.open(stream=f.read(), filetype="pdf") as doc:
                merged_doc.insert_pdf(doc)
        st.download_button("📥 Download Result", data=merged_doc.tobytes(), file_name="merged.pdf")

elif app_mode == "Split PDF":
    file = st.file_uploader("Upload PDF", type="pdf")
    if file and st.button("Split PDF"):
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        for i in range(len(doc)):
            new_pdf = fitz.open()
            new_pdf.insert_pdf(doc, from_page=i, to_page=i)
            st.download_button(f"Download Page {i+1}", data=new_pdf.tobytes(), file_name=f"page_{i+1}.pdf")

elif app_mode == "Organize Pages":
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        page_items = [f"Page {i+1}" for i in range(len(doc))]
        sorted_items = sort_items(page_items, direction="horizontal")
        if st.button("Apply Changes"):
            new_indices = [int(item.split(" ")[1]) - 1 for item in sorted_items]
            doc.select(new_indices)
            st.download_button("📥 Download Result", data=doc.tobytes(), file_name="organized.pdf")
