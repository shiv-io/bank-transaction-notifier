import telegram
import pandas as pd
import plaid
from datetime import datetime
import config

bot = telegram.Bot(token=config.BOT_TOKEN)

def push_msg(msg):
    bot.send_message(chat_id=config.CHAT_ID, text=msg)

# Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
# password: pass_good)
# Use `development` to test with live users and credentials and `production`
# to go live
PLAID_ENV = 'development'

# PLAID_PRODUCTS is a comma-separated list of products to use when initializing
# Link. Note that this list must contain 'assets' in order for the app to be
# able to create and retrieve asset reports.
PLAID_PRODUCTS = 'transactions'

client = plaid.Client(client_id=config.PLAID_CLIENT_ID, secret=config.PLAID_SECRET,
                      public_key=config.PLAID_PUBLIC_KEY, environment=PLAID_ENV, api_version='2018-05-22')

today = datetime.strftime(datetime.today(), '%Y-%m-%d')

response = client.Transactions.get(config.PLAID_ACCESS_TOKEN, start_date=today, end_date=today, count=100)

transactions = response['transactions']

try:
    df = pd.DataFrame(transactions)[['name','amount']]
    total = '$' + str(df['amount'].sum())
    spend_txt = datetime.strftime(datetime.today(), '%A, %b %d, %Y') + '\n'
    spend_txt += 'Total: ' + total + '\n\n'
    for i in range(len(df)):
        spend_txt += '$' + str(df.iloc[i]['amount']) + ': ' + str(df.iloc[i]['name']) + '\n'

    push_msg(spend_txt)
    print('Successfully ran on ' + today)
except Exception as e:
    if len(transactions) < 1:
        print('No transactions today.')
        push_msg('No transactions today.')
    else:
        print('There was some error on {}'.format(today))
        push_msg('There was some error')
        push_msg(str(e))
