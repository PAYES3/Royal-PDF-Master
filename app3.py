import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 FORCE AD INJECTION (Full HTML Mode) ---
def show_force_ads():
    # Indha HTML code, browser-a idhu oru thani website nu namba vaikkum
    # Adhanaala script block aagama run aagum
    ad_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                margin: 0; 
                padding: 0; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                background-color: #f8f9fa;
                overflow: hidden; 
            }
            .ad-container {
                text-align: center;
                border: 2px dashed #007bff;
                padding: 10px;
                border-radius: 10px;
                background: white;
                width: 95%;
            }
            p { font-family: Arial, sans-serif; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class="ad-container">
            <p>🔴 <b>Support Us:</b> Ad Loading...</p>
            
            <script type="text/javascript">
                atOptions = {
                    'key' : '47814c075272639cd29456ec395859e2',
                    'format' : 'iframe',
                    'height' : 250,
                    'width' : 300,
                    'params' : {}
                };
            </script>
            <script type="text/javascript" src="https://pl28477503.effectivegatecpm.com/47/81/4c/47814c075272639cd29456ec395859e2.js"></script>
            </div>
    </body>
    </html>
    """
    
    # Inga height-a correct-a 280px vekkuren, appo dhaan ad cut aagathu
    components.html(ad_html, height=280, scrolling=False)

# --- 💰 PAYMENT & SIDEBAR ---
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])
st.sidebar.markdown("---")
st.sidebar.markdown(f'<a href="{upi_url}" target="_blank"><div style="background:#FFDD00; color:black; padding:10px; border-radius:8px; text-align:center; font-weight:bold; border:2px solid black;">☕ Buy Me a Coffee</div></a>', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px;">🚀 Pay ₹99 via GPay</button></a>', unsafe_allow_html=True)

else:
    # 1. Ad Layout-a Mela Kaatrom
    show_force_ads()
    
    st.title(f"📂 {app_mode}")

    # --- TOOLS LOGIC ---
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
                st.download_button("📥 Download", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs and st.button("🖼️ Convert"):
            out = fitz.open()
            for img in imgs:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="images.pdf")
