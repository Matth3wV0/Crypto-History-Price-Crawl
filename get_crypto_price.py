from datetime import datetime,timezone,timedelta,date
import calendar
import time
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

class Candle:
    def __init__(self,startTime,openPrice,highPrice,lowPrice,closePrice,volume,turnover):
        self.startTime = startTime
        self.openPrice = openPrice
        self.highPrice = highPrice
        self.lowPrice = lowPrice
        self.closePrice	= closePrice
        self.volume = volume
        self.turnover = turnover

session = HTTP(
    # testnet=True,
    testnet=False,
    api_key=os.getenv("API_KEY_SUBACCOUNT"),
    api_secret=os.getenv("API_SECRET_SUBACCOUNT"),
)

def get_days_apart():
    today = date.today()
    first_day_of_year = date(today.year, 1, 1)
    # print(today)
    # print(first_day_of_year)
    days_apart = 0
    current_date = first_day_of_year

    while current_date <= today:
        if current_date.weekday() < 7:  # Monday to Friday (0 to 4)
            # print(current_date)
            days_apart += 1
        current_date += timedelta(days=1)

    # print("Number of business days apart:", days_apart)
    return days_apart

def calculate_time(days_apart,countback_day):
    # current_datetime = datetime.now(timezone.utc) #now time
    # current_datetime = countback_day 
    # past_datetime = current_datetime - timedelta(minutes=24*60*int(days_apart)) #time before 1800 mins aka 360 candles type 5mins
    # print(current_datetime)
    # print(past_datetime)
    # print(current_datetime)
    # print(past_datetime)

    # current_timestamp_milliseconds = int(current_datetime.timestamp() * 1000)
    current_timestamp_milliseconds = countback_day * 1000
    past_timestamp_milliseconds = current_timestamp_milliseconds - 24*60*int(days_apart)*60*1000
    
    return current_timestamp_milliseconds, past_timestamp_milliseconds

def get_countback_day(year,today):
    if(year == today.year):
        countback_day = calendar.timegm(time.strptime(f'{today}T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ'))
    else:
        countback_day = calendar.timegm(time.strptime(f'{year}-12-31T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.%fZ'))
    return countback_day

def get_candles(symbol,start,end,days_apart):
    # session = HTTP(testnet=True)
    response = session.get_kline(
        category="linear", #linear USDT perpetual, and USDC contract, including USDC perp, USDC futures
        symbol=symbol,
        interval="D",
        start=start,
        end=end,
        # limit=3605, #hardcode 1805 -> get 361 candles type 5 mins still now go to past -> (11/02/2024) WRONG 
        # limit=720, #hardcode 720 -> get 720 candles still now go to past
        limit=str(days_apart), #numbers of candles depend on length
    )
    
    candle_list = response['result']['list']
    return candle_list

def formated_date(your_timestamp_milliseconds):
    # your_timestamp_milliseconds = 1692748800000# Replace this with your long date value in milliseconds
    # print(your_timestamp_milliseconds)
    # Convert milliseconds timestamp to seconds and then to datetime object
    dt_object_milliseconds = datetime.utcfromtimestamp(your_timestamp_milliseconds / 1000)

    # Format the datetime object as a string in dd-mm-yyyy format
    formatted_date_milliseconds = dt_object_milliseconds.strftime('%d/%m/%Y, %H:%M:%S')

    return formatted_date_milliseconds

    
