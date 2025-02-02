import random
import os

PROXY_FILE = "config/proxy.txt"
PROXY_LIST = []


def load_proxies():
    """从 proxy.txt 加载代理并缓存"""
    global PROXY_LIST
    if os.path.exists(PROXY_FILE):
        with open(PROXY_FILE, "r") as file:
            PROXY_LIST = [line.strip() for line in file.readlines() if line.strip()]
        print(f"[INFO] 已加载 {len(PROXY_LIST)} 个代理")
    else:
        print("[WARNING] 未找到 proxy.txt，默认使用直连模式")


def get_random_proxy():
    """从代理池随机选择一个代理，如果池为空则返回 None"""
    return random.choice(PROXY_LIST) if PROXY_LIST else None


# 启动时加载代理
load_proxies()
