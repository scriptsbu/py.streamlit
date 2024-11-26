import streamlit as st
import pandas as pd
import io

def load_csv(uploaded_file):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(uploaded_file)

def compare_access(export_df, employees_df):
    """Compare users from the export against current employees."""
    # Normalize column names for comparison
    export_df.columns = export_df.columns.str.strip().str.lower()
    employees_df.columns = employees_df.columns.str.strip().str.lower()

    # Extract relevant columns
    export_users = export_df[['username', 'email', 'license']]
    valid_employees = set(zip(employees_df['username'], employees_df['email']))

    # Identify users who are in the export but not in the employee list
    invalid_users = export_users[~export_users.apply(lambda row: (row['username'], row['email']) in valid_employees, axis=1)]

    return invalid_users

def main():
    st.title("Software License and Access Audit")

    # Upload files
    export_file = st.file_uploader("Upload Software Export CSV (i.e Adobe, Avigilon, MS 365)", type='csv')
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
            
            if not invalid_users.empty:
                # Display results
                st.subheader("Users with Invalid Access:")
                st.write(invalid_users)

                # Create CSV export of invalid users
                csv = invalid_users.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Invalid Users as CSV",
                    data=csv,
                    file_name='invalid_users.csv',
                    mime='text/csv'
                )
            else:
                st.subheader("All users are valid.")

if __name__ == "__main__":
    main()
