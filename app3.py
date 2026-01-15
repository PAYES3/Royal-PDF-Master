import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master | Enterprise Edition", page_icon="📑", layout="wide")

# --- 🚀 STABLE AD ENGINE ---
def inject_pc_ads(label="PARTNER CONTENT"):
    ad_html = f"""
    <div style="background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 12px; padding: 20px; text-align: center; margin: 15px auto; max-width: 1050px;">
        <p style="font-family: sans-serif; font-size: 11px; color: #adb5bd;">{label}</p>
        <div style="min-height: 250px; display: flex; justify-content: center; align-items: center;">
            <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
            <div id="container-91c31c4db3f1171ac7807f880c080828" style="width:100%;"></div>
        </div>
    </div>
    """
    components.html(ad_html, height=310, scrolling=False)

# --- 💰 SIDEBAR ---
st.sidebar.title("📑 Royal PDF Master")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])

# --- 🚀 MAIN APP ---
st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Professional PDF Toolkit</h1>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Premium Plan")
    st.write("Upgrade for ad-free experience.")
else:
    with st.container():
        inject_pc_ads("OFFICIAL PARTNER")
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- 1. MERGE PDFS (Preview All Uploaded Files) ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files:
            st.write("### 📂 Files to be Merged")
            for f in files:
                with st.expander(f"👁️ Preview: {f.name}"):
                    doc = fitz.open(stream=f.read(), filetype="pdf")
                    cols = st.columns(5)
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
                        cols[page_num % 5].image(pix.tobytes(), caption=f"Pg {page_num+1}")
                    f.seek(0)
            
            if st.button("🔗 Merge Now"):
                doc_out = fitz.open()
                for f in files:
                    with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                        doc_out.insert_pdf(doc_in)
                st.download_button("📥 Download Merged PDF", data=doc_out.tobytes(), file_name="merged.pdf")

    # --- 2. SPLIT PDF (Preview All Pages) ---
    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            st.write(f"### 📑 Document Preview ({len(doc)} Pages)")
            
            # Grid display for all pages
            cols = st.columns(6)
            for i in range(len(doc)):
                page = doc.load_page(i)
                pix = page.get_pixmap(matrix=fitz.Matrix(0.2, 0.2))
                cols[i % 6].image(pix.tobytes(), caption=f"Page {i+1}")
            
            if st.button("✂️ Split & Download All"):
                for i in range(len(doc)):
                    new = fitz.open(); new.insert_pdf(doc, from_page=i, to_page=i)
                    st.download_button(f"Download Page {i+1}", data=new.tobytes(), file_name=f"page_{i+1}.pdf", key=f"dl_{i}")

    # --- 3. ORGANIZE PAGES (Visual Reorder) ---
    elif app_mode == "Organize Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            st.write("### 🔄 Reorder Pages")
            
            # Pre-generating page thumbnails for clarity
            page_labels = []
            for i in range(len(doc)):
                page_labels.append(f"Page {i+1}")
                with st.sidebar: # Temporary thumbnails in sidebar for reference
                    p = doc.load_page(i)
                    st.image(p.get_pixmap(matrix=fitz.Matrix(0.15, 0.15)).tobytes(), caption=f"Page {i+1}")
            
            sorted_items = sort_items(page_labels, direction="horizontal")
            
            if st.button("🚀 Apply & Download"):
                indices = [int(x.split(" ")[1]) - 1 for x in sorted_items]
                doc.select(indices)
                st.download_button("📥 Download PDF", data=doc.tobytes(), file_name="organized.pdf")

    # --- 4. IMAGES TO PDF ---
    elif app_mode == "Images to PDF":
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs:
            st.write("### 🖼️ Image Sequence Preview")
            cols = st.columns(5)
            for idx, img in enumerate(imgs):
                cols[idx % 5].image(img, caption=f"Image {idx+1}", use_container_width=True)
            
            if st.button("🖼️ Convert to PDF"):
                out = fitz.open()
                for img in imgs:
                    img_data = img.read()
                    img_doc = fitz.open(stream=img_data, filetype=img.name.split(".")[-1])
                    out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
                st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images_to_pdf.pdf")

    # 📢 FOOTER AD
    st.write("---")
    with st.container():
        inject_pc_ads("RECOMMENDED RESOURCES")

# --- 📜 FOOTER ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1: st.caption("© 2026 Royal PDF Master")
with col2: st.caption("Privacy Policy | Security Standards")
with col3: st.caption("Contact Support: 7094914276")
