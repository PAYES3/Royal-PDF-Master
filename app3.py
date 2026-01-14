import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 MOBILE ADS (Munnadi work aana adhe method) ---
def show_ads():
    ad_code = """
    <div style="text-align:center; margin-bottom: 20px;">
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    components.html(ad_code, height=120)

# --- 🛠️ SIDEBAR & GPay ---
st.sidebar.title("🛠️ PDF Tools")
app_mode = st.sidebar.radio("Menu", ["Merge PDFs", "Split PDF", "Organize/Delete", "Images to PDF", "👑 Premium"])

st.sidebar.markdown("---")
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.markdown(f'<a href="{upi_url}"><button style="width:100%; border-radius:10px; background:#FFDD00; font-weight:bold;">☕ Buy Coffee (GPay)</button></a>', unsafe_allow_html=True)

# --- 👑 PREMIUM PAGE ---
if app_mode == "👑 Premium":
    st.title("👑 Royal PDF Premium")
    st.info("Upgrade to ₹99 for No Ads experience.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:50px; background:green; color:white; border-radius:10px;">🚀 Pay via GPay</button></a>', unsafe_allow_html=True)

# --- 🚀 PDF TOOLS ---
else:
    show_ads() # Ads first
    st.title(f"🔥 {app_mode}")

    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🔗 Merge"):
            doc_out = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                    doc_out.insert_pdf(doc_in)
            st.download_button("📥 Download", data=doc_out.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("✂️ Split"):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for i in range(len(doc)):
                new = fitz.open(); new.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Page {i+1}", data=new.tobytes(), file_name=f"p{i+1}.pdf")

    elif app_mode == "Organize/Delete":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            items = [f"Page {i+1}" for i in range(len(doc))]
            sorted_items = sort_items(items, direction="horizontal")
            if st.button("🚀 Apply"):
                indices = [int(x.split(" ")[1]) - 1 for x in sorted_items]
                doc.select(indices)
                st.download_button("📥 Download", data=doc.tobytes(), file_name="fixed.pdf")

    elif app_mode == "Images to PDF":
        images = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if images and st.button("🖼️ Convert"):
            out = fitz.open()
            for img in images:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images.pdf")
