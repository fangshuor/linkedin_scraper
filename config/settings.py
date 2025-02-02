import logging
import os
from config.proxy import get_random_proxy  # 代理管理
from config.cookies import get_cookies  # Cookies 管理
from src.rotate_identity import get_identity  # 伪装身份

# =============================
# 🔹 LinkedIn 目标搜索 URL
# =============================
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

# =============================
# 🔹 代理开关（主程序通过 settings.py 读取）
# =============================
USE_PROXY = True  # 设置为 False 则不使用代理


# =============================
# 🔹 代理获取逻辑（主程序调用时使用）
# =============================
def get_proxy():
    """根据 USE_PROXY 开关决定是否返回代理"""
    return get_random_proxy() if USE_PROXY else None


# =============================
# 🔹 伪装身份（Headers 由 rotate_identity 处理）
# =============================
def get_headers():
    """直接从 rotate_identity 获取完整 Headers"""
    identity = get_identity()
    return identity["headers"]


# =============================
# 🔹 数据库配置
# =============================
DB_CONFIG = {
    "type": "mysql",  # "mysql" 或 "sqlite"
    "sqlite_path": "database.db",
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "password",
        "database": "linkedin_agents",
    },
}

# =============================
# 🔹 日志配置（方便调试）
# =============================
LOG_FILE = "logs/scraper.log"

if not os.path.exists("logs"):
    os.makedirs("logs")

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
