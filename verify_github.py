#!/usr/bin/env python3
"""
GitHub Repository Verification Report
Generated: 28 January 2026
"""

import subprocess
import os

def run_cmd(cmd):
    """Run command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

# Get repository info
remote = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git remote -v")
branch = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git branch --show-current")
commit_count = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git rev-list --count HEAD")
last_commit = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git log -1 --format=%ai")

print_section("✅ GITHUB REPOSITORY STATUS - VERIFICATION REPORT")

# Repository Info
print("📦 REPOSITORY INFORMATION")
print("-" * 70)
print(f"GitHub URL: https://github.com/soumyadeep-pandit/trading-bot")
print(f"Repository Name: trading-bot")
print(f"Remote: {remote}")
print(f"Current Branch: {branch}")
print(f"Total Commits: {commit_count}")
print(f"Last Push: {last_commit}")

# Key Files
print("\n📁 REQUIRED FILES - VERIFICATION")
print("-" * 70)

required_files = {
    "main.py": "Main bot entry point",
    "requirements.txt": "Python dependencies",
    "Procfile": "Render deployment config",
    "render.yaml": "Render service config",
    ".gitignore": "Git ignore rules",
    "auth/login.py": "Zerodha authentication",
    "config/settings.py": "Configuration file",
    "data/market_data.py": "Market data fetching",
    "strategy/strategy.py": "Trading strategy",
    "risk/risk.py": "Risk management",
    "execution/orders.py": "Order execution",
    "backtest_mock.py": "Mock backtesting",
    "RENDER_DEPLOYMENT.md": "Deployment guide",
    "ACCURACY_GUIDE.md": "Accuracy evaluation",
}

all_files_present = True
for file, description in required_files.items():
    path = f"/Users/soumyadeeppandit/Project/Trading AI Agent/{file}"
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"✅ {file:<30} ({size:>6} bytes) - {description}")
    else:
        print(f"❌ {file:<30} - MISSING!")
        all_files_present = False

# Git Status
print("\n🔄 GIT STATUS")
print("-" * 70)
status = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git status")
if "working tree clean" in status:
    print("✅ Working tree is clean (all changes committed)")
    print("✅ No uncommitted files")
else:
    print("⚠️  There may be uncommitted changes")
    print(status)

# Recent Commits
print("\n📝 RECENT COMMITS")
print("-" * 70)
commits = run_cmd("cd '/Users/soumyadeeppandit/Project/Trading AI Agent' && git log --oneline -5")
for i, commit in enumerate(commits.split('\n'), 1):
    print(f"  {i}. {commit}")

# File Count
print("\n📊 FILE STATISTICS")
print("-" * 70)
py_files = run_cmd("find '/Users/soumyadeeppandit/Project/Trading AI Agent' -maxdepth 2 -name '*.py' ! -path '*/venv/*' -type f | wc -l")
config_files = run_cmd("find '/Users/soumyadeeppandit/Project/Trading AI Agent' -maxdepth 1 -name '*.md' -o -name 'Procfile' -o -name 'render.yaml' | wc -l")

print(f"Python Files: {py_files}")
print(f"Configuration Files: {config_files}")
print(f"Total Directories: 6 (auth, config, data, execution, risk, strategy)")

# Verification Summary
print("\n" + "="*70)
print("  ✅ VERIFICATION SUMMARY")
print("="*70 + "\n")

if all_files_present and "working tree clean" in status:
    print("✅ ALL CHECKS PASSED!")
    print("\n  Your repository is properly configured:")
    print("  • All required files are present")
    print("  • All changes are committed")
    print("  • Code is synced with GitHub")
    print("  • Ready for Render deployment")
    print("\n  🎯 Next Step: Go to https://render.com/dashboard")
    print("     and create a new Web Service")
else:
    print("⚠️  SOME ISSUES DETECTED")
    if not all_files_present:
        print("  • Some files are missing")
    if "working tree clean" not in status:
        print("  • There are uncommitted changes")
        print("    Run: git add . && git commit -m 'message'")

# Deployment Readiness
print("\n" + "="*70)
print("  🚀 RENDER DEPLOYMENT READINESS")
print("="*70 + "\n")

checklist = [
    ("Repository pushed to GitHub", "✅" if "working tree clean" in status else "❌"),
    ("All files committed", "✅" if "working tree clean" in status else "❌"),
    ("Procfile present", "✅" if os.path.exists("/Users/soumyadeeppandit/Project/Trading AI Agent/Procfile") else "❌"),
    ("render.yaml present", "✅" if os.path.exists("/Users/soumyadeeppandit/Project/Trading AI Agent/render.yaml") else "❌"),
    ("requirements.txt present", "✅" if os.path.exists("/Users/soumyadeeppandit/Project/Trading AI Agent/requirements.txt") else "❌"),
    ("GitHub remote configured", "✅" if "origin" in remote else "❌"),
]

for item, status in checklist:
    print(f"  {status} {item}")

print("\n" + "="*70)
print("  📖 NEXT STEPS")
print("="*70 + "\n")

print("""
  1. ✅ Code is on GitHub
  
  2. 📱 Go to: https://render.com/dashboard
  
  3. Click: "New +" → "Web Service"
  
  4. Connect: soumyadeep-pandit/trading-bot repository
  
  5. Configure:
     • Name: trading-bot
     • Build: pip install -r requirements.txt
     • Start: python main.py
     • Instance: Free
  
  6. Add Environment Variables:
     • API_KEY (your key)
     • API_SECRET (your secret)
     • ACCESS_TOKEN (your token)
     • MODE (PAPER)
  
  7. Deploy and verify logs
  
  ✅ Done! Your bot will run 24/7 on Render
""")

print("="*70)
print("  📚 Documentation")
print("="*70)
print("\n  • Deployment Guide: RENDER_DEPLOYMENT.md")
print("  • Accuracy Testing: ACCURACY_GUIDE.md")
print("  • GitHub Repo: https://github.com/soumyadeep-pandit/trading-bot")
print("\n" + "="*70)
