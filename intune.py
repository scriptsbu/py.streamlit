import streamlit as st
import subprocess
import os

# Define the URL of the shell script
SCRIPT_URL = "https://github.com/scriptsbu/py.streamlit/raw/refs/heads/main/intune.sh"
SCRIPT_FILE = "intune.sh"

st.title("Install Company Portal")

if st.button("Install Company Portal"):
    with st.spinner("Downloading and installing..."):
        # Download the shell script
        try:
            result = subprocess.run(['curl', '-L', '-o', SCRIPT_FILE, SCRIPT_URL], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            st.error(f"Failed to download the script: {e}")
            st.stop()
        
        # Make the script executable
        os.chmod(SCRIPT_FILE, 0o755)

        # Run the shell script
        try:
            subprocess.run(['sudo', './' + SCRIPT_FILE], check=True)
            st.success("Company Portal installed successfully!")
        except subprocess.CalledProcessError as e:
            st.error(f"Error during installation: {e}")
            st.stop()
        
        # Clean up by removing the script after execution
        os.remove(SCRIPT_FILE)

st.write("Press the button above to install the Company Portal.")
