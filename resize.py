import streamlit as st
from PIL import Image
import io

def resize_image(image, target_size_kb):
    """Resize the image to be under the target size in KB."""
    # Initial image size check
    img_stream = io.BytesIO()
    image.save(img_stream, format='PNG')
    size_kb = img_stream.tell() / 1024  # Initial size in KB

    # Resize if initial size is larger than target
    if size_kb > target_size_kb:
        # Resize image proportionally
        width, height = image.size
        scaling_factor = (target_size_kb / size_kb) ** 0.5
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Adjust quality to fit the size requirement
    quality = 95
    while quality > 10:
        img_stream = io.BytesIO()
        image.save(img_stream, format='PNG', quality=quality)
        size_kb = img_stream.tell() / 1024  # Check the size again

        if size_kb <= target_size_kb:
            img_stream.seek(0)
            return Image.open(img_stream)
        
        quality -= 5  # Decrease quality

    st.error("Unable to compress image below 500 KB. Try a smaller image.")
    return None

# Streamlit app
st.title("PNG Image Resizer")

uploaded_file = st.file_uploader("Upload a PNG image", type=["png"])

if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)

    # Resize the image to less than 500 KB
    resized_image = resize_image(image, target_size_kb=500)

    if resized_image:
        # Display the resized image
        st.image(resized_image, caption="Resized Image", use_container_width=True)

        # Provide a download link for the resized image
        img_buffer = io.BytesIO()
        resized_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        st.download_button(
            label="Download Resized Image",
            data=img_buffer,
            file_name="resized_image.png",
            mime="image/png"
        )
