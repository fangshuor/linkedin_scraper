import random
import time
from config.logger import log_info  # ✅ 现在从 logger.py 引入日志
from config.proxy import get_proxy  # ✅ 代理管理

# =============================
# 🔹 模拟不同的设备 & 浏览器环境
# =============================

# 操作系统类型
OS_TYPES = [
    "Windows NT 10.0; Win64; x64",
    "Macintosh; Intel Mac OS X 10_15_7",
    "Macintosh; Intel Mac OS X 11_6",
    "X11; Linux x86_64",
    "X11; Ubuntu; Linux x86_64",
    "X11; Fedora; Linux x86_64",
]

# 浏览器内核 & 版本
BROWSER_ENGINES = [
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "AppleWebKit/537.51.1 (KHTML, like Gecko)",
    "AppleWebKit/604.1.38 (KHTML, like Gecko)",
]

# 浏览器类型（不同版本的 Chrome、Firefox、Edge、Safari）
BROWSERS = [
    "Chrome/112.0.0.0 Safari/537.36",
    "Chrome/110.0.0.0 Safari/537.36",
    "Firefox/113.0",
    "Firefox/110.0",
    "Edge/114.0.1823.37 Safari/537.36",
    "Safari/604.1.38",
]

# 语言设置（不同地区）
LANGUAGES = [
    "en-US,en;q=0.9",
    "en-GB,en;q=0.9",
    "fr-FR,fr;q=0.8,en;q=0.6",
    "de-DE,de;q=0.8,en-US;q=0.6,en;q=0.4",
]

# 屏幕分辨率（模拟不同设备）
SCREEN_RESOLUTIONS = ["1920x1080", "1366x768", "1536x864", "1440x900", "1280x720"]

# 浏览器插件（随机模拟安装了一些插件）
PLUGINS = [
    "PDF Viewer; Chrome PDF Viewer; Native Client",
    "Widevine Content Decryption Module; Chrome PDF Viewer",
    "Google Hangouts Plugin; Native Client",
    "WebRTC Plugin; Adobe Flash",
]

# 是否开启 `Do Not Track`
DNT_OPTIONS = ["1", "0"]

# 设备类型（桌面 / 移动）
DEVICE_TYPES = ["desktop", "mobile"]

# WebGL 伪装（显卡模拟）
WEBGL_RENDERERS = [
    "Intel(R) UHD Graphics 620",
    "NVIDIA GeForce GTX 1050",
    "AMD Radeon RX 580",
    "Intel(R) Iris Plus Graphics 640",
    "Apple M1 GPU",
]

# =============================
# 🔹 生成伪装身份
# =============================


def get_random_user_agent():
    """生成真实的 User-Agent"""
    os_type = random.choice(OS_TYPES)
    browser_engine = random.choice(BROWSER_ENGINES)
    browser = random.choice(BROWSERS)
    user_agent = f"Mozilla/5.0 ({os_type}) {browser_engine} {browser}"
    return user_agent


def get_random_headers():
    """生成真实的 HTTP Headers"""
    return {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": random.choice(LANGUAGES),
        "DNT": random.choice(DNT_OPTIONS),  # `Do Not Track` 选项
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
    }


def get_browser_fingerprint():
    """生成浏览器指纹信息"""
    return {
        "screen_resolution": random.choice(SCREEN_RESOLUTIONS),
        "plugins": random.choice(PLUGINS),
        "webgl_renderer": random.choice(WEBGL_RENDERERS),
        "device_type": random.choice(DEVICE_TYPES),
    }


def get_identity():
    """生成完整的身份信息，包括 User-Agent、代理、Cookies、浏览器指纹"""
    user_agent = get_random_user_agent()
    proxy = get_proxy()
    headers = get_random_headers()
    fingerprint = get_browser_fingerprint()

    log_info(f"当前身份: User-Agent={user_agent}, Proxy={proxy}, 指纹={fingerprint}")

    return {
        "headers": headers,
        "proxy": {"http": proxy, "https": proxy} if proxy else None,
        "fingerprint": fingerprint,
    }


def simulate_user_behavior():
    """模拟真实用户的访问间隔"""
    sleep_time = random.uniform(15, 45)  # 访问间隔模拟
    log_info(f"等待 {sleep_time:.2f} 秒后进行下一次请求")
    time.sleep(sleep_time)
