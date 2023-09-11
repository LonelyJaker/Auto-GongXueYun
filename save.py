import datetime
import json
import time

import requests
from push import push
from log import MainLog
from md5 import Md5
import mysql
import AES


def Writ(WritUser: dict, SaveTime: str) -> None:
    Sql = f"""UPDATE users 
        SET 
        save_time = '{SaveTime}',
        WHERE 
        name = '{WritUser["name"]}';"""
    mysql.Update(Sql=Sql, Name=WritUser["name"])


def Save(SaveUser: dict, Ua: str):
    logger = MainLog(SaveUser["name"])

    time.sleep(5)
    global res

    headers: dict = {
        'roleKey': 'student',
        "user-agent": Ua,
        "sign": Md5(text='Android' + 'START' + SaveUser['planId'] + SaveUser['userId'] + SaveUser['address']),
        "authorization": SaveUser["token"],
        "content-type": "application/json; charset=UTF-8",
        "userid": SaveUser['userId']
    }
    data: dict = {
        # 国家
        "country": SaveUser["country"],
        # 详细地址
        "address": SaveUser["address"],
        # 省
        "province": SaveUser["province"],
        # 市
        "city": SaveUser["city"],
        # 县
        "area": SaveUser["area"],
        # 经纬度
        "latitude": SaveUser['latitude'],
        "longitude": SaveUser['longitude'],
        # 打卡备注
        "description": SaveUser["note"],
        "planId": SaveUser['planId'],
        # 签到时间标识 上午或下午 START是上班，END是下班
        "type": 'START',
        # 设备标识
        "device": 'Android',

        "distance": None,
        "content": None,
        "lastAddress": None,
        "lastDetailAddress": SaveUser["address"],
        "attendanceId": None,
        "createBy": None,
        "createTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "images": None,
        "isDeleted": None,
        "isReplace": None,
        "modifiedBy": None,
        "modifiedTime": None,
        "schoolId": None,
        "state": "NORMAL",
        "teacherId": None,
        "stuId": None,
        "attendanceType": None,
        "username": None,
        "attachments": None,
        "userId": SaveUser["userId"],
        "isSYN": None,
        "studentId": None,
        "applyState": None,
        "studentNumber": None,
        "headImg": None,
        "attendenceTime": None,
        "depName": None,
        "majorName": None,
        "className": None,
        "logDtoList": None,
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save",
                            headers=headers,
                            data=json.dumps(data)).json()
        if res['code'] == 200:
            logger.info("签到成功")
            Writ(WritUser=SaveUser, SaveTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            push(PushUser=SaveUser, CreateTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), SaveCode=200)
            return "签到成功"
        else:
            logger.error("签到失败")
            push(PushUser=SaveUser, CreateTime="请手动签到")
            return "签到失败"
    except:
        logger.error("请求失败")
        push(PushUser=SaveUser, CreateTime="请手动签到")
        return "请求失败"
