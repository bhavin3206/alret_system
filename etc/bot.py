# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
import pyotp

api_key = 'NYKYuBV9'
username = 'V60263464'
pwd = '3011'
smartApi = SmartConnect(api_key)
try:
    token = "VGUQL3STRLPAG2T6L34CH2KZVM"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    print(e)

correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)
breakpoint()
if data['status'] == False:
    print(data)
    
else:
    # login api call
    # logger.info(f"You Credentials: {data}")
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
#     # fetch the feedtoken
    feedToken = smartApi.getfeedToken()
#     # fetch User Profile
#     res = smartApi.getProfile(refreshToken)
#     smartApi.generateToken(refreshToken)
#     res=res['data']['exchanges']

#     #gtt rule creation
#     try:
#         gttCreateParams={
#                 "tradingsymbol" : "SBIN-EQ",
#                 "symboltoken" : "3045",
#                 "exchange" : "NSE", 
#                 "producttype" : "MARGIN",
#                 "transactiontype" : "BUY",
#                 "price" : 100000,
#                 "qty" : 10,
#                 "disclosedqty": 10,
#                 "triggerprice" : 200000,
#                 "timeperiod" : 365
#             }
#         rule_id=smartApi.gttCreateRule(gttCreateParams)
#         logger.info(f"The GTT rule id is: {rule_id}")
#     except Exception as e:
#         logger.exception(f"GTT Rule creation failed: {e}")
        
#     #gtt rule list
#     try:
#         status=["FORALL"] #should be a list
#         page=1
#         count=10
#         lists=smartApi.gttLists(status,page,count)
#     except Exception as e:
#         logger.exception(f"GTT Rule List failed: {e}")

#     #Historic api
#     try:
#         historicParam={
#         "exchange": "NSE",
#         "symboltoken": "3045",
#         "interval": "ONE_MINUTE",
#         "fromdate": "2021-02-08 09:00", 
#         "todate": "2021-02-08 09:16"
#         }
#         smartApi.getCandleData(historicParam)
#     except Exception as e:
#         logger.exception(f"Historic Api failed: {e}")
#     #logout
#     try:
#         logout=smartApi.terminateSession('Your Client Id')
#         logger.info("Logout Successfull")
#     except Exception as e:
#         logger.exception(f"Logout failed: {e}")


#     from SmartApi.smartWebSocketV2 import SmartWebSocketV2
#     from logzero import logger

#     AUTH_TOKEN = "Your Auth_Token"
#     API_KEY = "Your Api_Key"
#     CLIENT_CODE = "Your Client Code"
#     FEED_TOKEN = "Your Feed_Token"
#     correlation_id = "abc123"
#     action = 1
#     mode = 1
#     token_list = [
#         {
#             "exchangeType": 1,
#             "tokens": ["26009"]
#         }
#     ]
#     #retry_strategy=0 for simple retry mechanism
#     sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=2, retry_strategy=0, retry_delay=10, retry_duration=30)

#     #retry_strategy=1 for exponential retry mechanism
#     # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)

#     def on_data(wsapp, message):
#         logger.info("Ticks: {}".format(message))
#         # close_connection()

#     def on_control_message(wsapp, message):
#         logger.info(f"Control Message: {message}")

#     def on_open(wsapp):
#         logger.info("on open")
#         some_error_condition = False
#         if some_error_condition:
#             error_message = "Simulated error"
#             if hasattr(wsapp, 'on_error'):
#                 wsapp.on_error("Custom Error Type", error_message)
#         else:
#             sws.subscribe(correlation_id, mode, token_list)
#             # sws.unsubscribe(correlation_id, mode, token_list1)

#     def on_error(wsapp, error):
#         logger.error(error)

#     def on_close(wsapp):
#         logger.info("Close")

#     def close_connection():
#         sws.close_connection()

