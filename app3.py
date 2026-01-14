import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
from streamlit_sortables import sort_items
import streamlit.components.v1 as components

# 1. Page Config
st.set_page_config(page_title="Royal PDF Master", page_icon="📑", layout="wide")

# --- 🚀 ADSTERRA ADS LOGIC (Visible Version) ---
def show_top_ad():
    # Top Banner Ad
    ad_html = """
    <div style="text-align:center; min-height: 150px;">
        <script type='text/javascript' src='https://pl28476980.effectivegatecpm.com/3f/ef/4a/3fef4a10ead8e81f2c13e14909da9ce3.js'></script>
    </div>
    """
    components.html(ad_html, height=150)

# --- 💰 PAYMENT CONFIG ---
gpay_number = "7094914276"
# UPI link for direct GPay payment
upi_url = f"upi://pay?pa={gpay_number}@okicici&pn=Royal%20PDF%20Product&cu=INR"

# --- 🛠️ SIDEBAR NAVIGATION ---
st.sidebar.title("📑 Royal PDF Menu")
app_mode = st.sidebar.radio("Select Tool", ["Merge PDFs", "Split PDF", "Organize/Delete Pages", "Images to PDF", "👑 Premium Plan"])

st.sidebar.markdown("---")
# Buy Me a Coffee (Always visible in sidebar)
st.sidebar.markdown(f'''
    <a href="{upi_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: black; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; border: 2px solid black;">
            ☕ Buy Me a Coffee (GPay)
        </div>
    </a>
''', unsafe_allow_html=True)

# --- 👑 PREMIUM PAGE LOGIC ---
if app_mode == "👑 Premium Plan":
    st.title("👑 Royal PDF Premium")
    st.write("Upgrade for ₹99 to remove ads and unlock priority processing.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("✅ No Ads | ✅ Faster Processing | ✅ Support Us")
        st.markdown(f'''
            <a href="{upi_url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #34a853; color: white; padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 20px; border: 2px solid #2d8a45;">
                    🚀 Pay ₹99 via GPay
                </div>
            </a>
        ''', unsafe_allow_html=True)
        st.caption(f"Payment sent to: {gpay_number}")
    
    with col2:
        st.image("https://www.gstatic.com/images/branding/product/2x/google_pay_96dp.png", width=100)

# --- 🚀 TOOLS LOGIC ---
else:
    show_top_ad() # Ads show on top of every tool
    st.title(f"🔥 {app_mode}")

    if app_mode == "Merge PDFs":
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if files and st.button("🔗 Merge All"):
            merged_doc = fitz.open()
            for f in files:
                with fitz.open(stream=f.read(), filetype="pdf") as doc:
                    merged_doc.insert_pdf(doc)
            st.download_button("📥 Download PDF", data=merged_doc.tobytes(), file_name="merged.pdf")

    elif app_mode == "Split PDF":
        file = st.file_uploader("Upload PDF", type="pdf")
        if file and st.button("✂️ Split"):
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
                st.download_button("📥 Download", data=doc.tobytes(), file_name="organized.pdf")

    elif app_mode == "Images to PDF":
        images = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if images and st.button("🖼️ Convert"):
            new_pdf = fitz.open()
            for img in images:
                img_doc = fitz.open(stream=img.read(), filetype=img.name.split(".")[-1])
                new_pdf.insert_pdf(fitz.open("pdf", img_doc.convert_to_pdf()))
            st.download_button("📥 Download", data=new_pdf.tobytes(), file_name="images.pdf")
