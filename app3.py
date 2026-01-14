import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items

# Page Config
st.set_page_config(page_title="PDF Master Pro", page_icon="📑", layout="wide")

# --- REUSABLE PREVIEW FUNCTION (PERUSA MATHIYACHU) ---
def show_pdf_preview(file_bytes, key_prefix):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        st.write(f"🔍 **Big Preview (Total Pages: {len(doc)})**")
        
        # Displaying pages in a larger format (2 per row for better visibility)
        num_previews = min(len(doc), 4) # Showing first 4 pages
        cols = st.columns(2) # 2 columns makes the images bigger
        for i in range(num_previews):
            page = doc.load_page(i)
            # Zoom increase panniyachu (1.0 is standard size)
            pix = page.get_pixmap(matrix=fitz.Matrix(0.8, 0.8)) 
            img = Image.open(io.BytesIO(pix.tobytes()))
            cols[i % 2].image(img, caption=f"Page {i+1}", use_container_width=True)
    except Exception as e:
        st.error("Could not generate preview.")

# --- MAIN INTERFACE ---
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select a Tool", 
    ["Merge PDFs", "Split PDF", "Organize/Delete Pages", "Images to PDF"])

st.title(f"🚀 PDF {app_mode}")

# 1. MERGE PDFs
if app_mode == "Merge PDFs":
    files = st.file_uploader("Upload PDFs to Combine", type="pdf", accept_multiple_files=True)
    if files:
        for idx, f in enumerate(files):
            with st.expander(f"📄 View File: {f.name}", expanded=True):
                show_pdf_preview(f.getvalue(), f"merge_{idx}")
        
        if st.button("🔗 Merge All Files"):
            merged_doc = fitz.open()
            for f in files:
                f.seek(0)
                with fitz.open(stream=f.read(), filetype="pdf") as doc:
                    merged_doc.insert_pdf(doc)
            st.download_button("📥 Download Merged PDF", data=merged_doc.tobytes(), file_name="merged.pdf")

# 2. SPLIT PDF
elif app_mode == "Split PDF":
    file = st.file_uploader("Upload PDF to Split", type="pdf")
    if file:
        file_bytes = file.getvalue()
        show_pdf_preview(file_bytes, "split")
        
        if st.button("✂️ Split into Single Pages"):
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for i in range(len(doc)):
                new_pdf = fitz.open()
                new_pdf.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Download Page {i+1}", data=new_pdf.tobytes(), file_name=f"page_{i+1}.pdf")

# 3. ORGANIZE / DELETE PAGES
elif app_mode == "Organize/Delete Pages":
    file = st.file_uploader("Upload PDF", type="pdf")
    if file:
        file_bytes = file.getvalue()
        
        # Preview expanded-ah vechukkalam
        with st.expander("🖼️ Click to See Original Pages", expanded=True):
            show_pdf_preview(file_bytes, "org")
        
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        page_items = [f"Page {i+1}" for i in range(len(doc))]
        
        st.subheader("🖱️ Drag & Drop to Reorder")
        sorted_items = sort_items(page_items, direction="horizontal")
        
        if st.button("🚀 Apply Reorder & Download"):
            try:
                new_indices = [int(item.split(" ")[1]) - 1 for item in sorted_items]
                output_doc = fitz.open(stream=file_bytes, filetype="pdf")
                output_doc.select(new_indices)
                st.download_button("📥 Download Result", data=output_doc.tobytes(), file_name="organized.pdf")
            except Exception as e:
                st.error(f"Error: {e}")

# 4. IMAGES TO PDF
elif app_mode == "Images to PDF":
    images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    if images:
        st.write("🖼️ **Large Image Previews**")
        img_cols = st.columns(2)
        for idx, img in enumerate(images):
            img_cols[idx % 2].image(img, use_container_width=True, caption=img.name)
            
        if st.button("🖼️ Convert Images to PDF"):
            new_pdf = fitz.open()
            for img in images:
                img_data = img.read()
                img_doc = fitz.open(stream=img_data, filetype=img.name.split(".")[-1])
                pdf_bytes = img_doc.convert_to_pdf()
                img_pdf = fitz.open("pdf", pdf_bytes)
                new_pdf.insert_pdf(img_pdf)
            st.download_button("📥 Download Image PDF", data=new_pdf.tobytes(), file_name="images_to_pdf.pdf")