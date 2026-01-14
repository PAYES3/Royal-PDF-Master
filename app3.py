import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- AD NETWORK CONFIG ---
def inject_ad_scripts():
    # Header Script (Adsterra / PropellerAds Header Code)
    header_script = """
    """
    components.html(header_script, height=0)

def show_banner_ad():
    # Fixed the variable name here
    ad_code = """
    <div style="text-align:center; margin: 10px 0; background:#f9f9f9; padding:10px; border-radius:8px; border:1px solid #ddd;">
        <p style="font-size: 10px; color: gray; margin-bottom: 5px;">SPONSORED</p>
        <div style="width:100%; height:90px; display:flex; align-items:center; justify-content:center;">
             <span style="color:#999;">Ad Slot (Ready for Adsterra)</span>
        </div>
    </div>
    """
    components.html(ad_code, height=150)

def show_social_bar():
    # Social Bar / Pop-under invisible scripts
    social_script = """
    """
    components.html(social_script, height=0)

# Injecting Scripts
inject_ad_scripts()
show_social_bar()

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .buy-coffee {
        display: flex; justify-content: center; padding: 12px;
        background-color: #FFDD00; color: black !important; text-decoration: none;
        border-radius: 10px; font-weight: bold; border: 2px solid black; margin: 10px 0;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- REUSABLE PREVIEW FUNCTION ---
def show_pdf_preview(file_bytes, key_prefix):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        st.write(f"🔍 **Big Preview (Total Pages: {len(doc)})**")
        num_previews = min(len(doc), 4)
        cols = st.columns(2)
        for i in range(num_previews):
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8)) 
            img = Image.open(io.BytesIO(pix.tobytes()))
            cols[i % 2].image(img, caption=f"Page {i+1}", use_container_width=True)
    except Exception as e:
        st.error("Could not generate preview.")

# --- SIDEBAR ---
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select a Tool", ["Merge PDFs", "Split PDF", "Organize/Delete Pages", "Images to PDF"])

st.sidebar.markdown("---")
show_banner_ad() # Sidebar Ad

st.sidebar.subheader("☕ Support Project")
upi_id = "9876543210@ybl" # Update your ID
st.sidebar.markdown(f'<a href="upi://pay?pa={upi_id}&pn=RoyalPDF&cu=INR" class="buy-coffee">☕ Support with UPI</a>', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title(f"🚀 Royal PDF {app_mode}")
show_banner_ad() # Top Ad

# --- TOOLS LOGIC ---
if app_mode == "Merge PDFs":
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files:
        for idx, f in enumerate(files):
            with st.expander(f"📄 View: {f.name}", expanded=True):
                show_pdf_preview(f.getvalue(), f"merge_{idx}")
        if st.button("🔗 Merge All"):
            merged_doc = fitz.open()
            for f in files:
                f.seek(0)
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
        with st.expander("🖼️ Original Pages", expanded=True):
            show_pdf_preview(file.getvalue(), "org")
        doc = fitz.open(stream=file.getvalue(), filetype="pdf")
        page_items = [f"Page {i+1}" for i in range(len(doc))]
        sorted_items = sort_items(page_items, direction="horizontal")
        if st.button("🚀 Apply & Download"):
            new_indices = [int(item.split(" ")[1]) - 1 for item in sorted_items]
            doc.select(new_indices)
            st.download_button("📥 Download Result", data=doc.tobytes(), file_name="organized.pdf")

elif app_mode == "Images to PDF":
    images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if images:
        img_cols = st.columns(2)
        for idx, img in enumerate(images):
            img_cols[idx % 2].image(img, use_container_width=True)
        if st.button("🖼️ Convert to PDF"):
            new_pdf = fitz.open()
            for img in images:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                new_pdf.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download Image PDF", data=new_pdf.tobytes(), file_name="images.pdf")

# Bottom Ad
st.markdown("---")
show_banner_ad()
