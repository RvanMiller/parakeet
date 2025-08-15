import os
from time import sleep

import pyotp
import robinhood_client as rh
from dotenv import load_dotenv

'''
This is an example script that will automatically retry an order 
up to a maximum number of retries if the order does not go through.

NOTE: View the two_factor_log_in.py script to see how automatic
two-factor log in works.
'''
### REPLACE ME - order is to buy 1000 shares of BRK.A which should fail for most people
stock = "BRK.A"
quantity = 1000
max_attempts = 10
sleep_time = 1 # in seconds
###
# Load environment variables
load_dotenv()
# Login using two-factor code
totp = pyotp.TOTP(os.environ['rh_mfa_code']).now()
login = rh.login(os.environ['rh_username'], os.environ['rh_password'], store_session=True, mfa_code=totp)
# Here it is important to set jsonify=False so that you can check
# status code of your order request. 200 is ok, 400 is bad request,
# and 404 is unknown url.
order = rh.order_buy_market(stock, quantity, jsonify=False)
# Feel free to use more advanced orders
attempts = 0
while order.status_code != 200 and attempts < max_attempts:
    order = rh.order_buy_market(stock, quantity, jsonify=False)
    attempts += 1
    sleep(sleep_time)

if attempts == max_attempts:
    print(f"ERROR CODE: {order.status_code}")
    print("max number of tries exceeded. Order failed because ")
    data = order.json()
    print(data['detail'])
