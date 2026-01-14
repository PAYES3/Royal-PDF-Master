import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 1. FORCED ADS INJECTION ---
# Banner theryala-na Social Bar popup kandippa mobile-la theryum
def inject_ads():
    ad_html = """
    <div style="background-color: #f1f1f1; border: 1px solid #ccc; text-align: center; padding: 10px; margin-bottom: 20px;">
        <p style="color: #666; font-size: 12px; margin: 0;">Advertisement</p>
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    # Height-a 180-ku ethittaen, appo dhaan PC-la layout space theryum
    components.html(ad_html, height=180)

# --- 💰 PAYMENT & PREMIUM CONFIG ---
gpay_number = "7094914276"
upi_url = f"upi://pay?pa={gpay_number}@okicici&pn=Royal%20PDF%20Product&cu=INR"

# --- 🛠️ SIDEBAR ---
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
    st.info("Upgrade for ₹99 to enjoy ad-free experience.")
    st.markdown(f'''
        <a href="{upi_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #34a853; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 20px;">
                🚀 Pay ₹99 via GPay
            </div>
        </a>
    ''', unsafe_allow_html=True)

# --- 🚀 MAIN TOOLS ---
else:
    # Ads Layout Rendering
    inject_ads()
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
                    with fitz.open(stream=f.read(), filetype="pdf") as doc:
                        merged_doc.insert_pdf(doc)
                st.download_button("📥 Download Merged PDF", data=merged_doc.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            show_pdf_preview(file.getvalue(), "split")
            if st.button("✂️ Split into Single Pages"):
                doc = fitz.open(stream=file.getvalue(), filetype="pdf")
                for i in range(len(doc)):
                    new_pdf = fitz.open()
                    new_pdf.insert_pdf(doc, from_page=i, to_page=i)
                    st.download_button(f"Download Page {i+1}", data=new_pdf.tobytes(), file_name=f"page_{i+1}.pdf")

    elif app_mode == "Organize/Delete Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.getvalue(), filetype="pdf")
            page_items = [f"Page {i+1}" for i in range(len(doc))]
            sorted_items =
