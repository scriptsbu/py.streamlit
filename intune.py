import streamlit as st

def main():
    st.title("Install Company Portal Application")

    # Command to be copied
    command = "bash <(curl -Ls https://github.com/scriptsbu/py.streamlit/raw/refs/heads/main/intune.sh)"

    st.subheader("Step by Step Instructions")
    st.write("To install the Company Portal application, please follow these steps:")

    st.write("1. **Copy the command below:**")

    # Display the command in a text area
    st.text_area("Command to Copy:", command, height=100)

    # Copy command button
    if st.button("Copy Command"):
        # This button will trigger the user to copy the command from the text area
        st.success("Command copied! Please paste it into your Terminal.")

    st.write("2. **Open the Terminal app** on your macOS.")
    st.write("3. **Paste the command** you copied into the Terminal window.")
    st.write("4. **Hit the Enter key.**")
    st.write("5. **Enter your credentials** if prompted.")

if __name__ == "__main__":
    main()
