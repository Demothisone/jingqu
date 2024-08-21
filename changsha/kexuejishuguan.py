"""
@demo出品 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
name "A馆（0.8米以上需购票）", "B馆（0.8米以上需购票）", "3D:熊猫传奇（中科馆巡映影片）", "飞越探奇（建议5岁以上观看）", "你好小蜜蜂（建议5岁以上观看）", "诸葛亮（建议5岁以上观看）"
const $ = new Env("湖南科学技术馆");
export hnkexuejishiguan="cookie&{'日期':['场馆名称1','场馆名称2'],'2024/08/24':['A馆（0.8米以上需购票）']}"
export hnkexuejishiguan="PHPSESSID=j。。; TS016716af=。。。&{'2024/08/21':['B馆（0.8米以上需购票）','A馆（0.8米以上需购票）'],'2024/08/24':['A馆（0.8米以上需购票）']}"
cron：52 0,6-22/2 * * *
"""





import requests
import os
from SendNotify import send
from datetime import datetime,timedelta

def changshabowuguan(timedata,cookie,name):
    url = f'http://pw.hnstm.org.cn/api/cinema/index/get_cinema_commodity_id?make_time={timedata}&site_id=9'
    heard = {'Cookie': cookie}
    # heard = {'Cookie': "PHPSESSID=jh5duepdn28gb7voje3kg44m6j; TS016716af=019569966b8919861f55c8fcffd0f3c0997fd5781f4bd284199d5e33ce6608f0b07ab37ff6c3dd6a1c5712cb9b810c08b9f146590d"}
    try:
        response = requests.get(url, headers=heard).json()
        if response["msg"] == '获取成功':
            data = response["data"]["list"]
            for i in data:
                if i["commodity_name"]==name:
                    num=int(i["cinema"][0]["cinema_field_set"][0]["cinema_make_time_set"][0]["max_num"])
                    if num>0:
                        return timedata+":"+name+"有"+str(num)+"张票"
                    return num

        else:
            return f"token错误或者{timedata}闭馆了"

    except Exception as e:
        print(e)
        return "获取失败请联系作者"
def fengzhuang(dataout):
    daone = []
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y/%m/%d')

    # 获取未来两天的日期
    next_day = (current_date + timedelta(days=1)).strftime('%Y/%m/%d')
    day_after_next = (current_date + timedelta(days=2)).strftime('%Y/%m/%d')
    try:
    # 找到逗号的位置并切割字符串
        split_data = dataout.split('&', 1)  # 只分割一次，得到两部分
        cookie = split_data[0]
        reservation_info_str = split_data[1]

        # 将预约信息字符串转换为Python字典
        import ast
        reservation_info = ast.literal_eval(reservation_info_str)


        # 使用 for 循环遍历字典中的键值对
        for timedata, name_list in reservation_info.items():
            if timedata in [formatted_date, next_day, day_after_next]:
                for name in name_list:
                    if name in ["A馆（0.8米以上需购票）", "B馆（0.8米以上需购票）", "3D:熊猫传奇（中科馆巡映影片）", "飞越探奇（建议5岁以上观看）", "你好小蜜蜂（建议5岁以上观看）", "诸葛亮（建议5岁以上观看）"]:
                        result = changshabowuguan(timedata=timedata, cookie=cookie, name=name)
                        if result!=0:
                            daone.append(result)
                    else:
                        daone.append(name+"场馆名称错误请检查")
            else:
                daone.append(timedata+"日期不在近三天范围内")
        return daone

    except Exception as e:
        print(f"解析出错: {e}")

if __name__ == '__main__':
    dataout = os.getenv("hnkexuejishiguan")
    v=fengzhuang(dataout)
    if v !=[]:
        send("湖南科学技术馆有票了",str(v))




