import json
import time

import requests

from AES import Encrypt
from push import push
from log import MainLog


def GetTokenDef(GetTokenUser: dict, Ua: str) -> dict:  # 用户信息 UA
    time.sleep(5)
    logger = MainLog(GetTokenUser["name"])

    headers: dict = {
        "content-type": "application/json; charset=utf-8",
        "accept-encoding": "gzip",
        "content-length": "213",
        "host": "api.moguding.net:9000",
        "UserAgent": Ua
    }

    data: dict = {
        "phone": Encrypt("23DbtQHR2UMbH6mJ", GetTokenUser["phone"]),
        "password": Encrypt("23DbtQHR2UMbH6mJ", GetTokenUser["password"]),
        "captcha": "null",
        "loginType": "android",
        "uuid": "",
        "device": "android",
        "version": "5.5.0",
        "t": Encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
    }

    try:
        res = requests.post(url="https://api.moguding.net:9000/session/user/v3/login",
                            data=json.dumps(data),
                            headers=headers).json()

        if res['code'] == 200:
            logger.info("Token UserId获取成功")
            return {
                "token": res["data"]["token"],
                "userId": res["data"]["userId"]
            }
        else:
            logger.error(f"Token UserId获取失败{res['msg']}")
            push(PushUser=GetTokenUser, CreateTime="请手动签到")
    except:
        logger.error("Token请求失败")
        push(PushUser=GetTokenUser, CreateTime="请手动签到")
