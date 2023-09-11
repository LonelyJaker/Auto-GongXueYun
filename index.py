import datetime

from log import MainLog

import mysql
from UA import GetUserAgent
from getToken import GetTokenDef
from location import ModifyPositioning
from planId import GetPlanId
from save import Save
from signrecord import SignRecord


# 写入用户信息
def Writ(WritUser: dict) -> None:
    logger.info("写入Token UserId PlanId")
    Sql = f"""UPDATE users 
    SET 
    token = "{WritUser['token']}",
    userId = "{WritUser['userId']}",
    planId = "{WritUser['planId']}" 
    WHERE 
    name = "{WritUser["name"]}";"""
    mysql.Update(Sql=Sql, Name=WritUser["name"])


# 获取token userid planid
def GetTokenUser(GetToken: dict) -> str:
    print("Token")
    Token_UserId_Information: dict = GetTokenDef(GetTokenUser=GetToken, Ua=UA)
    # 判断是否获取到 Token UserId
    if "token" in Token_UserId_Information and "userId" in Token_UserId_Information:
        GetToken['token'] = Token_UserId_Information['token']
        GetToken['userId'] = Token_UserId_Information['userId']
    else:
        logger.warning("结束签到")
        return "结束"

    PlanIdInformation: dict = GetPlanId(GetPlanIdUser=GetToken, Ua=UA)
    print("PlanId")
    # 判断是否获取到PlanId
    if "planId" in PlanIdInformation:
        GetToken['planId'] = PlanIdInformation['planId']
    else:
        logger.warning("结束签到")
        return "结束"

    # 执行更新
    Writ(WritUser=GetToken)

    return "签到"


# 判断是否需要签到并执行
def Sing(SingUser: dict, ) -> str:
    print("Sign")
    SignInformation: str = SignRecord(SignRecordUser=SingUser, Ua=UA)
    if "token失效" == SignInformation:
        GetTokenUser(GetToken=SingUser)

    elif "不需要签到" == SignInformation or "请求失败" == SignInformation or "获取失败" == SignInformation:
        logger.warning("结束签到")
        return "结束"

    elif "没签过" == SignInformation or "需要签到" == SignInformation:
        return "签到"


def IsSave(IsSaveUser):
    print("Save")
    Positioninguser = ModifyPositioning(PositionUser=IsSaveUser)
    print("定位")
    Save(SaveUser=Positioninguser, Ua=UA)


if __name__ == '__main__':

    global UA, user
    # 循环用户列表
    for user in mysql.QueryData():
        UA: str = GetUserAgent()
        logger = MainLog(user["name"])
        print(user["name"])
        logger.info('-' * 30)

        if len(user['token']) != 306:
            logger.warning("没有Token")
            SignToken: str = GetTokenUser(GetToken=user)
            if SignToken == "签到":
                SignSing = Sing(SingUser=user)
                if SignSing == "签到":
                    IsSave(IsSaveUser=user)
                else:
                    break
            else:
                break
        else:
            logger.info("存在Token")
            SignSing = Sing(SingUser=user)
            if SignSing == "签到":
                IsSave(IsSaveUser=user)
            else:
                break