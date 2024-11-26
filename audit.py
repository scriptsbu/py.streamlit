import streamlit as st
import pandas as pd

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(export_df, employees_df):
    """Compare access from the export against current employees."""
    # Normalize column names for comparison
    export_df.columns = export_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()
    
    # Define relevant columns based on expected structure
    export_keys = ['username', 'name', 'type of license', 'active']  # Adjust based on your export structure
    export_access = export_df[export_keys]

    # Remove users not in the current employee list
    valid_employees = set(employees_df['username'].str.strip().str.lower())

    # Check access from the export
    invalid_users = export_access[~export_access['username'].str.strip().str.lower().isin(valid_employees)]

    return invalid_users

def main():
    st.title("Software License and Access Audit")

    # Upload files
    export_file = st.file_uploader("Upload Software Export CSV (Adobe or Avigilon)", type='csv')
    employees_file = st.file_uploader("Upload Current Employees CSV", type='csv')

    if export_file and employees_file:
        if st.button("Execute Audit"):
            # Load data
            export_df = load_csv(export_file)
            employees_df = load_csv(employees_file)
            
            # Compare access
            invalid_users = compare_access(export_df, employees_df)
            
            # Display results
            st.subheader("Users with Invalid Access:")
            st.dataframe(invalid_users)
    
if __name__ == "__main__":
    main()
