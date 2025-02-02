import os
import json

# =============================
# 🔹 LinkedIn Cookies 管理
# =============================
COOKIES_FILE = "config/cookies.json"


def load_cookies():
    """从 cookies.json 读取 LinkedIn 登录 Cookies"""
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, "r") as file:
            return json.load(file)
    print("[WARNING] 未找到 cookies.json，可能无法正常爬取数据")
    return {}


def get_cookies():
    """获取当前 LinkedIn Cookies"""
    return load_cookies()
