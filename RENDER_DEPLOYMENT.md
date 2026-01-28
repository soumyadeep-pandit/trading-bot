# Render Deployment Guide for Trading Bot

## Step-by-Step Deployment to Render

### ✅ Prerequisites:
- GitHub account (free)
- Render account (free)
- Your code pushed to GitHub
- Zerodha API credentials ready

---

## **STEP 1: Prepare Your Code**

### 1.1 Initialize Git Repository
```bash
cd "/Users/soumyadeeppandit/Project/Trading AI Agent"
git init
```

### 1.2 Create .gitignore
```bash
cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
logs/*.log
*.db
.DS_Store
EOF
```

### 1.3 Add All Files
```bash
git add .
git commit -m "Initial trading bot commit"
```

---

## **STEP 2: Push to GitHub**

### 2.1 Create New Repository
- Go to https://github.com/new
- Repository name: `trading-bot` (or any name)
- Description: "Automated Trading Bot with EMA and RSI"
- Choose: **Public** (for free tier)
- Click "Create repository"

### 2.2 Push Your Code
```bash
git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
git branch -M main
git push -u origin main
```

### 2.3 Verify on GitHub
- Go to https://github.com/YOUR_USERNAME/trading-bot
- You should see all your files

---

## **STEP 3: Create Render Account**

### 3.1 Sign Up
- Go to https://render.com
- Click "Get Started Free"
- Sign up with GitHub (easiest)
- Authorize Render to access GitHub

### 3.2 Verify Email
- Check your email for verification link
- Click to verify

---

## **STEP 4: Create New Service on Render**

### 4.1 Go to Dashboard
- After sign-up, you'll be on: https://dashboard.render.com
- Click **"New +"** button (top right)
- Select **"Web Service"**

### 4.2 Connect GitHub Repository
- Click "Connect a repository"
- Find your repository: `trading-bot`
- Click "Connect"

### 4.3 Configure Service
Fill in these fields:

| Field | Value |
|-------|-------|
| Name | `trading-bot` |
| Environment | `Python 3` |
| Region | `Frankfurt` (or nearest to you) |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python main.py` |
| Instance Type | **Free** |
| Auto-deploy | **Yes** |

### 4.4 Click "Create Web Service"
- Wait for deployment (takes 2-3 minutes)

---

## **STEP 5: Add Environment Variables**

### 5.1 Go to Service Settings
- On Render dashboard, click on your service
- Go to "Environment" tab

### 5.2 Add Variables
Click "Add Environment Variable" and add:

```
API_KEY              → your_actual_api_key
API_SECRET           → your_actual_api_secret
ACCESS_TOKEN         → your_actual_access_token
MODE                 → PAPER
SYMBOL               → RELIANCE
CAPITAL              → 50000
RISK_PER_TRADE       → 0.01
```

### 5.3 Save
- Click "Save" after each variable

---

## **STEP 6: Verify Deployment**

### 6.1 Check Logs
- Click on "Logs" tab
- Should see: `Bot Started`

### 6.2 Check Status
- If green dot next to service name = Running ✅
- If error, check logs for issues

### 6.3 Monitor Bot
```
Expected log output:
2026-01-28 10:30:45 | INFO | Bot Started
2026-01-28 10:30:50 | INFO | Fetching historical data
2026-01-28 10:30:55 | INFO | Signal: BUY
2026-01-28 10:30:56 | INFO | Order Placed
```

---

## **STEP 7: Daily Token Refresh** ⚠️

### Problem:
Access token expires daily at market close

### Solution:
You need to manually update token each day:

1. **Run login locally:**
   ```bash
   python auth/login.py
   ```

2. **Get new token and update Render:**
   - Copy new access token
   - Go to Render dashboard
   - Environment tab
   - Update `ACCESS_TOKEN` value
   - Changes apply automatically

### Alternative: Auto-Refresh (Advanced)
You can implement auto-refresh in code, but requires more setup.

---

## **STEP 8: Monitor & Troubleshoot**

### 8.1 View Live Logs
- Dashboard → Your service → Logs tab
- Logs update in real-time

### 8.2 Common Issues

**Issue: "ModuleNotFoundError"**
```
Solution: Check requirements.txt has all packages
```

**Issue: "Authentication failed"**
```
Solution: Check API_KEY and ACCESS_TOKEN are correct
```

**Issue: "Service crashed"**
```
Solution: Check logs, usually API credentials issue
```

### 8.3 Restart Service
- Click "Manual Deploy" button
- Service restarts

---

## **STEP 9: Stop/Delete Service**

### 9.1 Pause Service
- Go to Settings tab
- Click "Suspend" (bot stops, can resume later)

### 9.2 Delete Service
- Go to Settings tab
- Scroll down to "Danger Zone"
- Click "Delete Service"

---

## **STEP 10: Update Code**

### 10.1 Make Local Changes
```bash
# Edit strategy.py or any file
# Test locally first
python main.py  # Test
```

### 10.2 Push to GitHub
```bash
git add .
git commit -m "Update strategy parameters"
git push
```

### 10.3 Render Auto-Updates
- Render detects GitHub push
- Automatically redeploys (takes 2-3 min)
- No manual action needed

---

## **CHECKLIST**

Before deploying, ensure:

- ✅ Code tested locally (`python main.py` works)
- ✅ `requirements.txt` has all packages
- ✅ `.gitignore` created
- ✅ Code pushed to GitHub
- ✅ Render account created
- ✅ GitHub connected to Render
- ✅ Environment variables set (API_KEY, API_SECRET, ACCESS_TOKEN)
- ✅ Procfile present
- ✅ render.yaml present
- ✅ Service shows "Running" status

---

## **QUICK COMMANDS**

### Test Locally
```bash
cd "/Users/soumyadeeppandit/Project/Trading AI Agent"
python main.py
```

### Push Updates
```bash
git add .
git commit -m "Your message"
git push
```

### View Logs
- Render dashboard → Your service → Logs

### Get New Token
```bash
python auth/login.py
# Update ACCESS_TOKEN in Render environment
```

---

## **AFTER DEPLOYMENT**

### Daily Routine:
1. ✅ Monitor bot logs (5 min check)
2. ✅ Update access token if expired
3. ✅ Check for errors in logs
4. ✅ Verify trades executing

### Weekly:
1. ✅ Review backtest results
2. ✅ Check profitability
3. ✅ Monitor strategy performance

### Monthly:
1. ✅ Optimize strategy if needed
2. ✅ Update parameters
3. ✅ Re-test changes

---

## **COSTS**

- **Render Free Tier**: $0/month
- **Zerodha API**: Free
- **GitHub**: Free
- **Total Monthly Cost**: $0 🎉

---

## **SUPPORT**

If you get stuck:
1. Check Render logs for error messages
2. Verify all environment variables are set
3. Ensure GitHub repo has all files
4. Test locally before pushing to GitHub

---

## **NEXT STEPS**

1. Follow steps 1-7 above
2. Verify bot is running with logs
3. Monitor for 24 hours
4. Check trades in Zerodha dashboard
5. Update strategy if needed

**Your bot will then run 24/7 automatically on Render!** 🚀

---

**Questions?** Check specific steps above or verify your configuration.
