class Loan:
    def __init__(
        self,
        loan_amount,
        collateral_asset,
        collateral_amount,
        maturity,
        loan_to_value,
        liquidation_ratio,
        safety_margin,
        interest_rate,
    ):
        self.loan_amount = loan_amount
        self.collateral_asset = collateral_asset
        self.collateral_amount = collateral_amount
        self.maturity = maturity
        self.loan_to_value = loan_to_value
        self.liquidation_ratio = liquidation_ratio
        self.safety_margin = safety_margin
        self.interest_rate = interest_rate
        # self.portfolio = [self.collateral_amount] => This needs to be price * quantity
