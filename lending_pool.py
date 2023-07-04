from loan import Loan
from pool_interest_rate import (
    calculate_variable_interest_rate,
    calculate_stable_borrow_rate,
)


class LendingPool:
    def __init__(self, asset):
        self.deposits = 0
        self.lenders = {}
        self.token_supply = 0
        self.loans = []
        self.utilization = 0
        self.variable_interest_rate = calculate_variable_interest_rate(
            asset, self.utilization
        )
        self.stable_interest_rate = calculate_stable_borrow_rate(
            asset, self.utilization
        )

    def deposit(self, lender, amount):
        self.deposits += amount
        if lender in self.lenders:
            self.lenders[lender]["amount"] += amount
        else:
            self.lenders[lender] = {"amount": amount, "tokens": 0}

    def issue_loan(
        self,
        loan_amount,
        collateral_amount,
        collateral_asset,
        loan_time_to_maturity,
        loan_to_value=0.75,
        liquidation_ratio=0.8,
        safety_margin=0.05,
        is_fixed_rate=True,
    ):
        loan_amount = collateral_amount * loan_to_value
        if self.deposits < loan_amount:
            raise ValueError("Not enough funds in the pool to issue this loan.")
        self.deposits -= loan_amount

        loan = Loan(
            loan_amount,
            collateral_asset,
            collateral_amount,
            loan_time_to_maturity,
            loan_to_value,
            liquidation_ratio,
            safety_margin,
            self,
            is_fixed_rate,
        )

        self.loans.append(loan)
        return loan

    def issue_tokens(self, lender, deposit_amount):
        self.token_supply += deposit_amount
        if lender in self.lenders:
            self.lenders[lender]["tokens"] += deposit_amount
        else:
            raise ValueError("Cant issue tokens to inexistent lender.")
