# 🤖 Trading AI Agent

**Automated Trading Bot with EMA, RSI, and Risk Management**

> An intelligent Python-based trading bot that automatically generates trading signals using technical indicators, manages risk, and executes trades on Zerodha platform.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)](https://github.com/soumyadeep-pandit/trading-bot)

---

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Backtesting](#backtesting)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Disclaimer](#disclaimer)

---

## ✨ Features

### Core Trading Features
- ✅ **Automated Signal Generation** - EMA20, EMA50, and RSI indicators
- ✅ **Risk Management** - Position sizing based on risk parameters
- ✅ **Order Execution** - Automatic BUY/SELL order placement
- ✅ **PAPER Trading Mode** - Test without real money
- ✅ **LIVE Trading Mode** - Real money trading (use with caution)

### Technical Indicators
- 📊 **EMA (Exponential Moving Average)** - Trend identification
- 📊 **RSI (Relative Strength Index)** - Overbought/Oversold detection
- 📊 **Support & Resistance** - Price level analysis

### Additional Features
- 🧪 **Mock Backtesting** - Test strategy on simulated data
- 📈 **Accuracy Metrics** - Win rate, profit factor, expected value
- 📝 **Comprehensive Logging** - Track all bot activities
- 🔄 **24/7 Deployment** - Run on cloud servers (Render, AWS, etc.)
- ⚙️ **Configurable Parameters** - Customize strategy settings

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Zerodha Kite API account
- Git

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/soumyadeep-pandit/trading-bot.git
cd trading-bot
\`\`\`

### 2. Create Virtual Environment
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configure Settings
Edit \`config/settings.py\` with your Zerodha credentials:
\`\`\`python
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
MODE = "PAPER"  # Start with PAPER mode
\`\`\`

### 5. Test Locally
\`\`\`bash
python main.py
\`\`\`

### 6. Run Backtest
\`\`\`bash
python backtest_mock.py
\`\`\`

---

## 📥 Installation

### Step 1: Clone Repository
\`\`\`bash
git clone https://github.com/soumyadeep-pandit/trading-bot.git
cd trading-bot
\`\`\`

### Step 2: Setup Python Environment
\`\`\`bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
\`\`\`

### Step 3: Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Verify Installation
\`\`\`bash
python -c "import kiteconnect; print('✅ All dependencies installed')"
\`\`\`

---

## ⚙️ Configuration

### Get Zerodha API Credentials

#### 1. Get API Key and Secret
1. Go to https://kite.trade
2. Settings → API Permissions
3. Create new app
4. Copy API_KEY and API_SECRET

#### 2. Get Access Token (Daily Requirement)
\`\`\`bash
python auth/login.py
# Follow the browser login, copy request token from redirect URL
# Paste when prompted
# ⚠️ NOTE: Access Token expires daily and must be regenerated
\`\`\`

#### 3. Update config/settings.py
\`\`\`python
# Zerodha Credentials
API_KEY = "your_actual_api_key"
API_SECRET = "your_actual_api_secret"
ACCESS_TOKEN = "your_generated_token"

# Trading Settings
SYMBOL = "RELIANCE"           # Stock symbol
TOKEN = 738561                # Zerodha token
CAPITAL = 50000               # Capital (rupees)
RISK_PER_TRADE = 0.01        # 1% risk per trade

# Mode
MODE = "PAPER"                # Use PAPER first, then LIVE
\`\`\`

---

## 🎮 Usage

### Run Bot Locally
\`\`\`bash
python main.py
\`\`\`

**Output:**
\`\`\`
2026-01-28 10:30:45 | INFO | Bot Started
2026-01-28 10:30:50 | INFO | Signal: BUY | Price: ₹2550
2026-01-28 10:30:51 | INFO | Order Placed
\`\`\`

### Test with Mock Backtest
\`\`\`bash
python backtest_mock.py
\`\`\`

### Real Backtest
\`\`\`bash
python backtest.py
\`\`\`

---

## 📊 Backtesting

### Understanding Accuracy Metrics

| Metric | Meaning | Good Value |
|--------|---------|-----------|
| **Win Rate** | % of profitable trades | > 50% |
| **Profit Factor** | Total wins / Total losses | > 1.5 |
| **Total PnL** | Total profit/loss | > 0 |
| **Expected Value** | Avg profit per trade | > ₹0 |

---

## 🌐 Deployment

### Deploy to Render (Free)

1. Push code to GitHub
2. Create account at https://render.com
3. Click "New +" → "Web Service"
4. Connect your trading-bot repository
5. Configure build and start commands
6. Add environment variables
7. Deploy!

For detailed steps, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)

---

## 🔧 Troubleshooting

### Bot not starting?
- Check API credentials are correct
- Verify internet connection
- Check logs in logs/ folder

### No trades executing?
- Verify MODE = "PAPER" or "LIVE"
- Check strategy signals
- Run backtest first

### Token expired?
- Run: \`python auth/login.py\`
- Update ACCESS_TOKEN in config
- Daily renewal needed for production

---

## ⚠️ Disclaimer

**For educational purposes only.** Trading involves risk. Always test in PAPER mode first.

- Past performance ≠ Future results
- Never risk more than you can afford to lose
- Monitor bot regularly
- Use proper stop-loss strategy

---

## 📚 Documentation

- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Deployment guide
- [ACCURACY_GUIDE.md](ACCURACY_GUIDE.md) - Accuracy evaluation
- [config/settings.py](config/settings.py) - Configuration

---

## 🎯 Next Steps

1. Clone repo
2. Setup environment
3. Add credentials
4. Test with backtest
5. Deploy to Render
6. Monitor performance

---

**Happy Trading! 🚀**
