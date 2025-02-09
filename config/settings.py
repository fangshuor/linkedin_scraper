import os
from config.proxy import get_proxy  # ✅ 代理管理
from config.cookies import get_cookies  # ✅ Cookies 统一管理
from config.logger import log_info, log_error  # ✅ 日志从 logger.py 统一引入
from src.rotate_identity import get_random_user_agent  # ✅ 伪装身份

# =============================
# 🔹 LinkedIn 目标搜索 URL
# =============================
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

# =============================
# 🔹 代理开关（从 proxy.py 读取）
# =============================
USE_PROXY = True  # ✅ 全局代理开关


# =============================
# 🔹 代理获取逻辑（scraper.py 可直接调用）
# =============================
def get_proxy():
    """代理获取逻辑：如果启用，则返回代理，否则 None"""
    return get_proxy() if USE_PROXY else None


# =============================
# 🔹 伪装身份（Headers 由 rotate_identity 处理）
# =============================
def get_headers():
    """生成随机 Headers（User-Agent + 语言）"""
    return {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }


# =============================
# 🔹 数据库配置（MySQL / SQLite 自动适配）
# =============================
DB_CONFIG = {
    "type": "mysql",  # "mysql" 或 "sqlite"
    "sqlite_path": "/opt/linkedin_scraper/database.db",
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "linkedin_scraper_pass",
        "database": "linkedin_scraper",
    },
}
