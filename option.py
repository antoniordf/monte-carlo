class Option:
    def __init__(self, strike_price, time_to_maturity, volatility, risk_free_rate):
        self.strike_price = strike_price
        self.time_to_maturity = time_to_maturity
        self.volatility = volatility
        self.risk_free_rate = risk_free_rate
