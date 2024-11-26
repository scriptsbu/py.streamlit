import streamlit as st
import pandas as pd

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(export_df, employees_df):
    """Compare users from the export against current employees."""
    # Normalize column names for comparison
    export_df.columns = export_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()

    # Extract relevant columns
    export_users = set(zip(export_df['username'], export_df['email']))
    valid_employees = set(zip(employees_df['username'], employees_df['email']))

    # Identify users who are in the export but not in the employee list
    invalid_users = [user for user in export_users if user not in valid_employees]

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
        
        if st.button("Execute Audit"):
            # Compare access
            invalid_users = compare_access(export_df, employees_df)
            
            if invalid_users:
                # Display results
                st.subheader("Users with Invalid Access:")
                for username, email in invalid_users:
                    st.write(f"Username: {username}, Email: {email}")
            else:
                st.subheader("All users are valid.")

if __name__ == "__main__":
    main()
