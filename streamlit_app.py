import streamlit as st
import math

def roundUp(n):
    """Rounds a number up to the nearest integer."""
    return math.ceil(n)

def calculate_event_costs(num_customers, total_event_cost, cancellation_percentage,
                           hourly_rate_min=16, hourly_rate_max=30, hours_per_event=8):
    """Calculates total event costs and cancellation charges."""
    if not isinstance(num_customers, int) or num_customers <= 0:
        return "Error: Number of customers must be a positive integer."
    if num_customers < 10:
        return "Error: Minimum 10 customers required for a group event."
    if not isinstance(total_event_cost, (int, float)) or total_event_cost <= 0:
        return "Error: Total event cost must be a positive number."
    if not isinstance(cancellation_percentage, (int, float)) or not 0 <= cancellation_percentage <= 100:
        return "Error: Cancellation percentage must be between 0 and 100."

    # Auto-calculate the number of employees needed
    if 10 <= num_customers < 20:
        num_employees = 2
    elif 20 <= num_customers < 25:
        num_employees = 3
    elif 25 <= num_customers < 30:
        num_employees = 5
    elif 70 <= num_customers < 71:
        num_employees = 10
    elif num_customers >= 30 and num_customers < 70:
        num_employees = roundUp(num_customers / 6)
    else:
        num_employees = roundUp(num_customers / 6)

    hourly_rate_used = (hourly_rate_min + hourly_rate_max) / 2
    employee_cost = num_employees * hourly_rate_used * hours_per_event
    cancellation_fee = (total_event_cost * cancellation_percentage) / 100
    total_cost = total_event_cost + employee_cost
    total_cancellation_charge = cancellation_fee + employee_cost

    return {
        'num_employees': num_employees,
        'employee_cost': employee_cost,
        'cancellation_fee': cancellation_fee,
        'total_cost': total_cost,
        'total_cancellation_charge': total_cancellation_charge,
        'average_hourly_rate': hourly_rate_used
    }

# Streamlit app layout
st.title("Event Cost Calculator")

# Input fields
num_customers = st.number_input("Number of Customers", min_value=10, step=1)
total_event_cost = st.number_input("Total Event Cost ($)", min_value=0.0, step=100.0)
cancellation_percentage = st.number_input("Cancellation Percentage (%)", min_value=0.0, max_value=100.0, step=0.1)

# Session state for adjusted employees and hourly rate
if 'adjusted_employees' not in st.session_state:
    st.session_state.adjusted_employees = None

if 'adjusted_hourly_rate' not in st.session_state:
    st.session_state.adjusted_hourly_rate = None

# Calculate button
if st.button("Calculate"):
    result = calculate_event_costs(num_customers, total_event_cost, cancellation_percentage)

    # Store the auto-calculated number of employees and hourly rate in session state
    if isinstance(result, dict):
        st.session_state.adjusted_employees = result['num_employees']
        st.session_state.adjusted_hourly_rate = result['average_hourly_rate']
    else:
        st.session_state.adjusted_employees = None
        st.session_state.adjusted_hourly_rate = None

# Allow user to adjust the number of employees
if st.session_state.adjusted_employees is not None:
    adjusted_employees = st.number_input("Adjust Number of Employees", 
                                          value=st.session_state.adjusted_employees, 
                                          min_value=1, 
                                          step=1)

    # Allow user to adjust the average hourly rate
    adjusted_hourly_rate = st.number_input("Adjust Average Hourly Rate ($)", 
                                            value=st.session_state.adjusted_hourly_rate, 
                                            min_value=0.0, 
                                            step=0.1)

    # Calculate costs based on adjusted number of employees and hourly rate
    adjusted_employee_cost = adjusted_employees * adjusted_hourly_rate * 8  # Assuming 8 hours per event
    cancellation_fee = (total_event_cost * cancellation_percentage) / 100
    total_cost = total_event_cost + adjusted_employee_cost
    total_cancellation_charge = cancellation_fee + adjusted_employee_cost

    # Display adjusted results
    st.subheader("Adjusted Calculation Results:")
    st.write(f"Adjusted number of employees: {adjusted_employees}")
    st.write(f"Adjusted average hourly rate: ${adjusted_hourly_rate:.2f}")
    st.write(f"Total employee cost with adjustments: ${adjusted_employee_cost:.2f}")
    st.write(f"Event Cancellation Fee: ${cancellation_fee:.2f}")
    st.write(f"Total Cancellation Charge (employee + event): ${total_cancellation_charge:.2f}")
