import math

def roundUp(n):
  """Rounds a number up to the nearest integer."""
  return math.ceil(n)

def calculate_event_costs(num_customers, total_event_cost, cancellation_percentage, hourly_rate_min=16, hourly_rate_max=30, hours_per_event=8):
    """Calculates total event costs and cancellation charges.

    Args:
        num_customers: The number of customers attending the event.
        total_event_cost: The total cost of the event (excluding employee costs).
        cancellation_percentage: The percentage of the total cost charged for cancellation (e.g., 25 for 25%).
        hourly_rate_min: Minimum hourly employee rate.
        hourly_rate_max: Maximum hourly employee rate.
        hours_per_event: Event duration in hours.

    Returns:
        A dictionary containing:
            - 'num_employees': Number of employees needed.
            - 'employee_cost': Total employee cost.
            - 'cancellation_fee': Cancellation fee.
            - 'total_cost': Total event cost + employee cost.
            - 'total_cancellation_charge': Total cancellation charge (employee + event).
        Returns an error message if input is invalid.

    """
    if not isinstance(num_customers, int) or num_customers <= 0:
        return "Error: Number of customers must be a positive integer."
    if num_customers < 10:
        return "Error: Minimum 10 customers required for a group event."
    if not isinstance(total_event_cost, (int, float)) or total_event_cost <= 0:
        return "Error: Total event cost must be a positive number."
    if not isinstance(cancellation_percentage, (int, float)) or not 0 <= cancellation_percentage <= 100:
        return "Error: Cancellation percentage must be between 0 and 100."


    if 10 <= num_customers < 20:
        num_employees = 2
    elif 20 <= num_customers < 25:
        num_employees = 3
    elif 25 <= num_customers < 30:
        num_employees = 5 # Adjusted for 25-29 customers
    elif 70 <= num_customers < 71:
        num_employees = 10
    elif num_customers >= 30 and num_customers < 70:
        num_employees = roundUp(num_customers / 6) #Adjusted ratio for larger groups
    else:
        num_employees = roundUp(num_customers / 6) #Adjusted ratio for larger groups


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
        'total_cancellation_charge': total_cancellation_charge
    }


# Example Usage
num_customers = 28
total_event_cost = 10000
cancellation_percentage = 25

result = calculate_event_costs(num_customers, total_event_cost, cancellation_percentage)

if isinstance(result, dict):
    print(f"For {num_customers} customers and a total event cost of ${total_event_cost:.2f}:")
    print(f"  Number of employees needed: {result['num_employees']}")
    print(f"  Total employee cost: ${result['employee_cost']:.2f}")
    print(f"  Event Cancellation Fee: ${result['cancellation_fee']:.2f}")
    print(f"  Total Cancellation Charge (employee + event): ${result['total_cancellation_charge']:.2f}")
else:
    print(result) # Print any error messages
