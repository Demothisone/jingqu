"""
@demo出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
const $ = new Env("湖南博物馆和马王堆汗墓墓坑遗址");
export changshabowuguan=Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbl91c2VyX2.......
cron：52 0,6-22/2 * * *
"""

import requests
from SendNotify import send
def changshabowuguan(url,cookie):
    filtered_dates = []
    heard = {
        'Authorization': cookie,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'wapticket.hnmuseum.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'xweb_xhr': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8391',
        'x-fc-source': 'wx',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'

    }
    response = requests.get(url, headers=heard).json()

    if response['msg'] != '操作成功':
        return response['msg']
    else:

        data = response['data']['calendarTicketPoolsByDate']
        # print(response)
        from datetime import datetime
        for entry in data:
            t_date = entry['currentDate']  # 获取日期
            tp_last_stock_sum = entry['status']  # 获取状态
            tp_last_stock_sum_fee = entry['ticketPool']  # 获取余票
            # print(t_date,tp_last_stock_sum,tp_last_stock_sum_fee)
            # 将日期字符串转换为日期对象
            date_obj = datetime.strptime(t_date, '%Y-%m-%d')

            # 判断日期是否大于10月1日，并且tp_last_stock_sum或tp_last_stock_sum_fee大于0
            # if date_obj > datetime(date_obj.year, 10, 1) and tp_last_stock_sum_fee > 0 :
            if tp_last_stock_sum_fee > 0 :
                # print(t_date)  # 打印日期
                filtered_dates.append(t_date)
        return filtered_dates
if __name__ == '__main__':
    cook = os.getenv("changshabowuguan")
    url_hunan = 'https://wapticket.hnmuseum.com/prod-api/basesetting/HallSetting/gainAllSystemConfigLogin?channel=wxMini&venueId=1&hallType=91&requestTaskKey=gainAllSystemConfigLogin&ticketUseType=1&p=wxmini'
    url_mawang = 'https://wapticket.hnmuseum.com/prod-api/basesetting/HallSetting/gainAllSystemConfigLogin?channel=wxMini&venueId=2&hallType=91&requestTaskKey=gainAllSystemConfigLogin&ticketUseType=1&p=wxmini'
    hunan_museum_dates = changshabowuguan(url_hunan, cook)
    mawangdui_dates = changshabowuguan(url_mawang, cook)
    if  hunan_museum_dates or mawangdui_dates:
        send("湖南博物馆有票了","湖南博物馆："+str(hunan_museum_dates)+"马王堆汗墓墓坑遗址："+str(mawangdui_dates))