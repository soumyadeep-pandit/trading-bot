from config.settings import MODE, SYMBOL
from data.market_data import kite
from loguru import logger


def place_order(signal, qty):

    if MODE == "PAPER":

        logger.info(f"PAPER TRADE: {signal} {qty}")
        return

    try:

        if signal == "BUY":

            kite.place_order(
                variety="regular",
                exchange="NSE",
                tradingsymbol=SYMBOL,
                transaction_type="BUY",
                quantity=qty,
                order_type="MARKET",
                product="MIS"
            )

        elif signal == "SELL":

            kite.place_order(
                variety="regular",
                exchange="NSE",
                tradingsymbol=SYMBOL,
                transaction_type="SELL",
                quantity=qty,
                order_type="MARKET",
                product="MIS"
            )

        logger.success("Order Placed")

    except Exception as e:

        logger.error(e)