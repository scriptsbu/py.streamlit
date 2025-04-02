import streamlit as st
import subprocess
import os

# Define the URL of the shell script
SCRIPT_URL = "https://github.com/scriptsbu/py.streamlit/raw/refs/heads/main/intune.sh"
SCRIPT_FILE = "intune.sh"

st.title("Install Company Portal")

# Password input (not secure, be cautious)
password = st.text_input("Enter your sudo password (this will not be secure):", type='password')

if st.button("Install Company Portal"):
    with st.spinner("Downloading and installing..."):
        # Download the shell script
        try:
            subprocess.run(['curl', '-L', '-o', SCRIPT_FILE, SCRIPT_URL], check=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to download the script: {e}")
            st.stop()
        
        # Make the script executable
        os.chmod(SCRIPT_FILE, 0o755)

        # Run the shell script with password input
        try:
            result = subprocess.run(['sudo', '-S', './' + SCRIPT_FILE], input=password + '\n', text=True, check=True, capture_output=True)
            st.success("Company Portal installed successfully!")
            st.text(result.stdout)  # Show standard output
        except subprocess.CalledProcessError as e:
            st.error(f"Error during installation: {e}")
            st.text(e.stdout)  # Show standard output
            st.text(e.stderr)  # Show standard error
        
        # Clean up by removing the script after execution
        os.remove(SCRIPT_FILE)

st.write("Press the button above to install the Company Portal.")
