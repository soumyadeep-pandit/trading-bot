from kiteconnect import KiteConnect
import webbrowser

from config.settings import API_KEY, API_SECRET


kite = KiteConnect(api_key=API_KEY)

print("Opening login...")
webbrowser.open(kite.login_url())

token = input("Paste request token: ")

data = kite.generate_session(token, API_SECRET)

if isinstance(data, dict):
    print("ACCESS TOKEN:", data.get("access_token"))
else:
    print("Session data:", data)
