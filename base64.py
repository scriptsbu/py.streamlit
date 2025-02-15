import streamlit as st
import base64

# Function to convert image to Base64
def convert_image_to_base64(image_file):
    if image_file is not None:
        # Read the image file
        image_bytes = image_file.read()
        # Encode as Base64
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return base64_string
    return None

# Streamlit app
st.title("PNG to Base64 Converter")

# File uploader
uploaded_file = st.file_uploader("Choose a PNG file", type=["png"])

if uploaded_file is not None:
    base64_string = convert_image_to_base64(uploaded_file)

    if base64_string:
        st.success("Image converted to Base64 successfully!")
        st.text_area("Base64 String:", base64_string, height=300)
        
        # Button to copy the Base64 string to clipboard
        if st.button("Copy to Clipboard"):
            # Use Streamlit's built-in method to copy text
            st.text("Base64 string copied to clipboard!")
            # JavaScript to copy to clipboard
            js = f"""
            <script>
            navigator.clipboard.writeText(`{base64_string}`);
            </script>
            """
            st.markdown(js, unsafe_allow_html=True)
