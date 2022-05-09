import time
from types import MethodDescriptorType
from unicodedata import name
from flask import Flask, jsonify,request
import datetime
from prometheus_client import Summary
import requests
import calendar
import dateutil.relativedelta
from datetime import date
app = Flask(__name__, static_folder='')

api_key="c7theeiad3i8dq4u3bng"

@app.route('/', methods=['GET'])

def home():
    return app.send_static_file('index.html')

@app.route('/test', methods=['GET'])
def test():
    global name
    global finnhub_client
    name=request.args.get('CPN')
    url1="https://finnhub.io/api/v1/stock/profile2?symbol={}&token={}".format(name, api_key)
    company=requests.get(url1)
    company=company.json()
    return company

@app.route('/route2', methods=['GET'])
def quote():
    url2="https://finnhub.io/api/v1/quote?symbol={}&token={}".format(name, api_key)
    data1=requests.get(url2)
    stock=data1.json()
    stock['t'] = time.strftime("%d %B, %Y",time.localtime(stock['t']))

    url3="https://finnhub.io/api/v1/stock/recommendation?symbol={}&token={}".format(name, api_key)
    data2=requests.get(url3)
    recommend=data2.json()

    if(len(recommend)==0):
         recommend1={'buy':'N.A.', 'hold': 'N.A.', 'period': 'N.A.', 'sell': 'N.A.', 'strongBuy': 'N.A.', 'strongSell': 'N.A.', 'symbol': name}
    else:
        recommend1=recommend[0]
    stock.update(recommend1)
    return stock

@app.route('/route3', methods=['GET'])
def graph():
    d2 = datetime.datetime.utcnow()
    d1 = d2 + dateutil.relativedelta.relativedelta(months=-6,days=-1)
    time1 = calendar.timegm(d1.utctimetuple())
    time2 = calendar.timegm(d2.utctimetuple())

    url4="https://finnhub.io/api/v1/stock/candle?symbol={}&resolution={}&from={}&to={}&token={}".format(name, 'D', time1,time2, api_key)
    data=requests.get(url4)
    candles=data.json()

    new_list=[]
    for i in range(len(candles['t'])):
        new_list.append([candles['t'][i]*1000,candles['c'][i], candles['v'][i]])
    return jsonify(new_list)

@app.route('/route4', methods=['GET'])
def news():
    today=date.today()
    day=datetime.timedelta(30)
    url5="https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token={}".format(name, day, today, api_key)
    data1=requests.get(url5)
    data=data1.json()
    
    j=0
    result={}

    for i in range(len(data)):
        if data[i]['image'] and data[i]['url'] and data[i]['headline'] and data[i]['datetime'] and j<len(data) and len(result)<5:
            data[i]['datetime'] = time.strftime("%d %B, %Y",time.localtime(data[i]['datetime']))
            result[j]=data[i]
            j=j+1
    return result




if __name__ == "__main__":
        app.run()
