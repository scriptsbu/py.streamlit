import streamlit as st
from PIL import Image
import io

def resize_image(image, target_size_kb):
    """Resize the image dimensions and quality to be under the target size in KB."""
    # Initial image size check
    img_stream = io.BytesIO()
    image.save(img_stream, format='PNG')
    size_kb = img_stream.tell() / 1024  # Initial size in KB

    # If the image is larger than the target size, resize it
    if size_kb > target_size_kb:
        # Reduce dimensions to half repeatedly until under size
        while size_kb > target_size_kb:
            width, height = image.size
            new_size = (width // 2, height // 2)
            image = image.resize(new_size, Image.ANTIALIAS)
            img_stream = io.BytesIO()
            image.save(img_stream, format='PNG')
            size_kb = img_stream.tell() / 1024  # Check new size

    # Adjust quality to fit the size requirement
    quality = 95
    while quality > 10:
        img_stream = io.BytesIO()
        image.save(img_stream, format='PNG', quality=quality)
        img_stream.seek(0)
        
        size_kb = img_stream.tell() / 1024  # Check the size again

        if size_kb <= target_size_kb:
            break
        quality -= 5  # Decrease quality

    img_stream.seek(0)
    return Image.open(img_stream)

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
        st.image(resized_image, caption="Resized Image", use_column_width=True)

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
