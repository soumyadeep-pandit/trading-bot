from kiteconnect import KiteConnect
from config.settings import API_KEY, ACCESS_TOKEN, TOKEN
from datetime import datetime, timedelta


kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)


def get_historical(days=30):

    to_dt = datetime.now()
    from_dt = to_dt - timedelta(days=days)

    data = kite.historical_data(
        TOKEN,
        from_dt,
        to_dt,
        "5minute"
    )

    return data


def get_ltp(symbol):

    data = kite.ltp(f"NSE:{symbol}")

    if isinstance(data, dict) and f"NSE:{symbol}" in data:
        return data[f"NSE:{symbol}"].get("last_price")
    return None
