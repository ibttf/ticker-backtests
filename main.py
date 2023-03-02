import yfinance as yf
import datetime
import stockstats

differences=[]
def getDiff(df,buyday,sellday,month,year):

  if not isTradingDay(df,buyday,month,year):
    buyday-=1
    if not isTradingDay(df,buyday,month,year):
      buyday+=2
      if not isTradingDay(df,buyday,month,year):
        buyday+=1
        if not isTradingDay(df,buyday,month,year):
          buyday-=4
  if not isTradingDay(df,sellday,month,year):
    sellday-=1
    if not isTradingDay(df,sellday,month,year):
      sellday+=2
      if not isTradingDay(df,sellday,month,year):
        sellday+=1
        if not isTradingDay(df,sellday,month,year):
          sellday-=4        
  buyIndex=str(year)+"-"+"{:02d}".format(month)+"-"+ "{:02d}".format(buyday)
  sellIndex=str(year)+"-"+"{:02d}".format(month)+"-"+ "{:02d}".format(sellday)


  for index, row in df.iterrows():
    if str(index)[:-9]==buyIndex:
      buyPrice=row["Close"]
    if str(index)[:-9]==sellIndex:
      sellPrice=row["Close"]
  return 100*(sellPrice-buyPrice)/buyPrice
  





def isTradingDay(df,day,month,year):
  for index,row in df.iterrows():
    if str(year)+"-"+"{:02d}".format(month)+"-"+ "{:02d}".format(day)==str(index)[:-9]:
      return True
  return False


def checkForRsi(ticker,day):
  try:
    stockData=yf.Ticker(ticker)
    dateFormat="%Y-%m-%d"
    start=day-datetime.timedelta(days=10)
    start=start.strftime(dateFormat)
    end=day
    end=end.strftime(dateFormat)
    dataFrame=stockData.history(interval="1d",start=start,end=end)
    stockData=stockstats.StockDataFrame.retype(dataFrame)

    rsi=stockData["rsi_14"][-1]
    previousRsi=stockData["rsi_14"][-2]
    rsiGood=False
    if rsi<50 and rsi>previousRsi:
      rsiGood=True
    return rsiGood

  except Exception:
    return False
    #change it to False to consider RSI, true to not consider it


tick=input("What ticker would you like to backtest?")
Ticker=yf.Ticker(tick)
data=Ticker.history(period="max",start="2016-01-01",end="2021-09-29")

startYear=int(input("What year would you like to start testing your data from?"))
endYear=2023
currentMonth=2
buyDay=int(input("What day would you like to buy the stock? "))
sellDay=int(input("What day would you like to sell the stock? "))
total=0
bestBuyDay=3
bestSellDay=22
bestAverage=-5

"""
#To find the best buy/sell points within a month.
#for buyDay in range(3,13):
for sellDay in range(14,27):
  for y in range(startYear,endYear+1):
    for m in range(1,13):
      
      if y==endYear and m>currentMonth:
        break
      #if checkForRsi("UVXY",datetime.datetime(y,m,buyDay)):
      difference=(getDiff(data,buyDay,sellDay,m,y))
      differences.append(difference)
      total+=difference
      print(str(y)+"-"+str(m)+":  " + str(difference))
  average=total/len(differences)
  if int(average)>int(bestAverage):
    bestAverage=average
    bestBuyDay=buyDay
    bestSellDay=sellDay
print(str(bestBuyDay)+"-"+str(bestSellDay)+"-"+str(bestAverage))
"""

#to just calculate for arbitrary buyday and sellday

for y in range(startYear,endYear+1):
  for m in range(1,13):
        
    if y==endYear and m>currentMonth:
      break
    #if checkForRsi("UVXY",datetime.datetime(y,m,buyDay)):
    difference=(getDiff(data,buyDay,sellDay,m,y))
    print("Return for " + str(m)  +"-" + str(y)+ ": " + str(difference))
    differences.append(difference)
      
    total+=difference
average=total/len(differences)

print("___________________________")  

print("The average percent return if you bought on the "+str(buyDay) +" of every month and sold on the "+str(sellDay)+" of every month would be: " + str(average))

print("___________________________")  
pos_count, neg_count = 0, 0
  
# iterating each number in list
for num in differences:
      
    # checking condition
    if num >= 0:
        pos_count += 1
  
    else:
        neg_count += 1
                 
print("Profitable trades: ", pos_count)
print("___________________________")  
print("Loss trades: ", neg_count)
print("___________________________")  
print("Percent profitable trades: "+str(pos_count/(pos_count+neg_count))) 