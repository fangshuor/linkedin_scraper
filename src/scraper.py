import sys
import os

# 确保 Python 可以找到 config 目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import (
    LINKEDIN_SEARCH_URL,
    get_headers,
    get_active_proxy,
    log_info,
    log_error,
)
import requests
import time
from bs4 import BeautifulSoup
from src.storage import save_to_database


def scrape_linkedin():
    """爬取 LinkedIn 页面"""
    log_info("开始爬取 LinkedIn 页面...")

    headers = get_headers()
    proxy = get_active_proxy()

    response = requests.get(LINKEDIN_SEARCH_URL, headers=headers, proxies=proxy)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        log_info("成功解析 LinkedIn 页面")

        # 存储数据
        data = [
            {
                "name": "John Doe",
                "company": "Real Estate Group",
                "location": "Sydney, Australia",
                "phone": "N/A",
                "email": "N/A",
                "company_email": "N/A",
                "address": "123 Street, Sydney",
                "abn": "123456789",
                "company_website": "https://example.com",
            }
        ]
        save_to_database(data)
    else:
        log_error(f"请求失败，状态码: {response.status_code}")


if __name__ == "__main__":
    scrape_linkedin()
