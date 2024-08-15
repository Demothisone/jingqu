"""
@demo出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
const $ = new Env("橘子洲头");
export juzizhoutou=20240814,20240815,20240816
export juzizhoutou=20240814
cron：52 0,6-22/2 * * *
"""

import requests
from datetime import datetime
import os
# 获取当前日期
current_date = datetime.now()

# 转换为指定格式的字符串 (格式为 YYYYMMDD)
formatted_date = int(current_date.strftime('%Y%m%d'))
from SendNotify import send
def juzizhoutou(data):
    filtered_dates = []
    url = f'https://yuelu-api.hnliantong.com/api?act=getOrderStock&scenic_id=2&book_day={data}'
    heard = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Accept': 'application/json',
        'xweb_xhr': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8391',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty'
    }
    response = requests.post(url, headers=heard).json()
    if response['errcode'] != 0:
        return response['errcode']
    else:
        data = response['data']
        # 原始返回的数据

        # 定义映射关系
        time_mapping = {'t1': '07:00~12:00', 't2': '12:00~17:00', 't3': '17:00~22:00'}
        mapped_data = {time_mapping.get(key, key): value for key, value in data.items()}
        for entry in mapped_data:
            if mapped_data[entry] > 0:
                filtered_dates.append(entry)
        return filtered_dates
if __name__ == '__main__':
    datajuzi = os.getenv("juzizhoutou")
    date_list = datajuzi.split(',')
# 如果需要将每个元素转换为整数，可以使用列表推导式
    data = [int(date) for date in date_list]
    daone = []
    # 遍历日期列表
    for d in data:
        if d in (formatted_date,int(formatted_date)+1,int(formatted_date)+2):
            if juzizhoutou(d)!=[]:
                a=str(d)+str(juzizhoutou(d))
                daone.append(a)
        else:
            daone.append(f"{d}不在查询范围")
    if daone !=[]:
        send("橘子洲头有票了",str(daone))
