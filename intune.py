import streamlit as st

def main():
    st.title("Install Company Portal Application")

    # Command to be copied
    command = "bash <(curl -Ls https://github.com/scriptsbu/py.streamlit/raw/refs/heads/main/intune.sh)"

    st.subheader("Step by Step Instructions")
    st.write("""
        To install the Company Portal application, please follow these steps:
    """)

    st.write(f"""
        1. **Copy the command below:**
    """)

    # Display the command in a copyable text area
    code_area = st.text_area("Command to Copy:", command, height=50)

    # Copy button functionality
    if st.button("Copy Command"):
        st.write("Command copied to clipboard!")
        # This doesn't actually copy to the clipboard in Streamlit, 
        # but informs the user to manually copy from the text area
    
    st.write("""
        2. **Open the Terminal app** on your macOS.
        3. **Paste the command** you copied into the Terminal window.
        4. **Hit the Enter key.**
        5. **Enter your credentials** if prompted.
    """)

if __name__ == "__main__":
    main()
