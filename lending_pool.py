from loan import Loan
from pool_interest_rate import (
    calculate_variable_interest_rate,
    calculate_stable_borrow_rate,
)


class LendingPool:
    def __init__(self, asset):
        self.deposits = {}
        self.loans = []
        self.utilization = 0
        self.variable_interest_rate = calculate_variable_interest_rate(
            asset, self.utilization
        )
        self.stable_interest_rate = calculate_stable_borrow_rate(
            asset, self.utilization
        )

    def deposit(self, lender, amount):
        self.deposits[lender] = amount

    def issue_loan(
        self,
        loan_amount,
        collateral,
        maturity,
        loan_to_value=0.75,
        liquidation_ratio=0.8,
        safety_margin=0.05,
    ):
        loan_amount = collateral * loan_to_value
        if self.deposits < loan_amount:
            raise ValueError("Not enough funds in the pool to issue this loan.")
        self.deposits -= loan_amount

        loan = Loan(
            loan_amount,
            collateral,
            maturity,
            loan_to_value,
            liquidation_ratio,
            safety_margin,
            self.variable_interest_rate,
        )
        self.loans.append(loan)
        return loan
