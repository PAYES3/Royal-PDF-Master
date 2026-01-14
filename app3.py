import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 ADSTERRA ADS (Fixed URL for PC & Mobile) ---
def show_ads_top():
    # PC-la nalla therya 728x90 format script-a direct-ah inject pandrom
    ad_code = """
    <div style="text-align:center; margin: 10px 0; min-height: 100px;">
        <script type="text/javascript">
            atOptions = {
                'key' : '3fef4a10ead8e81f2c13e14909da9ce3',
                'format' : 'iframe',
                'height' : 90,
                'width' : 728,
                'params' : {}
            };
        </script>
        <script type="text/javascript" src="//www.highperformancegate.com/3fef4a10ead8e81f2c13e14909da9ce3/invoke.js"></script>
    </div>
    """
    components.html(ad_code, height=120)

# --- 💰 PAYMENT & PREMIUM CONFIG ---
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

# Coffee Button (Direct GPay)
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: black; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; border: 2px solid black;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🖼️ REUSABLE PREVIEW FUNCTION (The Original Logic) ---
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
    st.info("Upgrade for ₹99 to remove ads and process large files instantly.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'''
            <a href="{upi_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #34a853; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 20px;">
                    🚀 Pay ₹99 via GPay
                </div>
            </a>
        ''', unsafe_allow_html=True)
    with col2:
        st.image("https://www.gstatic.com/images/branding/product/2x/google_pay_96dp.png", width=100)

# --- 🚀 MAIN TOOLS (Full 140+ Line Logic) ---
else:
    show_ads_top() # Ads back on top
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
                    st.download_button(f"Download Page {i+1}", data=new_pdf.tob previews=doc.tobytes(), file_name=f"page_{i+1}.pdf")

    elif app_mode == "Organize/Delete Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.getvalue(), filetype="pdf")
            page_items = [f"Page {i+1}" for i in range(len(doc))]
            sorted_items = sort_items(page_items, direction="horizontal")
            if st.button("🚀 Apply Changes & Download"):
                new_indices = [int(item.split(" ")[1]) - 1 for item in sorted_items]
                doc.select(new_indices)
                st.download_button("📥 Download Result", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if images and st.button("🖼️ Convert to PDF"):
            new_pdf = fitz.open()
            for img in images:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                new_pdf.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=new_pdf.tobytes(), file_name="images.pdf")
