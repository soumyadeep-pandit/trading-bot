import time
from loguru import logger

from data.market_data import get_historical, get_ltp
from strategy.strategy import generate_signal
from risk.risk import get_quantity
from execution.orders import place_order
from config.settings import SYMBOL


logger.add("logs/bot.log", rotation="1 MB")


def run():

    logger.info("Bot Started")

    while True:

        try:

            data = get_historical()

            signal = generate_signal(data)

            price = get_ltp(SYMBOL)
            
            if price is None:
                logger.warning(f"Could not get price for {SYMBOL}")
                continue

            stoploss = price * 0.98

            qty = get_quantity(price, stoploss)

            logger.info(f"Signal: {signal} | Price: {price} | Qty: {qty}")

            if signal != "HOLD" and qty > 0:

                place_order(signal, qty)

            time.sleep(300)   # 5 min

        except Exception as e:

            logger.error(e)

            time.sleep(60)


if __name__ == "__main__":
    run()
