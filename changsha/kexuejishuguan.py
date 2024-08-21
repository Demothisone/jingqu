





import requests
import os
from SendNotify import send
def changshabowuguan():
    url = 'http://pw.hnstm.org.cn/api/cinema/index/get_cinema_commodity_id?make_time=2024%2F08%2F18&site_id=9'
    filtered_dates = []
    heard = {

        'Cookie': 'PHPSESSID=3or8adpplmjdf9qjjt9laf3ncp; TS016716af=019569966b01a7393b751c784e67f0cf91714484bbad746117d6d9a34b9f4e4c855e7be39bb47178e3ef1a449b741b2a1fc690b477',


    }
    response = requests.get(url, headers=heard).json()
    print(response)

if __name__ == '__main__':
    changshabowuguan()