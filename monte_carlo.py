import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes

# Set the parameters
NUM_SIMULATIONS = 1000
NUM_DAYS = 365
LAST_PRICE = 1957  # This should be the current price of ETH
VOLATILITY = 0.4  # This should be the historical VOLATILITY of ETH
EXPECTED_RETURN = 0.00  # This should be the expected return of ETH
NUM_ETH = 50  # Amount of ETH in collateral
NUM_OPTIONS = 50  # Number of options bought
STRIKE_PRICE = 0.8 * LAST_PRICE  # 80% of the starting price
MATURITY = 1  # Maturity of the loan and the option
INTEREST_RATE = 0.05

# Create an empty matrix to hold the end price data
all_simulated_price = np.zeros((NUM_SIMULATIONS, NUM_DAYS))

# Create an empty matrix to hold the portfolio value data
all_simulated_portfolio_value = np.zeros((NUM_SIMULATIONS, NUM_DAYS))

# Set the plot size
plt.figure(figsize=(10, 5))

eth_values = []
portfolio_values = []

# Run the Monte Carlo simulation
for x in range(NUM_SIMULATIONS):
    # Calculate daily returns using GBM formula
    daily_returns = np.exp(
        (EXPECTED_RETURN - 0.5 * VOLATILITY**2) / NUM_DAYS
        + VOLATILITY * np.random.normal(0, 1, NUM_DAYS) / np.sqrt(NUM_DAYS)
    )

    # Calculate price series
    price_series = LAST_PRICE * np.cumprod(daily_returns)

    # Plot each simulation
    plt.figure(1)
    plt.plot(price_series)

    # Append the end price of each simulation to the matrix
    all_simulated_price[x] = price_series[-1]

    # Calculate the value of the ETH holdings each day
    eth_value = NUM_ETH * price_series
    eth_values.append(eth_value)

    # Calculate the value of the put options each day
    options_value = NUM_OPTIONS * black_scholes(
        price_series,
        STRIKE_PRICE,
        MATURITY,
        INTEREST_RATE,
        VOLATILITY,
        option_type="put",
    )

    # Calculate the total value of the portfolio each day
    portfolio_value = eth_value + options_value
    portfolio_values.append(portfolio_value)

    # Append the end value of each simulation to the matrix
    all_simulated_portfolio_value[x] = portfolio_value[-1]

# Convert lists to numpy arrays
eth_values = np.array(eth_values)
portfolio_values = np.array(portfolio_values)

# Calculate the minimum and maximum values across both datasets
min_value = min(np.min(eth_values), np.min(portfolio_values))
max_value = max(np.max(eth_values), np.max(portfolio_values))

# Plot the value of the ETH holdings each day
plt.figure(2)
for eth_value in eth_values:
    plt.plot(eth_value)
plt.ylim([min_value, max_value])  # Set the limits of the y-axis

# Plot the total value of the portfolio each day
plt.figure(3)
for portfolio_value in portfolio_values:
    plt.plot(portfolio_value)
plt.ylim([min_value, max_value])  # Set the limits of the y-axis

# Show the plot
plt.show()

# Output the mean end price
print("Mean final price: ", np.mean(all_simulated_price))

# Output the mean end value
print("Mean final portfolio value: ", np.mean(all_simulated_portfolio_value))
