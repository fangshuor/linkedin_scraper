import random
import time
from config.logger import log_info
from config.proxy import get_proxy

# =============================
# 🔹 生成随机 User-Agent
# =============================

OS_TYPES = [
    "Windows NT 10.0; Win64; x64",
    "Macintosh; Intel Mac OS X 10_15_7",
    "X11; Linux x86_64",
]

BROWSER_ENGINES = [
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "AppleWebKit/604.1.38 (KHTML, like Gecko)",
]

BROWSERS = ["Chrome/112.0.0.0 Safari/537.36", "Firefox/113.0", "Safari/604.1.38"]


def get_random_user_agent():
    """生成真实的 User-Agent"""
    os_type = random.choice(OS_TYPES)
    browser_engine = random.choice(BROWSER_ENGINES)
    browser = random.choice(BROWSERS)
    return f"Mozilla/5.0 ({os_type}) {browser_engine} {browser}"


def get_identity():
    """生成完整的身份信息（User-Agent、代理）"""
    user_agent = get_random_user_agent()
    proxy = get_proxy()

    log_info(f"当前身份: User-Agent={user_agent}, Proxy={proxy}")

    return {
        "headers": {"User-Agent": user_agent},
        "proxy": {"http": proxy, "https": proxy} if proxy else None,
    }
