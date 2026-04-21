import streamlit as st
from streamlit_paste_button import paste_image_button as paste_button
from PIL import Image
from io import BytesIO
import json
import streamlit.components.v1 as components

from api_calling import text_generator

# ---------------- UI ----------------
st.title("📸 Image To Text Generator")
st.info("Upload an image or press Ctrl+V to paste a screenshot")

# ---------------- Upload ----------------
uploaded_image = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
)

# ---------------- Paste Button ----------------
pasted_image = paste_button("📋 Paste Image")

image = None

# ---------------- Image Source Logic ----------------
if uploaded_image:
    image = Image.open(uploaded_image)

elif pasted_image is not None and pasted_image.image_data is not None:
    try:
        if isinstance(pasted_image.image_data, bytes):
            image = Image.open(BytesIO(pasted_image.image_data))
        else:
            image = pasted_image.image_data
    except Exception:
        st.error("Invalid pasted image")

# ---------------- Preview ----------------
if image:
    st.subheader("🖼️ Preview")
    st.image(image, width=300)

# ---------------- Button ----------------
pressed = st.button("🚀 Convert Image to Text", type="primary")

# ---------------- Main Logic ----------------
if pressed:
    if not image:
        st.error("Please upload or paste an image")
    else:
        with st.container(border=True):
            st.subheader("📄 Extracted Text")

            with st.spinner("AI is extracting text..."):
                generated_text = text_generator(image)
                st.markdown(generated_text)

            # -------- Copy Button (SAFE) --------
            safe_text = json.dumps(generated_text)

            copy_html = f"""
            <button onclick="navigator.clipboard.writeText({safe_text});
                             document.getElementById('copyMsg').style.display='block';"
                    # style="margin-top:10px;
                    #        padding:8px 14px;
                    #        background-color:#4CAF50;
                    #        color:white;
                    #        border:none;
                    #        border-radius:6px;
                    #        cursor:pointer;"
                           >
                #Copy Text
            </button>

           """

            components.html(copy_html, height=80)
