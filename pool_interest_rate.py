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


def calculate_actual_borrow_rate(Rt, secsperyear):
    ActualAPY = (1 + Rt / secsperyear) ** secsperyear - 1
    return ActualAPY


def calculate_stable_borrow_rate(asset, ratio):
    ratio_o = params[asset]["optimal_stable_to_total_debt_ratio"]
    r0 = params[asset]["base_stable_rate"]
    R_base = params[asset]["stable_rate_slope1"]

    if ratio < ratio_o:
        Rt = r0 + (ratio - ratio_o) / (1 - ratio_o) * R_base
    else:
        print("something went wrong")
    return Rt
