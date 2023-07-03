import numpy as np
import matplotlib.pyplot as plt
from black_scholes import black_scholes


class Loan:
    def __init__(self, collateral, loan_amount, interest_rate, maturity, strike_price):
        self.collateral = collateral
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate
        self.maturity = maturity
        self.strike_price = strike_price
        self.value_over_time = []


class LendingPool:
    def __init__(self):
        self.deposits = 0
        self.loans = []

    def deposit(self, amount):
        self.deposits += amount

    def issue_loan(
        self,
        collateral,
        interest_rate,
        maturity,
        loan_to_value=0.75,
        liquidation_ratio=0.8,
        safety_margin=0.05,
    ):
        loan_amount = collateral * loan_to_value
        if self.deposits < loan_amount:
            raise ValueError("Not enough funds in the pool to issue this loan.")
        self.deposits -= loan_amount
        liquidation_value = collateral * liquidation_ratio
        strike_price = liquidation_value * (1 + safety_margin)
        loan = Loan(collateral, loan_amount, interest_rate, maturity, strike_price)
        self.loans.append(loan)
        return loan

    def simulate(
        self, num_days, last_price, volatility, expected_return, num_simulations
    ):
        for x in range(num_simulations):
            daily_returns = np.exp(
                (expected_return - 0.5 * volatility**2) / num_days
                + volatility * np.random.normal(0, 1, num_days) / np.sqrt(num_days)
            )
            price_series = last_price * np.cumprod(daily_returns)
            for loan in self.loans:
                loan.value_over_time = (
                    []
                )  # Reset the value_over_time list at the start of each simulation
                option_price = black_scholes(
                    price_series,
                    loan.strike_price,
                    loan.maturity,
                    loan.interest_rate,
                    volatility,
                    option_type="put",
                )
                num_contracts = (
                    loan.collateral / 1
                )  # Deribit options contracts are for 1 ETH
                total_option_value = (
                    option_price * price_series * num_contracts
                )  # Multiply by the price of ETH to get the total value in USD
                loan_value = price_series * loan.collateral + total_option_value
                loan.value_over_time.append(loan_value)
            plt.figure(1)
            plt.plot(price_series)
            plt.figure(2)
            plt.plot(np.arange(num_days), np.array(loan.value_over_time).flatten())
        plt.show()


# Create a lending pool
pool = LendingPool()

# Deposit funds into the pool
pool.deposit(100000)

# Issue a loan
loan = pool.issue_loan(collateral=50000, interest_rate=0.05, maturity=1)

# Simulate the ETH price and track the value of the loan
pool.simulate(
    num_days=365,
    last_price=1957,
    volatility=0.4,
    expected_return=0.05,
    num_simulations=1,
)
