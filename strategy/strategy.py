import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from typing import Optional


def generate_signal(data: list) -> str:
    """
    Generate trading signals based on technical indicators.
    
    Args:
        data: List of OHLC data dictionaries
        
    Returns:
        str: "BUY", "SELL", or "HOLD"
    """
    
    try:
        if not data or len(data) < 50:
            return "HOLD"
        
        df = pd.DataFrame(data)
        
        # Calculate technical indicators
        df["ema20"] = EMAIndicator(df['close'], 20).ema_indicator()
        df["ema50"] = EMAIndicator(df['close'], 50).ema_indicator()
        df["rsi"] = RSIIndicator(df['close']).rsi()
        
        df.dropna(inplace=True)
        
        if df.empty:
            return "HOLD"
        
        last = df.iloc[-1]
        
        # Buy Condition: More aggressive entry for more trades
        # EMA20 > EMA50 (uptrend), RSI below 75, price above EMA20
        # OR: Price above both EMAs with RSI < 75
        if (
            (last['ema20'] > last['ema50'] and last['rsi'] < 75) or
            (last['close'] > last['ema20'] and last['close'] > last['ema50'] and last['rsi'] < 75)
        ):
            return "BUY"
        
        # Sell Condition: More aggressive exits
        # EMA20 < EMA50 (downtrend) OR RSI > 75 (approaching overbought)
        if (
            (last['ema20'] < last['ema50']) or 
            (last['rsi'] > 75)
        ):
            return "SELL"
        
        return "HOLD"
        
    except Exception as e:
        print(f"Error generating signal: {e}")
        return "HOLD"


def validate_signal(signal: str, current_price: float, entry_price: Optional[float] = None) -> bool:
    """
    Validate trading signal with additional checks.
    
    Args:
        signal: Trading signal ("BUY", "SELL", "HOLD")
        current_price: Current market price
        entry_price: Entry price for existing position (optional)
        
    Returns:
        bool: Whether signal is valid to execute
    """
    
    if signal == "HOLD":
        return False
    
    if signal == "BUY" and current_price > 0:
        return True
    
    if signal == "SELL" and entry_price is not None and current_price != entry_price:
        return True
    
    return False