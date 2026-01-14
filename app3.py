import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 1. ADS LAYOUT (Visual Container First) ---
def show_ads_layout():
    # Inga oru border box vekkuraen, appo dhaan layout theryum
    ad_html = """
    <div style="background-color: #f9f9f9; border: 2px dashed #bbb; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;">
        <p style="color: #888; font-size: 12px; margin-bottom: 5px;">Special Offer / Advertisement</p>
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
        </div>
    """
    components.html(ad_html, height=180)

# --- 💰 PAYMENT CONFIG ---
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"

# --- 🛠️ SIDEBAR ---
st.sidebar.title("🛠️ PDF Tools")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium"])

st.sidebar.markdown("---")
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration:none;">
        <div style="background:#FFDD00; color:black; padding:10px; border-radius:8px; text-align:center; font-weight:bold;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
if app_mode == "👑 Premium":
    st.title("👑 Royal PDF Premium")
    st.info("Upgrade for ₹99 to remove ads permanently.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:50px; background:green; color:white; border-radius:10px; font-weight:bold;">🚀 Pay ₹99 via GPay</button></a>', unsafe_allow_html=True)

else:
    # Title-ku mela layout theryum
    show_ads_layout()
    st.title(f"📂 {app_mode}")

    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🔗 Merge"):
            doc_out = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                    doc_out.insert_pdf(doc_in)
            st.download_button("📥 Download PDF", data=doc_out.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("✂️ Split"):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for i in range(len(doc)):
                new = fitz.open()
                new.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Page {i+1}", data=new.tobytes(), file_name=f"page_{i+1}.pdf")

    elif app_mode == "Organize Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            items = [f"Page {i+1}" for i in range(len(doc))]
            sorted_items = sort_items(items, direction="horizontal")
            if st.button("🚀 Apply"):
                indices = [int(x.split(" ")[1]) - 1 for x in sorted_items]
                doc.select(indices)
                st.download_button("📥 Download", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs and st.button("🖼️ Convert"):
            out = fitz.open()
            for img in imgs:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images.pdf")
