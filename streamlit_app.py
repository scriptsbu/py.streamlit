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

# Calculate button
if st.button("Calculate"):
    result = calculate_event_costs(num_customers, total_event_cost, cancellation_percentage)

    # Display results
    if isinstance(result, dict):
        st.subheader("Calculation Results:")
        st.write(f"Auto-calculated number of employees needed: {result['num_employees']}")
        
        # Allow user to adjust the number of employees
        adjusted_employees = st.number_input("Adjust Number of Employees", 
                                              value=result['num_employees'], 
                                              min_value=1, 
                                              step=1)

        # Recalculate costs based on adjusted number of employees
        hourly_rate_used = (16 + 30) / 2  # Average hourly rate
        adjusted_employee_cost = adjusted_employees * hourly_rate_used * 8  # Assuming 8 hours per event
        cancellation_fee = (total_event_cost * cancellation_percentage) / 100
        total_cost = total_event_cost + adjusted_employee_cost
        total_cancellation_charge = cancellation_fee + adjusted_employee_cost

        # Display adjusted results
        st.write(f"Adjusted number of employees: {adjusted_employees}")
        st.write(f"Total employee cost with adjustments: ${adjusted_employee_cost:.2f}")
        st.write(f"Event Cancellation Fee: ${cancellation_fee:.2f}")
        st.write(f"Total Cancellation Charge (employee + event): ${total_cancellation_charge:.2f}")
        st.write(f"Average Hourly Rate: ${hourly_rate_used:.2f}")
    else:
        st.error(result)  # Display error message if any
