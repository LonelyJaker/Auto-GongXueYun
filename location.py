import random

import requests

import mysql

from log import MainLog

# 写入定位
def Writ(Name: str, Lon: str, Lat: str) -> None:
    Sql = f"""UPDATE users
    SET
    longitude = "{Lon}",
    latitude = "{Lat}"
    WHERE
    name = '{Name}';"""
    mysql.Update(Sql=Sql, Name=Name)


# 修改定位
def ModifyPositioning(PositionUser) -> dict:  # 用户信息 定位路径
    logger = MainLog(PositionUser["name"])
    logger.info("修改定位")
    if PositionUser["latitude"] == '':
        logger.info("获取定位")
        lng, lat = Req(Name=PositionUser['name'],
                       Lat=PositionUser["latitude"],
                       Lon=PositionUser["longitude"],
        Address=PositionUser["address"])
        PositionUser["longitude"] = lng
    latitude: str = str(PositionUser["latitude"])
    longitude: str = str(PositionUser["longitude"])
    PositionUser["latitude"] = latitude[0:len(latitude) - 1] + str(random.randint(0, 10))
    PositionUser["longitude"] = longitude[0:len(longitude) - 1] + str(random.randint(0, 10))

    return PositionUser


# 获取定位
def Req(Name: str, Lon: str, Lat: str, Address: str) -> tuple:  # 详细地址
    url = f'https://apis.map.qq.com/ws/geocoder/v1/?address={Address}&key=XN6BZ-6YYEX-2OE4C-ZTGOK-EAQRV-IZBZG'
    heasers = {
        'sec-ch-ua-platform': 'Windows',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46'
    }
    res = requests.get(url=url, headers=heasers, ).json()
    lng = res['result']['location']['lng']
    lat = res['result']['location']['lat']
    # 经度
    if len(str(lng).split('.')[1]) < 6:
        lng = f"{str(lng).split('.')[0]}.{str(lng).split('.')[1]}{'0' * int(6 - len(str(lng).split('.')[1]))}"
    elif len(str(lng).split('.')[1]) > 6:
        lng = f"{str(lng).split('.')[0]}.{str(lng).split('.')[1][:6]}"
    # 维度
    if len(str(lat).split('.')[1]) < 6:
        lat = f"{str(lat).split('.')[0]}.{str(lat).split('.')[1]}{'0' * int(6 - len(str(lat).split('.')[1]))}"
    elif len(str(lat).split('.')[1]) > 6:
        lat = f"{str(lat).split('.')[0]}.{str(lat).split('.')[1][:6]}"

    Writ(Name=Name, Lon=Lon, Lat=Lat)

    return lng, lat


