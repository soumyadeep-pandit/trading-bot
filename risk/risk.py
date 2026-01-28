from config.settings import CAPITAL, RISK_PER_TRADE


def get_quantity(price, stoploss):

    risk_amt = CAPITAL * RISK_PER_TRADE

    qty = risk_amt / abs(price - stoploss)

    return int(qty)