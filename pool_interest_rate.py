from interest_rate_params import params


def calculate_variable_interest_rate(asset, utilization):
    r_0 = params[asset]["base_variable_rate"]
    u_optimal = params[asset]["optimal_usage"]
    r_slope1 = params[asset]["variable_rate_slope1"]
    r_slope2 = params[asset]["variable_rate_slope2"]

    if utilization <= u_optimal:
        r_t = r_0 + utilization / u_optimal * r_slope1
    else:
        r_t = r_0 + r_slope1 + (utilization - u_optimal) / (1 - u_optimal) * r_slope2
    return r_t


def calculate_actual_borrow_rate(r_t, secsperyear):
    actual_apy = (1 + r_t / secsperyear) ** secsperyear - 1
    return actual_apy


def calculate_stable_borrow_rate(asset, ratio):
    ratio_o = params[asset]["optimal_stable_to_total_debt_ratio"]
    r_0 = params[asset]["base_stable_rate"]
    r_base = params[asset]["stable_rate_slope1"]

    if ratio < ratio_o:
        r_t = r_0 + (ratio - ratio_o) / (1 - ratio_o) * r_base
    else:
        print("something went wrong")
    return r_t
