import json
import time

import requests

from push import push
from md5 import Md5
import AES

from log import MainLog


def GetPlanId(GetPlanIdUser: dict, Ua: str) -> dict:  # 用户信息 Ua
    time.sleep(5)
    global res

    logger = MainLog(GetPlanIdUser["name"])
    data: dict = {
        # "pageSize": 999999,
        "t": AES.Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }
    headers: dict = {
        "userid": GetPlanIdUser['userId'],
        "accept-encoding": "gzip",
        "content-length": "58",
        "rolekey": "student",
        "host": "api.moguding.net:9000",
        "authorization": GetPlanIdUser['token'],
        "content-type": "application/json; charset=utf-8",
        "sign": Md5(f'{GetPlanIdUser["userId"]}student'),
        "UserAgent": Ua
    }
    try:
        res = requests.post(url="https://api.moguding.net:9000/practice/plan/v3/getPlanByStu", data=json.dumps(data),
                            headers=headers, ).json()
        if res["code"] == 200:
            logger.info("PlanId获取成功")
            return {
                'planId': res['data'][0]['planId']
            }
        else:
            logger.error(f"PlanId获取失败：{res['msg']}")
            push(PushUser=GetPlanIdUser, CreateTime="请手动签到")

    except:
        logger.error("PlanId请求失败")
        push(PushUser=GetPlanIdUser, CreateTime="请手动签到")
