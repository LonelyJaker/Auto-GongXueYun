import datetime
import json
import time

import requests

import AES
from push import push

from log import MainLog


def SignRecord(SignRecordUser: dict, Ua: str) -> str:  # 用户信息 Ua
    time.sleep(5)
    logger = MainLog(SignRecordUser["name"])

    global res
    header: dict = {
        "accept-encoding": "gzip",
        "content-type": "application/json;charset=UTF-8",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": SignRecordUser["token"],
        "user-agent": Ua
    }
    data: dict = {
        # "startTime": "2022-08-20 00:00:00",
        # "endTime": "2023-03-20 00:00:00",
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000)))
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/attendence/clock/v1/listSynchro",
                            headers=header,
                            data=json.dumps(data)).json()

        if res['code'] == 200:
            if "token失效" == res['msg']:
                logger.info("token失效")
                return "token失效"
            elif res['data'] == [] or res['data'] is None or res['data'] == '':
                logger.info("没签过")
                return "没签过"
            elif str(datetime.date.today()) == res['data'][0]['dateYmd']:
                logger.info("不需要签到")
                return "不需要签到"
            else:
                logger.info("需要签到")
                return "需要签到"
        else:
            logger.error(f"签到记录获取失败：{res['msg']}")
            push(PushUser=SignRecordUser, CreateTime="请手动签到")
            return "获取失败"

    except:
        logger.error("签到记录请求失败")
        push(PushUser=SignRecordUser, CreateTime="请手动签到")
        return "请求失败"
