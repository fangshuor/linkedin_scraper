import os
from config.proxy import get_random_proxy  # 代理管理
from config.cookies import get_cookies  # Cookies 管理
from config.logger import log_info, log_error  # ✅ 现在从 logger.py 引入日志
from src.rotate_identity import get_random_user_agent  # 伪装身份

# =============================
# 🔹 LinkedIn 目标搜索 URL
# =============================
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

# =============================
# 🔹 代理开关（主程序通过 settings.py 读取）
# =============================
USE_PROXY = True  # 设置为 False 则不使用代理


# =============================
# 🔹 伪装身份 Headers
# =============================
def get_headers():
    """生成随机 Headers（User-Agent + 语言）"""
    return {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }


# =============================
# 🔹 代理获取逻辑
# =============================
def get_proxy():
    """根据 USE_PROXY 开关决定是否返回代理"""
    return get_random_proxy() if USE_PROXY else None


# =============================
# 🔹 数据库配置
# =============================
DB_CONFIG = {
    "type": "mysql",
    "sqlite_path": "/opt/linkedin_scraper/database.db",
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "linkedin_scraper_pass",
        "database": "linkedin_scraper",
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
