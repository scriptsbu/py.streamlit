import streamlit as st
import pandas as pd

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(export_df, employees_df, identifier_col):
    """Compare access from the export against current employees using the identifier."""
    # Normalize column names for comparison
    export_df.columns = export_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()
    
    # Ensure the identifier column exists
    if identifier_col not in export_df.columns:
        st.error(f"Identifier column '{identifier_col}' not found in the export file.")
        return None

    # Get the users from the export file
    export_users = set(export_df[identifier_col].str.strip().str.lower())
    
    # Get the valid employees from the current employees list
    valid_employees = set(employees_df['username'].str.strip().str.lower())  # Assuming 'username' as identifier in employees

    # Identify users who are in the export but not in the employee list
    invalid_users = export_users.difference(valid_employees)

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
        
        # Allow the user to specify which column to use as an identifier (e.g., email)
        identifier_col = st.text_input("Enter the column name for user identification (e.g., email):", value="email").strip().lower()

        if st.button("Execute Audit"):
            # Compare access
            invalid_users = compare_access(export_df, employees_df, identifier_col)
            
            if invalid_users is not None:
                # Display results
                st.subheader("Users with Invalid Access:")
                st.write(", ".join(invalid_users) if invalid_users else "All users are valid.")

if __name__ == "__main__":
    main()
