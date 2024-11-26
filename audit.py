import streamlit as st
import pandas as pd

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(adobe_df, avigilon_df, employees_df):
    """Compare access from Adobe and Avigilon against current employees."""
    # Normalize column names for comparison
    adobe_df.columns = adobe_df.columns.str.strip().str.lower()
    avigilon_df.columns = avigilon_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()
    
    # Define relevant columns based on expected structure
    adobe_keys = ['username', 'name', 'type of license', 'active']
    avigilon_keys = ['username', 'name', 'type of access', 'status']
    
    # Filter necessary columns
    adobe_access = adobe_df[adobe_keys]
    avigilon_access = avigilon_df[avigilon_keys]

    # Remove users not in the current employee list
    valid_employees = set(employees_df['username'].str.strip().str.lower())

    # Check access from Adobe
    adobe_invalid_users = adobe_access[~adobe_access['username'].str.strip().str.lower().isin(valid_employees)]
    
    # Check access from Avigilon
    avigilon_invalid_users = avigilon_access[~avigilon_access['username'].str.strip().str.lower().isin(valid_employees)]

    return adobe_invalid_users, avigilon_invalid_users

def main():
    st.title("Software License and Access Audit")
    
    # Upload files
    adobe_file = st.file_uploader("Upload Adobe Export CSV", type='csv')
    avigilon_file = st.file_uploader("Upload Avigilon Export CSV", type='csv')
    employees_file = st.file_uploader("Upload Current Employees CSV", type='csv')

    if adobe_file and avigilon_file and employees_file:
        # Load data
        adobe_df = load_csv(adobe_file)
        avigilon_df = load_csv(avigilon_file)
        employees_df = load_csv(employees_file)
        
        # Compare access
        adobe_invalid_users, avigilon_invalid_users = compare_access(adobe_df, avigilon_df, employees_df)
        
        # Display results
        st.subheader("Users with Invalid Adobe Access:")
        st.dataframe(adobe_invalid_users)

        st.subheader("Users with Invalid Avigilon Access:")
        st.dataframe(avigilon_invalid_users)

if __name__ == "__main__":
    main()
