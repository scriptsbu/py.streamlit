import streamlit as st
import math

def roundUp(n):
    return math.ceil(n)

def calculate_event_costs(num_customers, total_event_cost, cancellation_percentage):
    # Your calculation logic here...
    # (Copy the function definition from your original code)

st.title("Event Cost Calculator")

num_customers = st.number_input("Number of Customers", min_value=10)
total_event_cost = st.number_input("Total Event Cost", min_value=0.0)
cancellation_percentage = st.number_input("Cancellation Percentage", min_value=0.0, max_value=100.0)

if st.button("Calculate"):
    result = calculate_event_costs(num_customers, total_event_cost, cancellation_percentage)
    st.json(result)
