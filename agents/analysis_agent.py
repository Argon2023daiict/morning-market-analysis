def interpret_allocation(current, previous):
    change = current - previous
    trend = "increased" if change > 0 else "decreased"
    return f"Your Asia tech stake is {current}%, which has {trend} by {abs(change)}% since yesterday."
