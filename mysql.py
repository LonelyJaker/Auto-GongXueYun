import pymysql.cursors
from log import MainLog


def GetConn():
    return pymysql.connect(
        host='',
        user="",
        password="",
        database="",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor  # 设置游标以返回字典格式数据
    )


def QueryData() -> tuple:
    conn = GetConn()
    try:
        cur = conn.cursor()
        sql = """SELECT
        name,
        phone,
        password,
        token,
        userId,
        planid,
        country,
        province,
        city,
        area,
        address,
        longitude,
        latitude,
        note,
        type,
        pushKey
        FROM users
        WHERE enable = 'true';"""

        cur.execute(sql)

        return cur.fetchall()
    finally:
        conn.close()


def Update(Sql: str, Name: str) -> None:
    logger = MainLog(Name)
    conn = GetConn()
    try:
        cur = conn.cursor()
        cur.execute(Sql)
        conn.commit()
        logger.info("修改成功")
    except pymysql.Error as e:
        logger.warning(f"修改失败：{e}")
    finally:
        conn.close()
