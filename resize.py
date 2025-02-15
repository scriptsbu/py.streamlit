import streamlit as st
from PIL import Image
import io

def resize_image(image, target_size_kb):
    """Resize the image to be under the target size in KB."""
    img_stream = io.BytesIO()
    quality = 95  # Start quality a bit lower to avoid too much iteration
    while True:
        # Save the image to the BytesIO stream
        image.save(img_stream, format='PNG', quality=quality)
        img_stream.seek(0)
        
        # Check the size of the image
        size_kb = img_stream.tell() / 1024  # Convert bytes to KB
        
        if size_kb <= target_size_kb or quality <= 10:
            break
            
        quality -= 5  # Decrease quality to reduce size
        
        # Prevent infinite loop by checking if quality is too low
        if quality <= 0:
            st.error("Unable to compress image below 500 KB. Try a smaller image.")
            return None
    
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
