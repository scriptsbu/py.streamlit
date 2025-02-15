import streamlit as st
import base64
from PIL import Image
import io

# Function to convert image to Base64
def convert_image_to_base64(image_file):
    if image_file is not None:
        # Read the image file
        image_bytes = image_file.read()
        # Encode as Base64
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        return base64_string
    return None

# Function to resize image
def resize_image(image, target_size_kb=500):
    """Resize the image to be less than target_size_kb."""
    target_size = target_size_kb * 1024  # Convert KB to bytes
    quality = 95  # Start with high quality
    buffer = io.BytesIO()

    while True:
        # Save image to buffer
        buffer.seek(0)
        image.save(buffer, format="PNG", quality=quality)
        if buffer.tell() <= target_size:
            break
        quality -= 5  # Reduce quality to decrease file size
        if quality < 10:  # Ensure quality doesn't go too low
            st.warning("Could not resize the image below the target size.")
            break

    buffer.seek(0)  # Reset buffer position
    return buffer

# Streamlit app
st.title("PNG to Base64 Converter")

# File uploader with a specific size limit
uploaded_file = st.file_uploader("Choose a PNG file (max size: 5 MB)", type=["png"])

if uploaded_file is not None:
    # Check file size
    if uploaded_file.size > 5 * 1024 * 1024:  # 5 MB in bytes
        st.error("File size exceeds 5 MB. Please upload a smaller file.")
    else:
        # Convert file to image
        image = Image.open(uploaded_file)
        
        # Resize if necessary
        if uploaded_file.size > 500 * 1024:  # 500 KB in bytes
            st.warning("File size exceeds 500 KB. Resizing the image...")
            resized_image_buffer = resize_image(image)
            base64_string = convert_image_to_base64(resized_image_buffer)
        else:
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
