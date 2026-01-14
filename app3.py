import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 1. ADS LAYOUT (Forcing Load) ---
def show_ads_layout():
    # Inga rendu script-ayum sethu vekkuraen, appo dhaan edhavadhu onnu kandippa theryum
    ad_html = """
    <div style="text-align:center; min-height: 150px;">
        <p style="color: #555; font-size: 10px;">Advertisement</p>
        
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
        
        <script type='text/javascript' src='//pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    # Scrolling True vechaa scripts block aagaadhu
    components.html(ad_html, height=160, scrolling=False)

# --- 💰 PAYMENT CONFIG ---
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"

# --- 🛠️ SIDEBAR ---
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])
st.sidebar.markdown("---")
st.sidebar.markdown(f'<a href="{upi_url}" target="_blank"><button style="width:100%; background:#FFDD00; font-weight:bold; border-radius:8px; padding:10px;">☕ Buy Coffee</button></a>', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold;">🚀 Pay ₹99 via GPay</button></a>', unsafe_allow_html=True)

else:
    # Title-ku mela ad layout load aagum
    show_ads_layout()
    st.title(f"📂 {app_mode}")

    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🔗 Merge Now"):
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
                new = fitz.open(); new.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Page {i+1}", data=new.tobytes(), file_name=f"p{i+1}.pdf")

    elif app_mode == "Organize Pages":
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
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs and st.button("🖼️ Convert"):
            out = fitz.open()
            for img in imgs:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images.pdf")
