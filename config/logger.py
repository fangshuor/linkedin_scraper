import logging
import os

# 日志文件路径
LOG_FILE = "/opt/linkedin_scraper/logs/scraper.log"

# 创建日志目录
if not os.path.exists("/opt/linkedin_scraper/logs"):
    os.makedirs("/opt/linkedin_scraper/logs")

# 配置日志
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_info(message):
    """记录 INFO 级别日志"""
    logging.info(message)
    print(f"[INFO] {message}")


def log_error(message):
    """记录 ERROR 级别日志"""
    logging.error(message)
    print(f"[ERROR] {message}")
