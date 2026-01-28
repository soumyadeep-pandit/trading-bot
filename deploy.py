#!/usr/bin/env python3
"""
Quick deployment script to help with Render setup
Run this to prepare your bot for deployment
"""

import os
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_step(num, text):
    print(f"\n📍 STEP {num}: {text}")
    print("-" * 70)

def run_command(cmd, description=""):
    """Run a shell command"""
    if description:
        print(f"  Running: {description}")
    print(f"  $ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Success")
            return True
        else:
            print(f"  ❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print_header("🚀 RENDER DEPLOYMENT HELPER")
    
    # Step 1: Check prerequisites
    print_step(1, "Verify Prerequisites")
    
    checks = {
        "Python": "python --version",
        "Git": "git --version",
        "requirements.txt": "test -f requirements.txt && echo 'Found'",
    }
    
    all_good = True
    for name, cmd in checks.items():
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ {name}: OK")
        else:
            print(f"  ❌ {name}: Missing")
            all_good = False
    
    if not all_good:
        print("\n  ⚠️  Please install missing prerequisites")
        return
    
    # Step 2: Initialize Git
    print_step(2, "Initialize Git Repository")
    
    if os.path.exists(".git"):
        print("  ℹ️  Git already initialized")
    else:
        print("  Initializing Git repository...")
        run_command("git init", "Initialize Git")
    
    # Step 3: Configure Git
    print_step(3, "Configure Git")
    
    print("  Enter your GitHub username: ", end="")
    username = input().strip()
    
    if username:
        print(f"  Your repo URL will be: https://github.com/{username}/trading-bot")
        print("  ✅ Ready for GitHub")
    
    # Step 4: Show deployment files
    print_step(4, "Deployment Files Created")
    
    files = ["Procfile", "render.yaml", ".gitignore", "RENDER_DEPLOYMENT.md"]
    for f in files:
        if os.path.exists(f):
            print(f"  ✅ {f}")
        else:
            print(f"  ❌ {f} - Missing!")
    
    # Step 5: Show next steps
    print_step(5, "Next Steps")
    
    print("""
  1️⃣  Push code to GitHub:
      $ git add .
      $ git commit -m "Initial trading bot commit"
      $ git remote add origin https://github.com/YOUR_USERNAME/trading-bot.git
      $ git push -u origin main
  
  2️⃣  Go to Render Dashboard:
      https://render.com/dashboard
  
  3️⃣  Click "New +" → "Web Service"
  
  4️⃣  Connect your GitHub repository
  
  5️⃣  Fill in:
      • Name: trading-bot
      • Build Command: pip install -r requirements.txt
      • Start Command: python main.py
      • Instance Type: Free
  
  6️⃣  Click "Create Web Service"
  
  7️⃣  Add Environment Variables:
      • API_KEY
      • API_SECRET
      • ACCESS_TOKEN
      • MODE (PAPER)
  
  8️⃣  Wait for deployment to complete
  
  9️⃣  Check logs to verify bot is running
  
  🔟 Monitor bot performance
    """)
    
    # Step 6: Useful commands
    print_step(6, "Useful Commands")
    
    print("""
  Test locally:
      $ python main.py
  
  Test backtest:
      $ python backtest_mock.py
  
  Update code and redeploy:
      $ git add .
      $ git commit -m "Update message"
      $ git push
  
  View Render logs:
      Go to: https://dashboard.render.com
      Click your service → Logs tab
    """)
    
    # Final checklist
    print_step(7, "Pre-Deployment Checklist")
    
    checklist = [
        ("Code tested locally", ""),
        ("All imports working", ""),
        ("requirements.txt complete", ""),
        ("Procfile created", ""),
        ("render.yaml created", ""),
        (".gitignore created", ""),
        ("Git initialized", ""),
        ("Ready for GitHub", ""),
    ]
    
    for item, _ in checklist:
        print(f"  ☐ {item}")
    
    print_header("✅ READY FOR DEPLOYMENT")
    
    print("\n  📚 Full guide: Read RENDER_DEPLOYMENT.md")
    print("  🎯 Quick start: Follow the 10 steps above")
    print("  💬 Need help? Check the detailed guide\n")

if __name__ == "__main__":
    main()