symbol_list = ['BTCUSDT','ETHUSDT','10000000AIDOGEUSDT', '10000COQUSDT', '10000LADYSUSDT', '10000NFTUSDT', '10000SATSUSDT', '10000STARLUSDT', '10000WENUSDT', '1000BONKUSDT', '1000BTTUSDT', '1000FLOKIUSDT', '1000IQ50USDT', '1000LUNCUSDT', '1000PEPEPERP', '1000PEPEUSDT', '1000RATSUSDT', '1000TURBOUSDT', '1000XECUSDT', '1CATUSDT', '1INCHUSDT', 'AAVEUSDT', 'ACEUSDT', 'ACHUSDT', 'ADAUSDT', 'AERGOUSDT', 'AEVOUSDT', 'AGIUSDT', 'AGIXUSDT', 'AGLDUSDT', 'AIUSDT', 'AKROUSDT', 'ALGOUSDT', 'ALICEUSDT', 'ALPACAUSDT', 'ALPHAUSDT', 'ALTUSDT', 'AMBUSDT', 'ANKRUSDT', 'ANTUSDT', 'APEUSDT', 'API3USDT', 'APTUSDT', 'ARBPERP', 'ARBUSDT', 'ARKMUSDT', 'ARKUSDT', 'ARPAUSDT', 'ARUSDT', 'ASTRUSDT', 'ATAUSDT', 'ATOMUSDT', 'AUCTIONUSDT', 'AUDIOUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 'BADGERUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BCHUSDT', 'BEAMUSDT', 'BELUSDT', 'BICOUSDT', 'BIGTIMEUSDT', 'BLURUSDT', 'BLZUSDT', 'BNBPERP', 'BNBUSDT', 'BNTUSDT', 'BNXUSDT', 'BOBAUSDT', 'BOMEUSDT', 'BONDUSDT', 'BRETTUSDT', 'BSVUSDT', 'BSWUSDT', 'BTC-10MAY24', 'BTC-17MAY24', 'BTC-24MAY24', 'BTC-27DEC24', 'BTC-27SEP24', 'BTC-28JUN24', 'BTC-28MAR25', 'BTC-31MAY24', 'BTCPERP', 'C98USDT', 'CAKEUSDT', 'CEEKUSDT', 'CELOUSDT', 'CELRUSDT', 'CETUSUSDT', 'CFXUSDT', 'CHRUSDT', 'CHZUSDT', 'CKBUSDT', 'COMBOUSDT', 'COMPUSDT', 'COREUSDT', 'COTIUSDT', 'COVALUSDT', 'CROUSDT', 'CRVUSDT', 'CTCUSDT', 'CTKUSDT', 'CTSIUSDT', 'CVCUSDT', 'CVXUSDT', 'CYBERUSDT', 'DAOUSDT', 'DARUSDT', 'DASHUSDT', 'DATAUSDT', 'DEGENUSDT', 'DENTUSDT', 'DGBUSDT', 'DODOUSDT', 'DOGEPERP', 'DOGEUSDT', 'DOTUSDT', 'DUSKUSDT', 'DYDXUSDT', 'DYMUSDT', 'EDUUSDT', 'EGLDUSDT', 'ENAUSDT', 'ENJUSDT', 'ENSUSDT', 'EOSUSDT', 'ETCPERP', 'ETCUSDT', 'ETH-10MAY24', 'ETH-17MAY24', 'ETH-24MAY24', 'ETH-27DEC24', 'ETH-27SEP24', 'ETH-28JUN24', 'ETH-28MAR25', 'ETH-31MAY24', 'ETHFIPERP', 'ETHFIUSDT', 'ETHPERP', 'ETHWUSDT', 'FETUSDT', 'FILUSDT', 'FITFIUSDT', 'FLMUSDT', 'FLOWUSDT', 'FLRUSDT', 'FORTHUSDT', 'FOXYUSDT', 'FRONTUSDT', 'FTMUSDT', 'FUNUSDT', 'FXSUSDT', 'GALAUSDT', 'GALUSDT', 'GASUSDT', 'GFTUSDT', 'GLMRUSDT', 'GLMUSDT', 'GMTUSDT', 'GMXUSDT', 'GODSUSDT', 'GRTUSDT', 'GTCUSDT', 'HBARUSDT', 'HFTUSDT', 'HIFIUSDT', 'HIGHUSDT', 'HNTUSDT', 'HOOKUSDT', 'HOTUSDT', 'ICPUSDT', 'ICXUSDT', 'IDEXUSDT', 'IDUSDT', 'ILVUSDT', 'IMXUSDT', 'INJUSDT', 'IOSTUSDT', 'IOTAUSDT', 'IOTXUSDT', 'JASMYUSDT', 'JOEUSDT', 'JSTUSDT', 'JTOUSDT', 'JUPUSDT', 'KASUSDT', 'KAVAUSDT', 'KDAUSDT', 'KEYUSDT', 'KLAYUSDT', 'KNCUSDT', 'KSMUSDT', 'LAIUSDT', 'LDOUSDT', 'LEVERUSDT', 'LINAUSDT', 'LINKUSDT', 'LITUSDT', 'LOOKSUSDT', 'LOOMUSDT', 'LPTUSDT', 'LQTYUSDT', 'LRCUSDT', 'LSKUSDT', 'LTCUSDT', 'LTOUSDT', 'LUNA2USDT', 'MAGICUSDT', 'MANAUSDT', 'MANTAUSDT', 'MASKUSDT', 'MATICPERP', 'MATICUSDT', 'MAVIAUSDT', 'MAVUSDT', 'MBLUSDT', 'MBOXUSDT', 'MDTUSDT', 'MEMEUSDT', 'MERLUSDT', 'METISUSDT', 'MEWUSDT', 'MINAUSDT', 'MKRUSDT', 'MNTPERP', 'MNTUSDT', 'MOBILEUSDT', 'MOVRUSDT', 'MTLUSDT', 'MYRIAUSDT', 'MYROUSDT', 'NEARUSDT', 'NEOUSDT', 'NFPUSDT', 'NKNUSDT', 'NMRUSDT', 'NTRNUSDT', 'OCEANUSDT', 'OGNUSDT', 'OGUSDT', 'OMGUSDT', 'OMNIUSDT', 'OMUSDT', 'ONDOUSDT', 'ONEUSDT', 'ONGUSDT', 'ONTUSDT', 'OPPERP', 'OPUSDT', 'ORBSUSDT', 'ORCAUSDT', 'ORDIPERP', 'ORDIUSDT', 'ORNUSDT', 'OXTUSDT', 'PAXGUSDT', 'PENDLEUSDT', 'PEOPLEUSDT', 'PERPUSDT', 'PHBUSDT', 'PIXELUSDT', 'POLYXUSDT', 'POPCATUSDT', 'PORTALUSDT', 'POWRUSDT', 'PROMUSDT', 'PUNDUUSDT', 'PYTHUSDT', 'QIUSDT', 'QNTUSDT', 'QTUMUSDT', 'RADUSDT', 'RAREUSDT', 'RDNTUSDT', 'REEFUSDT', 'RENUSDT', 'REQUSDT', 'RIFUSDT', 'RLCUSDT', 'RNDRUSDT', 'RONUSDT', 'ROSEUSDT', 'RPLUSDT', 'RSRUSDT', 'RSS3USDT', 'RUNEUSDT', 'RVNUSDT', 'SAFEUSDT', 'SAGAUSDT', 'SANDUSDT', 'SCAUSDT', 'SCRTUSDT', 'SCUSDT', 'SEIUSDT', 'SFPUSDT', 'SHIB1000USDT', 'SILLYUSDT', 'SKLUSDT', 'SLERFUSDT', 'SLPUSDT', 'SNTUSDT', 'SNXUSDT', 'SOLPERP', 'SOLUSDT', 'SPELLUSDT', 'SSVUSDT', 'STEEMUSDT', 'STGUSDT', 'STMXUSDT', 'STORJUSDT', 'STPTUSDT', 'STRKUSDT', 'STXUSDT', 'SUIPERP', 'SUIUSDT', 'SUNUSDT', 'SUPERUSDT', 'SUSHIUSDT', 'SWEATUSDT', 'SXPUSDT', 'TAOUSDT', 'THETAUSDT', 'TIAUSDT', 'TLMUSDT', 'TNSRUSDT', 'TOKENUSDT', 'TOMIUSDT', 'TONUSDT', 'TRBUSDT', 'TRUUSDT', 'TRXUSDT', 'TUSDT', 'TWTUSDT', 'UMAUSDT', 'UNFIUSDT', 'UNIUSDT', 'USDCUSDT', 'USTCUSDT', 'VANRYUSDT', 'VETUSDT', 'VGXUSDT', 'VRAUSDT', 'VTHOUSDT', 'WAVESUSDT', 'WAXPUSDT', 'WIFUSDT', 'WLDUSDT', 'WOOUSDT', 'WUSDT', 'XAIUSDT', 'XCNUSDT', 'XEMUSDT', 'XLMUSDT', 'XMRUSDT', 'XNOUSDT', 'XRDUSDT', 'XRPPERP', 'XRPUSDT', 'XTZUSDT', 'XVGUSDT', 'XVSUSDT', 'YFIUSDT', 'YGGUSDT', 'ZBCNUSDT', 'ZECUSDT', 'ZENUSDT', 'ZETAUSDT', 'ZEUSUSDT', 'ZILUSDT', 'ZKFUSDT', 'ZKUSDT', 'ZRXUSDT']
# symbol_list = ['BTCUSDT',"ETHUSDT"]
if __name__ == "__main__":
    year_list = [2024,2023]
    # today = date.today()
    today = datetime.now(timezone.utc).date()
    # print(today)
    df_list = []
    # total_close_price_list = []
    date_list = []
    formated_date_list = []
    for j,symbol in enumerate(symbol_list):
        # print(len(candle_obj_list))
        close_price_list = []
        candle_obj_list = []
        
        # print("XXX")
        # print(symbol)
        # print("XXX")
        
        for year in year_list:
            days_apart = "365"                                       #hard code days apart for past year
            # print("\n"+ str(year)+ code +"\n")
            if(year == today.year):                             #only current year need to change days apart
                # print(str(year) + " "+ str(today.year))
                days_apart = get_days_apart()
            countback_day = get_countback_day(year,today)                 #get the day end of the year and convert it to Long type
            
            #each 86400 is a day distance
            if(j==0):
                for i in range(int(days_apart)):
                    date_list.append(str((countback_day-(i*86400))*1000))
                    formated_day = formated_date((countback_day-(i*86400))*1000)
                    formated_date_list.append(formated_day)
            #countback_day == endTime
            # print(countback_day)
            # print(days_apart)

            end_time ,start_time = calculate_time(days_apart,countback_day)
            candle_list = get_candles(symbol,start_time,end_time,days_apart)
            # print(symbol)
            # print(candle_list)
            for i,candle in enumerate(candle_list):
                candle_obj = Candle(candle[0],candle[1],candle[2],candle[3],candle[4],candle[5],candle[6])
                candle_obj_list.append(candle_obj)

                if(candle_obj_list[i].startTime==date_list[i]):
                    close_price_list.append(candle_obj.closePrice)
                else:
                    print(f"{candle_obj.startTime}!={date_list[i]}")
                    print("XXX")
                    close_price_list.append("")
                        
            # print(f"Len close price list = {len(close_price_list)}")
            # print(f"{symbol} close price list = ",end="")
            # print(close_price_list)
            # print(f"Len candle list = {len(candle_list)}")
            # print(f"{symbol} candle obj list = ",end="")
            # print(candle_list)
            # print(f"Len date list = {len(date_list)}")
            # print(f"{symbol} date_list = ",end="")
            # print(date_list)
            
            
            # print(end_time)
            # print(start_time)
            # print(candle_list)
            # print(len(candle_list))
        if(j==0):
            # df_list.append(date_list)
            df_list.append(formated_date_list)
            df_list.append(close_price_list)
        else:
            df_list.append(close_price_list)
        # print(df_list)
    # print(symbol_list)
    symbol_list.insert(0,"Date")
    
    # print(symbol_list)
    # print(len(symbol_list))
    # print(df_list)
    # print(len(df_list))
    df = pd.DataFrame(df_list,index=symbol_list)
    print(df)
    transpose_df = df.transpose()
    # transpose_df['Date'] = pd.to_datetime(transpose_df['Date'],unit='ms',errors='coerce')
    transpose_df.to_excel("D:\\Tool\\get_stock_history_price\\crypto_close_price_3.xlsx")
    print(transpose_df)
    