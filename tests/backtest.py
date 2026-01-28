#!/usr/bin/env python3
"""
Backtesting module to evaluate bot accuracy on historical data.
Measures signal accuracy, win rate, and profitability metrics.
"""

import sys
import os
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

# Add project root to path (go up one level from tests folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.market_data import get_historical, kite
from strategy.strategy import generate_signal
from risk.risk import get_quantity
from config.settings import SYMBOL, TOKEN, API_KEY, ACCESS_TOKEN

# Configure logger
logger.add("logs/backtest.log", rotation="1 MB")


class BacktestEngine:
    """Engine to backtest trading strategy and calculate accuracy metrics."""
    
    def __init__(self, symbol=SYMBOL, days=30):
        self.symbol = symbol
        self.days = days
        self.trades = []
        self.signals = []
        self.data = None
        
    def fetch_data(self):
        """Fetch historical data for backtesting."""
        logger.info(f"Fetching {self.days} days of historical data for {self.symbol}...")
        try:
            self.data = get_historical(self.days)
            if self.data:
                logger.success(f"✓ Fetched {len(self.data)} candles")
                return True
            else:
                logger.error("No data received")
                return False
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
            return False
    
    def generate_signals(self):
        """Generate trading signals for all historical data."""
        logger.info("Generating trading signals...")
        
        if not self.data:
            logger.error("No data available")
            return False
        
        try:
            for i in range(50, len(self.data)):
                # Use previous candles to generate signal
                lookback_data = self.data[max(0, i-50):i]
                signal = generate_signal(lookback_data)
                
                candle = self.data[i]
                self.signals.append({
                    'timestamp': candle.get('date', i),
                    'close': candle['close'],
                    'signal': signal,
                    'index': i
                })
            
            logger.success(f"✓ Generated {len(self.signals)} signals")
            return True
        except Exception as e:
            logger.error(f"Failed to generate signals: {e}")
            return False
    
    def simulate_trades(self):
        """Simulate trades based on signals and calculate P&L."""
        logger.info("Simulating trades...")
        
        if not self.signals or not self.data:
            logger.error("No signals available")
            return False
        
        try:
            entry_price = None
            entry_signal = None
            entry_index = None
            
            for sig_data in self.signals:
                signal = sig_data['signal']
                price = sig_data['close']
                
                if signal == "BUY" and entry_price is None:
                    # Enter long position
                    entry_price = price
                    entry_signal = "BUY"
                    entry_index = sig_data['index']
                    logger.info(f"📈 BUY signal at ₹{price}")
                
                elif signal == "SELL" and entry_price is not None and entry_signal == "BUY":
                    # Exit long position
                    exit_price = price
                    pnl = exit_price - entry_price
                    pnl_pct = (pnl / entry_price) * 100
                    
                    self.trades.append({
                        'entry_price': entry_price,
                        'exit_price': exit_price,
                        'entry_index': entry_index,
                        'exit_index': sig_data['index'],
                        'pnl': pnl,
                        'pnl_pct': pnl_pct,
                        'type': 'LONG',
                        'status': 'CLOSED'
                    })
                    
                    logger.info(f"📉 SELL signal at ₹{exit_price} | PnL: ₹{pnl:.2f} ({pnl_pct:.2f}%)")
                    entry_price = None
                    entry_signal = None
            
            logger.success(f"✓ Simulated {len(self.trades)} complete trades")
            return True
        except Exception as e:
            logger.error(f"Failed to simulate trades: {e}", exc_info=True)
            return False
    
    def calculate_accuracy(self):
        """Calculate various accuracy metrics."""
        logger.info("\n" + "="*60)
        logger.info("ACCURACY METRICS")
        logger.info("="*60)
        
        if not self.trades:
            logger.warning("No completed trades to analyze")
            return {}
        
        metrics = {}
        
        # Total trades
        total_trades = len(self.trades)
        metrics['total_trades'] = total_trades
        logger.info(f"Total Completed Trades: {total_trades}")
        
        # Winning trades
        winning_trades = [t for t in self.trades if t['pnl'] > 0]
        win_count = len(winning_trades)
        metrics['winning_trades'] = win_count
        logger.info(f"Winning Trades: {win_count}")
        
        # Losing trades
        losing_trades = [t for t in self.trades if t['pnl'] < 0]
        loss_count = len(losing_trades)
        metrics['losing_trades'] = loss_count
        logger.info(f"Losing Trades: {loss_count}")
        
        # Win rate
        if total_trades > 0:
            win_rate = (win_count / total_trades) * 100
            metrics['win_rate'] = win_rate
            logger.success(f"Win Rate: {win_rate:.2f}%")
        
        # Average winning trade
        if winning_trades:
            avg_win = sum(t['pnl'] for t in winning_trades) / win_count
            metrics['avg_win'] = avg_win
            logger.success(f"Average Win: ₹{avg_win:.2f}")
        
        # Average losing trade
        if losing_trades:
            avg_loss = sum(t['pnl'] for t in losing_trades) / loss_count
            metrics['avg_loss'] = avg_loss
            logger.error(f"Average Loss: ₹{avg_loss:.2f}")
        
        # Total PnL
        total_pnl = sum(t['pnl'] for t in self.trades)
        metrics['total_pnl'] = total_pnl
        logger.info(f"\nTotal PnL: ₹{total_pnl:.2f}")
        
        # Total PnL %
        if self.trades:
            total_pnl_pct = sum(t['pnl_pct'] for t in self.trades) / len(self.trades)
            metrics['avg_pnl_pct'] = total_pnl_pct
            logger.info(f"Average PnL %: {total_pnl_pct:.2f}%")
        
        # Profit Factor
        if losing_trades:
            total_wins = sum(t['pnl'] for t in winning_trades) if winning_trades else 0
            total_losses = abs(sum(t['pnl'] for t in losing_trades))
            profit_factor = total_wins / total_losses if total_losses > 0 else 0
            metrics['profit_factor'] = profit_factor
            logger.info(f"Profit Factor: {profit_factor:.2f}")
        
        # Expected value
        if total_trades > 0:
            expected_value = total_pnl / total_trades
            metrics['expected_value'] = expected_value
            logger.info(f"Expected Value per Trade: ₹{expected_value:.2f}")
        
        logger.info("="*60 + "\n")
        
        return metrics
    
    def print_trade_details(self):
        """Print detailed breakdown of each trade."""
        logger.info("\n" + "="*60)
        logger.info("TRADE DETAILS")
        logger.info("="*60)
        
        for i, trade in enumerate(self.trades, 1):
            logger.info(f"\nTrade #{i}")
            logger.info(f"  Entry: ₹{trade['entry_price']:.2f}")
            logger.info(f"  Exit:  ₹{trade['exit_price']:.2f}")
            logger.info(f"  PnL:   ₹{trade['pnl']:.2f} ({trade['pnl_pct']:.2f}%)")
        
        logger.info("="*60 + "\n")
    
    def run_backtest(self):
        """Run complete backtest workflow."""
        logger.info("🤖 Starting Backtest...")
        
        if not self.fetch_data():
            return False
        
        if not self.generate_signals():
            return False
        
        if not self.simulate_trades():
            return False
        
        metrics = self.calculate_accuracy()
        self.print_trade_details()
        
        logger.success("✓ Backtest completed successfully!")
        
        return metrics


def main():
    """Main entry point for backtesting."""
    try:
        # Create backtest engine
        engine = BacktestEngine(days=30)
        
        # Run backtest
        metrics = engine.run_backtest()
        
        if metrics:
            logger.info("📊 Summary:")
            logger.info(f"   • Total Trades: {metrics.get('total_trades', 0)}")
            logger.info(f"   • Win Rate: {metrics.get('win_rate', 0):.2f}%")
            logger.info(f"   • Total PnL: ₹{metrics.get('total_pnl', 0):.2f}")
            logger.info(f"   • Profit Factor: {metrics.get('profit_factor', 0):.2f}")
        
    except Exception as e:
        logger.error(f"Backtest failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
