import streamlit as st

def main():
    st.title("Install Company Portal Application")

    # Command to be copied
    command = "bash <(curl -Ls https://github.com/scriptsbu/py.streamlit/raw/refs/heads/main/intune.sh)"

    st.subheader("Step by Step Instructions")
    st.write("To install the Company Portal application, please follow these steps:")

    st.write("1. **Copy the command below:**")
    
    # Display the command in a code block (non-editable)
    st.code(command, language="bash")

    # Copy command button (informational)
    #if st.button("Click to Copy Command"):
    #    st.success("Please select the command above to copy it to your clipboard.")

    st.write("2. **Open the Terminal app** on your macOS.")
    st.write("3. **Paste the command** you copied into the Terminal window.")
    st.write("4. **Hit the Enter key.**")
    st.write("5. **Enter your credentials** if prompted.")

if __name__ == "__main__":
    main()
