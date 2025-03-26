from pybit.unified_trading import HTTP
from datetime import datetime,timezone,timedelta
import pandas as pd
import config

session = HTTP(
    # testnet=True,
    testnet=False,
    api_key= config.api_key,
    api_secret= config.api_secret,
)

def calculate_time(end_time ,start_time):
    if(i==0):
        current_datetime = datetime.now(timezone.utc) #now time
        past_datetime = current_datetime - timedelta(hours=1000) #time before 1800 mins aka 360 candles type 5mins
        current_timestamp_milliseconds = int(current_datetime.timestamp() * 1000)
        past_timestamp_milliseconds = int(past_datetime.timestamp() * 1000)
    else:
        current_timestamp_milliseconds = start_time
        past_timestamp_milliseconds = current_timestamp_milliseconds - 3600000000 #time before 1800 mins aka 360 candles type 5minsv
    
    return current_timestamp_milliseconds, past_timestamp_milliseconds

def get_candles(symbol,start,end):
    response = session.get_kline(
        category="linear", #linear USDT perpetual, and USDC contract, including USDC perp, USDC futures
        symbol=symbol,
        interval=60,
        start=start,
        end=end,
        limit=1000, #numbers of candles depend on length
    )
    candle_list = response['result']['list'] #candle_list[0] is the latest
    return candle_list

if __name__ == "__main__":
    end_time = start_time = 0
    result = []
    for i in range(10):
        end_time ,start_time = calculate_time(end_time ,start_time)
        candle_list = get_candles("BTCUSDT",start_time,end_time)
        result += candle_list
    df_list = pd.DataFrame(result,columns=["Date","Open","High","Low","Close","Volumn","Turnover"],dtype=float)
    df_list["Date"] = pd.to_datetime(df_list["Date"],unit="ms")
    df_list = df_list.set_index("Date")
    df_list.index = df_list.index.tz_localize('UTC').tz_convert('Etc/GMT-7')
    print(df_list)
    
    df_list.to_excel("BTC_Data.xlsx")
