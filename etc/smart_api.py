# package import statement
from SmartApi import SmartConnect #or from SmartApi.smartConnect import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import pyotp, requests
import json, time
from datetime import datetime
import pandas as pd

class Fetch_liveData:
    def __init__(self) -> None:
        self.api_key ="zb1uzu8p"
        self.client_code = "P342447"
        self.password = "2188"
        self.totp = pyotp.TOTP("KVZPGMGGHAILAMGFPRCB2YI5LA").now()
        self.obj=SmartConnect(api_key=self.api_key)
        data = self.obj.generateSession(self.client_code,self.password,self.totp)
        self.refreshToken= data['data']['refreshToken']
        self.jwtToken= data['data']['jwtToken']
        self.feedToken=self.obj.getfeedToken()
        print('feedToken : ',self.feedToken)
        print('jwtToken : ',self.jwtToken)
        # print('banknifty ltp price---->',self.get_ltp_data_banknifty())
        # index_type = 'future'
        # Here 3 name of future and options index 1.NIFTY, 2.FINNIFTY, 3.BANKNIFTY
        # If you want future data pass param in this "get_strike_price" function get_data=='future' by default options
        # price_data = get_strike_price(expiry=current_exp,data=data,nameOfindex=IndexName,index_type=index_type)
        # print(price_data)
        # self.get_ltp_data_banknifty('tradingSymbol','symbolToken')
       
        # If you want ce and pe both in diffrent dict call this fuction this available only on options index 
        # price_data = self.get_strike_price_by_optionType_banknifty_test(expiry=current_exp,data=data,nameOfindex=IndexName)
       
    def get_Open_Api_Data(self):
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)
        data = json.loads(response.content)
        table = pd.DataFrame(data)
        return table


    def get_ltp_data_banknifty(self):
        data = self.obj.ltpData('NSE','BANKNIFTY1','5852')
        return data['data']['ltp']

    def get_ltp_data(self,exchange,tradingsymbol,symboltoken):
        breakpoint()
        data = self.obj.ltpData(exchange,tradingsymbol,symboltoken)
        return data['data']['ltp']
    
    def get_ltp_data_nifty50(self):
        data = self.obj.ltpData('CDS','NIFTY50','2')
        return data['data']['ltp']
      
    def get_ltp_data_banknifty_options(self,symbol,token):
        data = self.obj.ltpData('NFO',str(symbol),str(token))
        return data['data']['ltp']
        
    def get_otm_pe(self):
        
        ...

    def log_out(self):
        try:
            logout=self.obj.terminateSession('P342447')
            print("Logout Successfull")
        except Exception as e:
            print("Logout failed: {}".format(e.message))

    def get_data(self,Symbol=None,token=None):
        AUTH_TOKEN = self.jwtToken
        API_KEY = self.api_key
        CLIENT_CODE = self.client_code
        FEED_TOKEN = self.feedToken

        correlation_id = "new_test_1"
        action = 1
        mode = 1

        token_list = [{"exchangeType": 2, "tokens": token}]

        ss = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)

        def on_data(wsapp, message):
            print("value:-",float(message['last_traded_price']/100))
            return float(message['last_traded_price']/100)

        def on_open(wsapp):
            print("on open")
            ss.subscribe(correlation_id, mode, token_list)


        def on_error(wsapp, error):
            print(error)


        def on_close(wsapp):
            print("Close")

        # Assign the callbacks.
        ss.on_open = on_open
        ss.on_data = on_data
        ss.on_error = on_error
        ss.on_close = on_close
        ss.connect()
    
    def convert_date(self,date_str):
        return datetime.strptime(date_str, '%d%b%Y')

    def get_current_exp(self,data,index_type=None):
        df = data
        if index_type == 'future':
            df = df[(df['name'] == 'NIFTY') & (df['exch_seg'] == 'NFO') & (df['instrumenttype'] == 'FUTIDX')]
            dates = list(df['expiry'].unique())
        else:
            df = df[(df['name'] == 'NIFTY') & (df['exch_seg'] == 'NFO') & (df['instrumenttype'] == 'OPTIDX')]
            dates = list(df['expiry'].unique())
        sorted_dates = sorted(dates, key=self.convert_date)
        current_exp = sorted_dates[0]
        next_exp = sorted_dates[1]
        return current_exp, next_exp


    def option_price_and_type(self,options):
        # # Extract the option type
        option_type = options[-2:]
        # Remove the last two words
        words = options[:-2]
        # Extract the last five words
        strike_price = "".join(words[-5:])
        return option_type, strike_price
    
    def nearest_to_150_from_list(self,numbers):
        return min(numbers, key=lambda x: abs(x - 150.0))

    def get_strike_price_by_optionType_banknifty(self, expiry, data, nameOfindex):
        
        df = data
        filtered_df = df[(df['name'] == 'BANKNIFTY') & (df['exch_seg'] == 'NFO') & (df['expiry'] == str(expiry)) & (df['instrumenttype'] == "OPTIDX")]
        ce_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'CE')
        ce_df = filtered_df[ce_mask]
        ce_df = filtered_df[ce_mask].copy()
        ce_df = ce_df.assign(**{
            'Option_type': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        ltp_price = self.get_ltp_data_banknifty()
        ce_df = ce_df[ce_df['Strike_price'].astype(float) >= float(ltp_price)]
        ce_token = ce_df['token'].astype(str).tolist()
        
        pe_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'PE')
        pe_df = filtered_df[pe_mask]
        pe_df = filtered_df[pe_mask].copy()
        pe_df = pe_df.assign(**{
            'Option_type': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        pe_df = pe_df[pe_df['Strike_price'].astype(float) <= float(ltp_price)]
        pe_token = pe_df['token'].astype(str).tolist()
        sorted_ce_options = ce_df.sort_values(by='Strike_price').to_dict(orient='records')
        sorted_pe_options = pe_df.sort_values(by='Strike_price').to_dict(orient='records')
        sorted_ce_options_new_df = [{'token':d['token'], 'symbol':d['symbol'], 'Option_type':d['Option_type'], 'Strike_price':d['Strike_price']}for d in sorted_ce_options]
        sorted_pe_options_new_df = [{'token':d['token'], 'symbol':d['symbol'], 'Option_type':d['Option_type'], 'Strike_price':d['Strike_price']}for d in sorted_pe_options]
        sorted_ce_options_new_df = pd.DataFrame(sorted_ce_options_new_df)
        sorted_ce_options_new_df = sorted_ce_options_new_df.assign(**{
            'ltp':sorted_ce_options_new_df.apply(lambda sorted_ce_options_new_df : self.get_ltp_data_banknifty_options(sorted_ce_options_new_df['symbol'],sorted_ce_options_new_df['token']), axis = 1)
        })
        sorted_pe_options_new_df = pd.DataFrame(sorted_pe_options_new_df)
        sorted_pe_options_new_df = sorted_pe_options_new_df.assign(**{
            'ltp':sorted_pe_options_new_df.apply(lambda sorted_pe_options_new_df : self.get_ltp_data_banknifty_options(sorted_pe_options_new_df['symbol'],sorted_pe_options_new_df['token']), axis = 1)
        })
        ce_ltp_option = sorted_ce_options_new_df.loc[sorted_ce_options_new_df['ltp'].apply(lambda x: abs(x - 150)).idxmin()]
        pe_ltp_option = sorted_pe_options_new_df.loc[sorted_pe_options_new_df['ltp'].apply(lambda x: abs(x - 150)).idxmin()]

        return ce_ltp_option, pe_ltp_option

    def get_strike_price_by_optionType_banknifty_test(self, expiry, data, nameOfindex):
        df = data
        filtered_df = df[(df['name'] == 'BANKNIFTY') & (df['exch_seg'] == 'NFO') & (df['expiry'] == str(expiry)) & (df['instrumenttype'] == "OPTIDX")]
        ce_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'CE')
        ce_df = filtered_df[ce_mask].copy()
        ce_df = ce_df.assign(**{
            'Option_type': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': ce_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        ltp_price = self.get_ltp_data_banknifty()
        ce_df = ce_df[ce_df['Strike_price'].astype(float) >= float(ltp_price)]
        ce_df = ce_df.assign(**{
            'ltp': ce_df.apply(lambda x: self.get_ltp_data_banknifty_options(x['symbol'], x['token']), axis=1),
        })
        ce_df = ce_df[ce_df['ltp'].apply(lambda x: abs(x - 150) <= 150)]
        ce_df = ce_df.sort_values(by='Strike_price')
        ce_ltp_option = ce_df.loc[ce_df['ltp'].apply(lambda x: abs(x - 150)).idxmin()]

        pe_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'PE')
        pe_df = filtered_df[pe_mask].copy()
        pe_df = pe_df.assign(**{
            'Option_type': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0]),
            'Strike_price': pe_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[1]),
        })
        pe_df = pe_df[pe_df['Strike_price'].astype(float) <= float(ltp_price)]
        pe_df = pe_df.assign(**{
            'ltp': pe_df.apply(lambda x: self.get_ltp_data_banknifty_options(x['symbol'], x['token']), axis=1),
        })
        pe_df = pe_df[pe_df['ltp'].apply(lambda x: abs(x - 150) <= 150)]
        pe_df = pe_df.sort_values(by='Strike_price')
        pe_ltp_option = pe_df.loc[pe_df['ltp'].apply(lambda x: abs(x - 150)).idxmin()]
        return ce_ltp_option, pe_ltp_option


