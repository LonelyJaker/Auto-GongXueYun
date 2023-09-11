import datetime
import json

import requests

from log import MainLog


def push(PushUser: dict, CreateTime: str, SaveCode=None) -> str:  # 用户信息 签到时间 签到标识=None
    logger = MainLog(PushUser["name"])
    global res
    print("    推送", end="    ")
    code = "失败"
    a = ''
    now = datetime.datetime.now()
    if SaveCode == 200:
        code = '成功'
    if (now.weekday() + 1) == 7 or (now.weekday() + 1) == 6:
        a = f'今天星期{now.weekday() + 1}，有周报'
    if (now.day == 30) or (now.day == 31):
        a += f'今天是{now.day}，有月报'
    data = {
        'channel': "wechat",
        'content': f"""
|签到情况|
| :-: |
|{code} {CreateTime}|
|{PushUser["name"]} {PushUser["phone"]}|
|{PushUser["address"]}|
|{a}|
|联系方式:没想好|
|毕竟不是正常签到，难免会出现问题|
|不确定，可以登录看看|
""",
        'template': "markdown",
        'title': f"{PushUser['name']}  {code}签到情况",
        'token': f"{PushUser['pushKey']}",
    }
    try:
        res = requests.post(url='https://www.pushplus.plus/api/send', data=json.dumps(data)).json()
    except:
        pass

    if res['code'] == 200:
        logger.info("推送成功")
        return '200'
    else:
        logger.error(f"推送失败：{res['msg']}")
        return res['msg']
