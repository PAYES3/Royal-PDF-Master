import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 AD RENDERING FUNCTION ---
def show_ad_unit(label="ADVERTISEMENT"):
    # PC-la bypass panna 'sandbox' attributes and full HTML wrap
    ad_html = f"""
    <div style="background-color: #ffffff; border: 1px solid #eee; border-radius: 10px; padding: 10px; text-align: center; margin: 10px auto; max-width: 1000px; box-shadow: 0px 2px 5px rgba(0,0,0,0.05);">
        <p style="font-family: sans-serif; font-size: 11px; color: #bbb; margin-bottom: 8px;">{label}</p>
        <div style="min-height: 250px; display: flex; justify-content: center;">
            <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
            <div id="container-91c31c4db3f1171ac7807f880c080828" style="width:100%;"></div>
        </div>
    </div>
    """
    # Components.html uses an iframe which isolates the script for better loading on PC
    components.html(ad_html, height=300, scrolling=False)

# --- 💰 SIDEBAR ---
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])
st.sidebar.markdown("---")
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank">
        <div style="background:#FFDD00; color:black; padding:12px; border-radius:10px; text-align:center; font-weight:bold; border: 2px solid black;">
            ☕ Buy Me a Coffee
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
st.markdown("<h1 style='text-align: center;'>📂 Royal PDF Master</h1>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.info("Get an Ad-free experience and unlimited file sizes.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px; border:none; cursor:pointer;">🚀 Pay ₹99 via GPay</button></a>', unsafe_allow_html=True)

else:
    # 📢 TOP AD (Desktop & Mobile)
    show_ad_unit("TOP SPONSORED CONTENT")
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- TOOLS LOGIC ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🔗 Merge Now"):
            doc_out = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                    doc_out.insert_pdf(doc_in)
            st.success("Files Merged Successfully!")
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
                st.download_button("📥 Download", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs and st.button("🖼️ Convert"):
            out = fitz.open()
            for img in imgs:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images.pdf")

    # 📢 BOTTOM AD (Earning boost)
    st.write("---")
    show_ad_unit("RECOMMENDED FOR YOU")
