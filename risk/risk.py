from config.settings import CAPITAL, RISK_PER_TRADE


def get_quantity(price, stoploss):
    """
    Calculate position size based on risk parameters.
    
    Args:
        price: Current market price
        stoploss: Stoploss price
        
    Returns:
        int: Number of shares to trade
    """
    risk_amt = CAPITAL * RISK_PER_TRADE

    qty = risk_amt / abs(price - stoploss)

    return int(qty)
