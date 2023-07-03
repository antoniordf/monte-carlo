import numpy as np
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculate the Black-Scholes price of a European option.

    Parameters:
    S (float): the spot price of the underlying asset.
    K (float): the strike price of the option.
    T (float): the time to expiration of the option, in years.
    r (float): the risk-free interest rate, in decimal.
    sigma (float): the volatility of the underlying asset, in decimal.
    option_type (str): the type of the option. Can be 'call' or 'put'.

    Returns:
    float: the Black-Scholes price of the option.
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the price of the option
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be either 'call' or 'put'.")

    return price
