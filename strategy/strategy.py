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
        
        # Buy Condition: EMA20 above EMA50, RSI in neutral zone, price above EMA20
        if (
            last['ema20'] > last['ema50'] and
            40 < last['rsi'] < 60 and
            last['close'] > last['ema20']
        ):
            return "BUY"
        
        # Sell Condition: EMA20 below EMA50, RSI overbought
        if (
            last['ema20'] < last['ema50'] and 
            last['rsi'] > 60
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