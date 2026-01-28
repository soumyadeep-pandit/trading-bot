# Trading Bot Accuracy Evaluation Guide

## Overview
This guide explains how to measure and evaluate the accuracy of your Trading AI Agent bot using the backtesting modules.

---

## Methods to Get Accuracy

### 1. **Mock Backtest (Recommended for Testing)**
Use simulated data to test the strategy without needing real API credentials.

```bash
python backtest_mock.py
```

**Pros:**
- Works without API credentials
- Fast execution
- Good for development and testing
- Reproducible results

**Output Metrics:**
- Win Rate (Accuracy %)
- Total Trades
- Winning/Losing Trades
- Profit & Loss
- Profit Factor
- Expected Value per Trade

---

### 2. **Real Backtest (Requires API Credentials)**
Uses actual historical market data from Zerodha API.

```bash
python backtest.py
```

**Requires:**
- Valid Zerodha API credentials in `config/settings.py`
- Valid access token for the day

---

## Key Accuracy Metrics Explained

### **Win Rate (Accuracy %)**
- **Definition:** Percentage of trades that made profit
- **Formula:** `(Winning Trades / Total Trades) × 100`
- **Good Range:** > 50%
- **Interpretation:** 60% win rate means 6 out of 10 trades were profitable

### **Total PnL (Profit & Loss)**
- **Definition:** Total profit or loss from all trades
- **Formula:** `Sum of all individual trade profits/losses`
- **Good:** Positive value
- **Interpretation:** Overall profitability of the strategy

### **Profit Factor**
- **Definition:** Ratio of total profits to total losses
- **Formula:** `Total Wins / Total Losses`
- **Good Range:** > 1.5
- **Interpretation:** 
  - `1.0` = Break-even
  - `1.5` = ₹1.50 profit for every ₹1 loss
  - `2.0` = ₹2.00 profit for every ₹1 loss

### **Expected Value per Trade**
- **Definition:** Average profit/loss per trade
- **Formula:** `Total PnL / Number of Trades`
- **Good:** Positive value
- **Interpretation:** On average, how much you make/lose per trade

### **Risk-Reward Ratio**
- **Definition:** Average win size vs average loss size
- **Formula:** `Average Win / Average Loss`
- **Good Range:** > 1.5
- **Interpretation:** 1:1.5 means average win is 1.5x the average loss

### **Max Win / Max Loss**
- **Definition:** Largest profitable and losing trade
- **Good:** High max win, low max loss
- **Interpretation:** Shows strategy's best and worst scenarios

---

## How to Interpret Results

### Excellent Performance 🟢
- Win Rate > 60%
- Profit Factor > 2.0
- Positive Total PnL
- Expected Value > 5 (per trade)

### Good Performance 🟡
- Win Rate > 50%
- Profit Factor > 1.5
- Positive Total PnL
- Expected Value > 0

### Poor Performance 🔴
- Win Rate < 50%
- Profit Factor < 1.0
- Negative Total PnL
- Expected Value < 0

---

## Example Backtest Output

```
ACCURACY METRICS
================================================================
Total Completed Trades: 15
Winning Trades: 9
Losing Trades: 6

Win Rate (Accuracy): 🟢 60.00%
Average Win: ₹250.50 | Max Win: ₹850.00
Average Loss: ₹-120.30 | Max Loss: ₹-350.00

Total PnL: 💰 ₹1845.00
Average PnL %: 1.23%

Profit Factor: 1.87x
Expected Value per Trade: ₹123.00
Risk-Reward Ratio: 1:2.08
================================================================
```

---

## Improving Bot Accuracy

### 1. **Optimize Parameters**
- Adjust EMA periods (20, 50)
- Tweak RSI thresholds (40-60)
- Change entry/exit conditions

### 2. **Add Filters**
- Volume confirmation
- Support/Resistance levels
- Time-based filters (trade only during certain hours)

### 3. **Risk Management**
- Implement proper stoploss
- Use position sizing
- Diversify trades

### 4. **Data Quality**
- Use more historical data
- Check for data gaps
- Ensure correct timeframe

---

## Backtesting Best Practices

✅ **DO:**
- Test on at least 2-3 months of data
- Include different market conditions (trending, ranging)
- Track all metrics consistently
- Keep detailed logs
- Test multiple symbols

❌ **DON'T:**
- Overfit to past data
- Use too short time periods
- Ignore transaction costs
- Trust 100% accuracy predictions
- Use unrealistic parameters

---

## Running Different Scenarios

### Test on More Data
```python
engine = MockBacktestEngine(num_candles=500)  # Increase from 200
```

### Test Different Time Periods
```python
engine = BacktestEngine(days=60)  # Test 60 days instead of 30
```

### Test Multiple Symbols
```python
from config.settings import SYMBOL
engine = BacktestEngine(symbol="TCS")  # Different stock
```

---

## Files for Accuracy Testing

| File | Purpose | Credentials Required |
|------|---------|----------------------|
| `backtest_mock.py` | Mock backtest with simulated data | No |
| `backtest.py` | Real backtest with API data | Yes |
| `test_bot.py` | Integration test | No |

---

## How to Use Results

1. **Initial Assessment:** Run mock backtest first
2. **Validate with Real Data:** Run real backtest with credentials
3. **Identify Issues:** Check accuracy metrics
4. **Optimize Strategy:** Adjust parameters based on results
5. **Monitor Live:** Track performance while trading

---

## Troubleshooting

**Q: Why is win rate 0%?**
- Strategy needs more data points
- RSI/EMA parameters may be too restrictive
- Try adjusting thresholds in [strategy.py](strategy.py)

**Q: Why is profit factor showing 0?**
- No winning trades generated
- Entry/exit signals need adjustment
- Test with different data periods

**Q: How do I improve accuracy?**
- Add more technical indicators
- Implement better entry/exit rules
- Test different timeframes
- Use proper risk management

---

## Quick Start

### Run Mock Backtest (Fastest)
```bash
python backtest_mock.py
```

### Run Real Backtest (If credentials available)
```bash
python backtest.py
```

### Monitor the Live Bot
```bash
python main.py
```

---

## Next Steps

1. ✅ Run mock backtest to understand metrics
2. ✅ Review accuracy metrics output
3. ✅ Identify improvement areas
4. ✅ Update strategy parameters
5. ✅ Re-test with improved parameters
6. ✅ Deploy to live trading (PAPER mode first)

---

**Remember:** Past performance is not a guarantee of future results. Always test thoroughly before live trading.
