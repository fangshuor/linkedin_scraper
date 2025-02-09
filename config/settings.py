import os
from config.proxy import get_proxy
from config.cookies import get_cookies
from config.logger import log_info, log_error
from src.rotate_identity import get_random_user_agent

# =============================
# 🔹 LinkedIn 目标搜索 URL
# =============================
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

# =============================
# 🔹 代理开关
# =============================
USE_PROXY = True  # ✅ 是否使用代理


# =============================
# 🔹 代理获取逻辑
# =============================
def get_active_proxy():
    """根据 USE_PROXY 开关决定是否返回代理"""
    return get_proxy() if USE_PROXY else None


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
