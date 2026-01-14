import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 Pudhu Ad Script Layout ---
def show_new_ad_layout():
    # User-ku theryura maadhiri oru layout box
    # Neenga kudutha pudhu script-a inga inject pannittaen
    ad_html = """
    <div style="background-color: #f0f7ff; border: 2px solid #007bff; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 25px; min-height: 250px;">
        <p style="color: #007bff; font-weight: bold; font-size: 16px; margin-bottom: 15px;">🔗 Sponsored Link / Advertisement</p>
        
        <div id="ad-container">
            <script type='text/javascript' src='https://pl28477503.effectivegatecpm.com/47/81/4c/47814c075272639cd29456ec395859e2.js'></script>
            </div>
        
        <p style="color: #888; font-size: 11px; margin-top: 15px;">Please wait while the advertisement loads...</p>
    </div>
    """
    # height-a 300-ah vechirukkaen, appo dhaan script render aaga free space kedaikkum
    components.html(ad_html, height=300)

# --- 💰 PAYMENT & SIDEBAR ---
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.title("🛠️ PDF Toolkit")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])
st.sidebar.markdown("---")
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank">
        <div style="background:#FFDD00; color:black; padding:12px; border-radius:10px; text-align:center; font-weight:bold; border:2px solid black;">
            ☕ Buy Me a Coffee
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px; cursor:pointer; border:none;">🚀 Pay ₹99 via GPay</button></a>', unsafe_allow_html=True)

else:
    # Pudhu script layout-a mela kaatrom
    show_new_ad_layout()
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
                st.download_button(f"Download Page {i+1}", data=new.tobytes(), file_name=f"p{i+1}.pdf")

    elif app_mode == "Organize Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            items = [f"Page {i+1}" for i in range(len(doc))]
            sorted_items = sort_items(items, direction="horizontal")
            if st.button("🚀 Apply"):
                indices = [int(x.split(" ")[1]) - 1 for x in sorted_items]
                doc.select(indices)
