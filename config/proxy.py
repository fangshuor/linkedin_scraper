import random
import os
from config.logger import log_info, log_error  # ✅ 直接引入 logger 以避免循环导入

# 代理列表存储文件
PROXY_FILE = "/opt/linkedin_scraper/config/proxy.txt"

# 代理列表（从 proxy.txt 读取）
proxies = []


# 读取代理文件
def load_proxies():
    """从 proxy.txt 读取代理列表"""
    global proxies
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        log_info(f"已加载 {len(proxies)} 个代理")


load_proxies()  # 启动时加载


# 获取随机代理
def get_random_proxy():
    """返回一个随机代理"""
    if proxies:
        return random.choice(proxies)
    return None


# 代理开关（从 settings.py 控制）
USE_PROXY = True


# 代理获取逻辑
def get_proxy():
    """如果启用代理，则返回随机代理，否则返回 None"""
    return get_random_proxy() if USE_PROXY else None
