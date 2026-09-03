import yfinance # 套件名稱
from pprint import pprint
from apps.clear import clear

def get_stock_info_(stock):
    yf = yfinance.Ticker(stock)    # 基本用法
    pprint(f'{stock} 的開盤價：{yf.fast_info['open']}')
    pprint(f'{stock} 的收盤價：{yf.fast_info['previousClose']}')
    pprint(f'{stock} 單日最高價：{yf.fast_info['dayHigh']}')
    pprint(f'{stock} 單日最低價：{yf.fast_info['dayLow']}')
    pprint(f'{stock} 單日最低價：{yf.fast_info.get('dayLow')}')





# stock = "NVDA"  # 股票代號，台積電為 2330.TW，台灣股票代號需加上 .TW

# yf = yfinance.Ticker(stock)    # 基本用法

# # pprint(yf.dividends)    # 取得股息資料
# # pprint(yf.splits)    # 取得拆股資料
# # pprint(yf.actions)    # 取得股息與拆股資料
# # pprint(yf.fast_info)    # 取得快速資訊

# pprint(f'{stock} 的詳細資料如下：')
# pprint(yf.fast_info)
# print()


