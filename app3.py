import streamlit as st
import fitz  # PyMuPDF
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config - Wide mode for PC
st.set_page_config(page_title="Royal PDF Master | Professional", page_icon="📑", layout="wide")

# --- 🚀 AD ENGINE (For Phone/General Bypass) ---
def show_ads():
    ad_html = """
    <div style="background-color: #ffffff; border: 1px solid #eee; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;">
        <p style="font-size: 11px; color: #999; margin-bottom: 10px;">SPONSORED CONTENT</p>
        <script async="async" data-cfasync="false" src="https://pl28481996.effectivegatecpm.com/91c31c4db3f1171ac7807f880c080828/invoke.js"></script>
        <div id="container-91c31c4db3f1171ac7807f880c080828"></div>
    </div>
    """
    components.html(ad_html, height=260)

# --- 💰 SIDEBAR & BRANDING ---
st.sidebar.title("📑 Royal PDF Master")
st.sidebar.caption("Enterprise v2.8")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize Pages", "Images to PDF", "👑 Premium Plan"])

st.sidebar.markdown("---")
upi_url = "upi://pay?pa=7094914276@okicici&pn=Royal%20PDF&cu=INR"
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank">
        <div style="background:#FFDD00; color:black; padding:12px; border-radius:10px; text-align:center; font-weight:bold; border: 2px solid black;">
            ☕ Support Free Tools
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 🚀 MAIN APP INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #1e88e5;'>Professional PDF Toolkit</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Secure & High-Speed Document Processing</p>", unsafe_allow_html=True)

if app_mode == "👑 Premium Plan":
    st.title("👑 Royal Premium")
    st.info("Ad-free experience and higher priority processing for larger files.")
    st.markdown(f'<a href="{upi_url}"><button style="width:100%; height:60px; background:#28a745; color:white; border-radius:12px; font-weight:bold; font-size:18px; border:none; cursor:pointer;">Upgrade to Premium - ₹99</button></a>', unsafe_allow_html=True)

else:
    # Ads (Phone-la varum, PC-la load aagalana box theryadhu)
    show_ads()
    
    st.write("---")
    st.header(f"🛠️ {app_mode}")

    # --- TOOLS LOGIC ---
    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload files to merge", type="pdf", accept_multiple_files=True)
        if files and st.button("Merge Now"):
            doc_out = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc_in:
                    doc_out.insert_pdf(doc_in)
            st.success("Documents Merged!")
            st.download_button("📥 Download PDF", data=doc_out.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF to split", type="pdf")
        if file and st.button("Extract Pages"):
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
            if st.button("Apply Order"):
                indices = [int(x.split(" ")[1]) - 1 for x in sorted_items]
                doc.select(indices)
                st.download_button("📥 Download Ordered PDF", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        imgs = st.file_uploader("Upload Images", type=["jpg","png","jpeg"], accept_multiple_files=True)
        if imgs and st.button("Convert to PDF"):
            out = fitz.open()
            for img in imgs:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                out.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download PDF", data=out.tobytes(), file_name="converted.pdf")

# --- 📜 OFFICIAL FOOTER (Company Look) ---
st.write("")
st.write("")
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns(3)
with f_col1:
    st.markdown("**Legal**")
    st.caption("Privacy Policy")
    st.caption("Terms of Service")
with f_col2:
    st.markdown("**Security**")
    st.caption("Files are processed locally and never stored on our servers.")
    st.caption("SSL Encrypted Transfer")
with f_col3:
    st.markdown("**Support**")
    st.caption("Help Center")
    st.caption("Contact: 7094914276")

st.markdown("<p style='text-align: center; color: #999; font-size: 10px;'>© 2026 Royal PDF Master | All Rights Reserved.</p>", unsafe_allow_html=True)
