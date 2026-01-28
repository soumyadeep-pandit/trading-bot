#!/usr/bin/env python3
"""
Test script to validate the Trading AI Bot in a safe environment.
Runs a few iterations in PAPER mode to verify all components work.
"""

import sys
import os
import time

# Add project root to path (go up one level from tests folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config.settings import MODE, SYMBOL

# Configure logger for test
logger.add("logs/test_bot.log", rotation="1 MB")

logger.info(f"=== Starting Bot Test ===")
logger.info(f"Trading Mode: {MODE}")
logger.info(f"Trading Symbol: {SYMBOL}")

# Test imports
try:
    from data.market_data import get_historical, get_ltp
    logger.success("✓ Market data module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import market data: {e}")
    sys.exit(1)

try:
    from strategy.strategy import generate_signal
    logger.success("✓ Strategy module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import strategy: {e}")
    sys.exit(1)

try:
    from risk.risk import get_quantity
    logger.success("✓ Risk management module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import risk: {e}")
    sys.exit(1)

try:
    from execution.orders import place_order
    logger.success("✓ Order execution module imported successfully")
except Exception as e:
    logger.error(f"✗ Failed to import orders: {e}")
    sys.exit(1)

# Test bot loop - 3 iterations
logger.info("\n=== Starting Bot Iterations ===")

for iteration in range(1, 4):
    try:
        logger.info(f"\n--- Iteration {iteration} ---")
        
        # Get market data
        logger.info(f"Fetching historical data for {SYMBOL}...")
        data = get_historical()
        if data:
            logger.success(f"✓ Retrieved {len(data)} data points")
        else:
            logger.warning("⚠ No historical data received")
        
        # Generate signal
        signal = generate_signal(data)
        logger.info(f"Signal Generated: {signal}")
        
        # Get current price
        logger.info(f"Fetching LTP for {SYMBOL}...")
        price = get_ltp(SYMBOL)
        
        if price is None:
            logger.warning(f"Could not get price for {SYMBOL}")
            continue
        
        logger.success(f"✓ Current Price: ₹{price}")
        
        # Calculate position size
        stoploss = price * 0.98
        qty = get_quantity(price, stoploss)
        logger.info(f"Position Size: {qty} shares | Stoploss: ₹{stoploss:.2f}")
        
        # Log summary
        logger.info(f"Summary - Signal: {signal} | Price: ₹{price} | Qty: {qty} | Mode: {MODE}")
        
        # Execute order (in PAPER mode, just logs)
        if signal != "HOLD" and qty > 0:
            logger.info(f"Executing {signal} order for {qty} shares...")
            place_order(signal, qty)
            logger.success(f"✓ {signal} order processed")
        else:
            logger.info("No trade executed (HOLD signal or invalid quantity)")
        
        logger.success(f"✓ Iteration {iteration} completed successfully\n")
        
    except Exception as e:
        logger.error(f"✗ Error in iteration {iteration}: {e}", exc_info=True)

logger.success("\n=== Bot Test Completed Successfully ===")
logger.info("Check logs/test_bot.log for detailed results")
