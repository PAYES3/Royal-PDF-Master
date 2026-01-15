import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master | Enterprise Edition", page_icon="📑", layout="wide")

# --- 🚀 DOUBLE AD ENGINE ---
def inject_ad(label="PARTNER CONTENT", unique_id="top"):
    # Container ID-a unique-ah maathuna dhaan rendu ad-um varum
    div_id = f"container-91c31c4db3f1171ac7807f880c080828-{unique_id}"
    
    ad_html = f"""
    <div style="background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 12px; padding: 15px; text-align: center; margin: 10px auto; max-width: 1050px;">
        <p style="font-family: Arial; font-size: 11px; color: #adb5bd; margin-bottom: 10px;">{label}</p>
        <div id="{div_id}">
            <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
        </div>
    </div>
    """
    components.html(ad_html, height=280)

# --- 💰 SIDEBAR & BRANDING ---
st.sidebar.title("📑 Royal PDF Master")
st.sidebar.caption("v2.5 Professional Edition")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])

st.sidebar.markdown("---")
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank">
        <div style="background:#FFDD00; color:black; padding:12px; border-radius:10px; text-align:center; font-weight:bold; border: 2px solid black; cursor: pointer;">
            ☕ Support Development
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Professional PDF Toolkit</h1>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Premium Subscription")
    st.write("Remove all advertisements and increase limits.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px; border:none; cursor:pointer;">Upgrade Now - ₹99</button></a>', unsafe_allow_html=True)

else:
    # 📢 HEADER AD (Unique ID: 'header')
    inject_ad("OFFICIAL PARTNER", "header")
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- TOOLS LOGIC ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Choose multiple PDF files", type="pdf", accept_multiple_files=True)
        if files and st.button("Merge Files"):
            doc_out = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                    doc_out.insert_pdf(doc_in)
            st.success("Successfully Merged!")
            st.download_button("📥 Download PDF", data=doc_out.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("Start Splitting"):
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for i in range(len(doc)):
                new = fitz.open(); new.insert_pdf(doc, from_page=i, to_page=i)
                st.download_button(f"Page {i+1}", data=new.tobytes(), file_name=f"p{i+1}.pdf")

    elif app_mode == "Organize Pages":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file:
            doc = fitz.open(stream=file.read(), filetype="pdf")
            items = [f"Page {i+1}" for i in range(len
