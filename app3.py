import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- ADSTERRA & REVENUE LOGIC ---
def inject_ad_scripts():
    # UNGA SOCIAL BAR SCRIPT INGA DHAAN VARUDHU
    social_bar_script = """
    <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    """
    components.html(social_bar_script, height=0)

def show_banner_ad():
    # Real Ad Banner Space
    # Neenga Adsterra-la "Banner" unit create panni andha code-a inga paste pannalaam
    ad_code = """
    <div style="text-align:center; margin: 10px 0; background:#f9f9f9; padding:15px; border-radius:10px; border:1px dashed #bbb;">
        <p style="font-size: 11px; color: gray; margin-bottom: 8px;">SPONSORED CONTENT</p>
        <div style="font-weight:bold; color:#007bff;">Ad Loading... (Verify in Mobile)</div>
    </div>
    """
    components.html(ad_code, height=130)

# Injecting the background ad script
inject_ad_scripts()

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
# High Earning Direct Link (Using your script URL for now, but better to use a real Direct Link)
direct_link = "https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js" 
st.sidebar.markdown(f'''
    <a href="{direct_link}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #007bff; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; border: 2px solid #0056b3;">
            🚀 Get Premium Features
        </div>
    </a>
    ''', unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("☕ Support Project")
upi_id = "mohamedpayes9@okicici" # Verified from your previous chat
st.sidebar.markdown(f'<a href="upi://pay?pa={upi_id}&pn=RoyalPDF&cu=INR" class="buy-coffee">☕ Buy Me a Coffee (UPI)</a>', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
show_banner_ad() # Ad shows at the very top
st.title(f"🚀 Royal PDF {app_mode}")

# --- TOOLS LOGIC ---
if app_mode == "Merge PDFs":
    files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if files:
        for idx, f in enumerate(files):
            with st.expander(f"📄 View: {f.name}"):
                show_pdf_preview(f.getvalue(), f"merge_{idx}")
        if st.button("🔗 Merge All"):
            merged_doc = fitz.open()
            for f in files:
                f.seek(0)
                with fitz.open(stream=f.read(), filetype="pdf") as doc:
                    merged_doc.insert_pdf(doc)
            st.download_button("📥 Download Result", data=merged_doc.tobytes(), file_name="merged.pdf")

elif app_mode == "Split PDF":
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        show_pdf_preview(file.getvalue(), "split")
        if st.button("✂️ Split PDF"):
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
        sorted_items = sort_items(page_items, direction="horizontal")
        if st.button("🚀 Apply Changes"):
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
        st.download_button("📥 Download Result", data=new_pdf.tobytes(), file_name="images.pdf")
