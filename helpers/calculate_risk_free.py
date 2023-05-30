from helpers.calculate_average_freq import calculate_average_freq


def calculate_risk_free(data):
    print("WARNING -- Risk free assumes a yearly of 5.03%")
    yearly = 0.0503
    minutes_in_year = 525600
    average_minutes = calculate_average_freq(data).total_seconds() / 60
    rate_per_period = yearly * average_minutes / minutes_in_year
    print("done")
    return rate_per_period
