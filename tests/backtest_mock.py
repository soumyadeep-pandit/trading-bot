#!/usr/bin/env python3
"""
Mock Backtesting module - simulates trading with generated price data.
Demonstrates how to measure bot accuracy without real API credentials.
"""

import sys
import os
import pandas as pd
import numpy as np
from loguru import logger

# Add project root to path (go up one level from tests folder)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy.strategy import generate_signal
from config.settings import SYMBOL, CAPITAL, RISK_PER_TRADE

# Configure logger
logger.add("logs/backtest_mock.log", rotation="1 MB")


class MockBacktestEngine:
    """Mock backtest engine using simulated price data."""
    
    def __init__(self, symbol=SYMBOL, num_candles=200):
        self.symbol = symbol
        self.num_candles = num_candles
        self.trades = []
        self.signals = []
        self.data = None
        
    def generate_mock_data(self):
        """Generate realistic simulated OHLC data."""
        logger.info(f"Generating {self.num_candles} mock candles...")
        
        # Generate price data with realistic patterns
        np.random.seed(42)  # For reproducibility
        
        # Start price
        start_price = 2500  # Approximate RELIANCE price
        
        # Generate realistic price movements
        candles = []
        current_price = start_price
        
        for i in range(self.num_candles):
            # Random walk with trend
            change = np.random.normal(0, 15)  # Standard deviation
            open_price = current_price
            close_price = current_price + change
            high_price = max(open_price, close_price) + abs(np.random.normal(0, 5))
            low_price = min(open_price, close_price) - abs(np.random.normal(0, 5))
            volume = np.random.randint(100000, 1000000)
            
            candles.append({
                'date': i,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            })
            
            current_price = close_price
        
        self.data = candles
        logger.success(f"✓ Generated {len(self.data)} mock candles")
        logger.info(f"  Price range: ₹{min(c['low'] for c in candles):.2f} - ₹{max(c['high'] for c in candles):.2f}")
        
        return True
    
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
                    logger.info(f"📈 BUY signal at ₹{price:.2f}")
                
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
                    
                    logger.info(f"📉 SELL signal at ₹{exit_price:.2f} | PnL: ₹{pnl:.2f} ({pnl_pct:.2f}%)")
                    entry_price = None
                    entry_signal = None
            
            logger.success(f"✓ Simulated {len(self.trades)} complete trades")
            return True
        except Exception as e:
            logger.error(f"Failed to simulate trades: {e}", exc_info=True)
            return False
    
    def calculate_accuracy(self):
        """Calculate various accuracy metrics."""
        logger.info("\n" + "="*70)
        logger.info("ACCURACY METRICS")
        logger.info("="*70)
        
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
        
        # Breakeven trades
        breakeven_trades = [t for t in self.trades if t['pnl'] == 0]
        breakeven_count = len(breakeven_trades)
        if breakeven_count > 0:
            metrics['breakeven_trades'] = breakeven_count
            logger.info(f"Breakeven Trades: {breakeven_count}")
        
        # Win rate (accuracy)
        if total_trades > 0:
            win_rate = (win_count / total_trades) * 100
            metrics['win_rate'] = win_rate
            accuracy_emoji = "🟢" if win_rate > 50 else "🟡" if win_rate > 45 else "🔴"
            logger.info(f"Win Rate (Accuracy): {accuracy_emoji} {win_rate:.2f}%")
        
        # Average winning trade
        if winning_trades:
            avg_win = sum(t['pnl'] for t in winning_trades) / win_count
            max_win = max(t['pnl'] for t in winning_trades)
            metrics['avg_win'] = avg_win
            metrics['max_win'] = max_win
            logger.success(f"Average Win: ₹{avg_win:.2f} | Max Win: ₹{max_win:.2f}")
        
        # Average losing trade
        if losing_trades:
            avg_loss = sum(t['pnl'] for t in losing_trades) / loss_count
            max_loss = min(t['pnl'] for t in losing_trades)
            metrics['avg_loss'] = avg_loss
            metrics['max_loss'] = max_loss
            logger.error(f"Average Loss: ₹{avg_loss:.2f} | Max Loss: ₹{max_loss:.2f}")
        
        # Total PnL
        total_pnl = sum(t['pnl'] for t in self.trades)
        metrics['total_pnl'] = total_pnl
        pnl_emoji = "💰" if total_pnl > 0 else "📉"
        logger.info(f"\nTotal PnL: {pnl_emoji} ₹{total_pnl:.2f}")
        
        # Average PnL %
        if self.trades:
            avg_pnl_pct = sum(t['pnl_pct'] for t in self.trades) / len(self.trades)
            metrics['avg_pnl_pct'] = avg_pnl_pct
            logger.info(f"Average PnL %: {avg_pnl_pct:.2f}%")
        
        # Profit Factor
        if losing_trades and winning_trades:
            total_wins = sum(t['pnl'] for t in winning_trades)
            total_losses = abs(sum(t['pnl'] for t in losing_trades))
            profit_factor = total_wins / total_losses if total_losses > 0 else 0
            metrics['profit_factor'] = profit_factor
            logger.info(f"Profit Factor: {profit_factor:.2f}x")
        
        # Expected value per trade
        if total_trades > 0:
            expected_value = total_pnl / total_trades
            metrics['expected_value'] = expected_value
            logger.info(f"Expected Value per Trade: ₹{expected_value:.2f}")
        
        # Risk-Reward Ratio
        if winning_trades and losing_trades:
            avg_win = sum(t['pnl'] for t in winning_trades) / len(winning_trades)
            avg_loss = abs(sum(t['pnl'] for t in losing_trades) / len(losing_trades))
            reward_risk_ratio = avg_win / avg_loss if avg_loss > 0 else 0
            metrics['reward_risk_ratio'] = reward_risk_ratio
            logger.info(f"Risk-Reward Ratio: 1:{reward_risk_ratio:.2f}")
        
        logger.info("="*70 + "\n")
        
        return metrics
    
    def print_trade_summary(self):
        """Print summary of all trades."""
        logger.info("\n" + "="*70)
        logger.info("TRADE SUMMARY")
        logger.info("="*70)
        
        if not self.trades:
            logger.warning("No trades to display")
            return
        
        for i, trade in enumerate(self.trades, 1):
            status_emoji = "✅" if trade['pnl'] > 0 else "❌" if trade['pnl'] < 0 else "⚪"
            logger.info(f"{status_emoji} Trade #{i:2d} | Entry: ₹{trade['entry_price']:7.2f} | " +
                       f"Exit: ₹{trade['exit_price']:7.2f} | " +
                       f"PnL: ₹{trade['pnl']:7.2f} ({trade['pnl_pct']:6.2f}%)")
        
        logger.info("="*70 + "\n")
    
    def run_backtest(self):
        """Run complete backtest workflow."""
        logger.info("🤖 Starting Mock Backtest...")
        logger.info(f"📊 Symbol: {self.symbol}")
        
        if not self.generate_mock_data():
            return False
        
        if not self.generate_signals():
            return False
        
        if not self.simulate_trades():
            return False
        
        metrics = self.calculate_accuracy()
        self.print_trade_summary()
        
        logger.success("✅ Backtest completed successfully!")
        
        return metrics


def main():
    """Main entry point for mock backtesting."""
    try:
        # Create mock backtest engine
        logger.info("="*70)
        logger.info("MOCK BACKTEST - Trading Bot Accuracy Evaluation")
        logger.info("="*70 + "\n")
        
        engine = MockBacktestEngine(num_candles=200)
        
        # Run backtest
        metrics = engine.run_backtest()
        
        if metrics:
            logger.info("\n📊 FINAL SUMMARY:")
            logger.info(f"   ✓ Total Trades: {metrics.get('total_trades', 0)}")
            logger.info(f"   ✓ Win Rate: {metrics.get('win_rate', 0):.2f}%")
            logger.info(f"   ✓ Total PnL: ₹{metrics.get('total_pnl', 0):.2f}")
            logger.info(f"   ✓ Profit Factor: {metrics.get('profit_factor', 0):.2f}x")
            logger.info(f"   ✓ Expected Value/Trade: ₹{metrics.get('expected_value', 0):.2f}")
            logger.info("\n💡 Check logs/backtest_mock.log for detailed results\n")
        
    except Exception as e:
        logger.error(f"Backtest failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
