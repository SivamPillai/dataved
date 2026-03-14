"""Rolling window calculation for trend resampling."""


def calculate_rolling_window(resample_period):
    """
    Calculate the appropriate rolling window based on resampling period.
    Rolling window is 5x the resampling period.

    Args:
        resample_period: The resampling period (None, '1min', '1D', '1M')

    Returns:
        str: The rolling window string for pandas rolling function
    """
    if resample_period is None:
        return "5Min"
    if resample_period == "1min":
        return "5min"
    if resample_period == "1D":
        return "5D"
    if resample_period == "1M":
        return "5M"
    return "5Min"
