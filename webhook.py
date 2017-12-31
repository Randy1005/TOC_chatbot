from pprint import pprint
import requests

bot_token = "527773154:AAGWCJJmg9s70uZi4GF3V5d0AIcDUt0IzYg"
test_url = "https://200018b6.ngrok.io/{}".format(bot_token)

def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(bot_token,method)

r = requests.get(get_url("setWebhook"), data={"url": test_url})
r = requests.get(get_url("getWebhookInfo"))
pprint(r.status_code)
pprint(r.json())
