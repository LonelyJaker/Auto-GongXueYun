import datetime
import logging


def MainLog(LoggerName: str):
    # 配置日志记录器
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=f"./logs/{datetime.date.today()}.log",
        filemode='a',
        encoding='utf-8',
    )

    return logging.getLogger(LoggerName)
