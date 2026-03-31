"""
Helper functions for formatting and calculations.
"""

def format_time(minutes: float) -> str:
    """Format time in minutes to readable string."""
    if minutes < 1:
        return f"{minutes * 60:.1f} secondes"
    elif minutes < 60:
        return f"{minutes:.1f} minutes"
    else:
        hours = minutes / 60
        return f"{hours:.1f} heures"


def format_probability(prob: float) -> str:
    """Format probability as percentage."""
    return f"{prob:.2%}"


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with specified decimals."""
    return f"{num:.{decimals}f}"