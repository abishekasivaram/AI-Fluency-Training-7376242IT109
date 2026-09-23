# tools.py

# Private gym membership data
MEMBERSHIP_PRICES = {
    "Basic": 1000,
    "Standard": 1500,
    "Premium": 2000
}

SERVICE_PRICES = {
    "Personal Trainer": 3000,
    "Diet Plan": 1000,
    "Fitness Assessment": 500
}

DISCOUNTS = {
    3: 10,
    6: 15,
    12: 20
}


def get_membership_price(plan):
    """Return the monthly price of a membership plan."""
    price = MEMBERSHIP_PRICES.get(plan)
    return f"₹{price} per month"


def get_service_price(service):
    """Return the price of an additional service."""
    price = SERVICE_PRICES.get(service)
    return f"₹{price} per month"


def get_discount(months):
    """Return the membership discount for the selected duration."""
    discount = DISCOUNTS.get(months, 0)
    return f"{discount}%"


def calculator(expression):
    """Calculate a mathematical expression."""
    try:
        return eval(expression)
    except Exception:
        return "Invalid calculation"