Fetch_liveData()


if __name__=='__main__':
    live_data = Fetch_liveData()
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url, timeout=300)
    data = response.json()

    for i in data:
        if i['token'] and i['symbol'] and i['exch_seg']:
            data = live_data.get_ltp_data(i['exch_seg'], i['token'] ,i['symbol'])
            if int(data) == 50440 or int(data) == 50441:
                print(data)


    # data = live_data.get_Open_Api_Data()
    # current_exp, next_exp = live_data.get_current_exp(data=data)
    # IndexName = 'BANKNIFTY'
    # start_time = time.time()
    # option = live_data.get_strike_price_by_optionType_banknifty(expiry=next_exp, data=data, nameOfindex=IndexName)
    # end_time = time.time()
    # print("Runtime: ", end_time - start_time, " seconds")
    # ce_option = option[0]
    # pe_option = option[1]
    # print(ce_option)
    # print(pe_option)
    # print('ce_option--->',ce_option,'pe_option--->',pe_option)






# import pandas as pd

# def get_strike_price_by_optionType(self, expiry, data, nameOfindex):
    
#     df = pd.DataFrame(data)
#     filtered_df = df[(df['name'] == 'BANKNIFTY') & (df['exch_seg'] == 'NFO') & (df['expiry'] == str(expiry)) & (df['instrumenttype'] == "OPTIDX")]

#     ce_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'CE')
#     ce_df = filtered_df[ce_mask]
#     ltp_price = self.get_ltp_data_banknifty()
#     ce_df = ce_df[ce_df['StrikePrice'].astype(float) >= float(ltp_price)]
#     ce_token = ce_df['token'].astype(str).tolist()

#     pe_mask = filtered_df['symbol'].apply(lambda x: self.option_price_and_type(options=x)[0] == 'PE')
#     pe_df = filtered_df[pe_mask]
#     pe_df = pe_df[pe_df['StrikePrice'].astype(float) <= float(ltp_price)]
#     pe_token = pe_df['token'].astype(str).tolist()

#     sorted_ce_options = ce_df.sort_values(by='StrikePrice').to_dict(orient='records')
#     sorted_pe_options = pe_df.sort_values(by='StrikePrice').to_dict(orient='records')

#     strike_price_data = [sorted_ce_options, ce_token, sorted_pe_options, pe_token]
#     return strike_price_data

