from black_scholes import black_scholes
from option import Option


class Loan:
    def __init__(
        self,
        loan_amount,
        collateral_asset,
        collateral_amount,
        loan_time_to_maturity,
        loan_to_value,
        liquidation_ratio,
        safety_margin,
        lending_pool,
        is_fixed_rate,
    ):
        self.loan_amount = loan_amount
        self.collateral_asset = collateral_asset
        self.collateral_amount = collateral_amount
        self.loan_time_to_maturity = loan_time_to_maturity
        self.loan_to_value = loan_to_value
        self.liquidation_ratio = liquidation_ratio
        self.safety_margin = safety_margin
        self.lending_pool = lending_pool
        self.is_fixed_rate = is_fixed_rate
        self.options = []
        self.portfolio_value = self.calculate_portfolio(self.collateral_asset)

    @property
    def interest_rate(self):
        if self.is_fixed_rate:
            return self.lending_pool.stable_interest_rate

        return self.lending_pool.variable_interest_rate

    def buy_options(
        self,
        num_options,
        strike_price,
        option_time_to_maturity,
        volatility,
        risk_free_rate,
    ):
        option_price = black_scholes(
            self.collateral_asset,
            strike_price,
            option_time_to_maturity,
            risk_free_rate,
            volatility,
            option_type="put",
        )
        cost = num_options * option_price
        if cost > self.collateral_amount:
            raise ValueError("Not enough collateral to buy these options.")
        self.collateral_amount -= cost
        for _ in range(num_options):
            option = Option(
                strike_price, option_time_to_maturity, volatility, risk_free_rate
            )
            self.options.append(option)

    def calculate_portfolio(self, current_price):
        # Calculate the current value of the collateral
        collateral_value = self.collateral_amount * current_price

        # Calculate the current value of the options
        options_value = sum(
            black_scholes(
                current_price,
                option.strike_price,
                option.time_to_maturity,
                option.risk_free_rate,
                option.volatility,
                option_type="put",
            )
            for option in self.options
        )

        # Calculate the total value of the portfolio
        self.portfolio_value = collateral_value + options_value
        return self.portfolio_value

    def liquidation(self):
        # Calculate the liquidation value
        liquidation_value = self.loan_amount / self.liquidation_ratio

        # Check if the portfolio value is less than or equal to the liquidation value
        if self.portfolio_value <= liquidation_value:
            return True
        return False
