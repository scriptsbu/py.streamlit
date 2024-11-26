import streamlit as st
import pandas as pd

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(export_df, employees_df, export_keys):
    """Compare access from the export against current employees."""
    # Normalize column names for comparison
    export_df.columns = export_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()
    
    # Filter necessary columns
    try:
        export_access = export_df[export_keys]
    except KeyError as e:
        st.error(f"Error: One or more columns not found in the export file. Missing: {e}")
        return None

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
        # Load data
        export_df = load_csv(export_file)
        employees_df = load_csv(employees_file)
        
        # Display column names for the export file
        st.subheader("Export File Column Names:")
        st.write(export_df.columns.tolist())
        
        # Define expected keys (adjust as needed)
        export_keys = st.text_input("Enter the column names for comparison, separated by commas:",
                                     value="username,name,type of license,active").split(",")

        # Clean up the keys
        export_keys = [key.strip().lower() for key in export_keys]

        if st.button("Execute Audit"):
            # Compare access
            invalid_users = compare_access(export_df, employees_df, export_keys)
            
            if invalid_users is not None:
                # Display results
                st.subheader("Users with Invalid Access:")
                st.dataframe(invalid_users)
    
if __name__ == "__main__":
    main()
