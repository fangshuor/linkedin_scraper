import requests
import time
import random
from bs4 import BeautifulSoup
from config.settings import get_random_proxy, get_random_user_agent
from src.storage import save_to_database


# 伪装身份（15分钟更换一次）
def get_headers():
    return {"User-Agent": get_random_user_agent(), "Accept-Language": "en-US,en;q=0.5"}


# 爬取 LinkedIn 页面
def scrape_linkedin():
    proxy = get_random_proxy()
    headers = get_headers()
    url = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

    print(f"使用代理 {proxy} 访问 {url}")

    response = requests.get(
        url, headers=headers, proxies={"http": proxy, "https": proxy}
    )

    if response.status_code == 200:
        return response.text
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


# 解析 HTML 并提取信息
def extract_data(html):
    soup = BeautifulSoup(html, "html.parser")
    agents = []

    for profile in soup.select(".search-result__info"):
        name = profile.select_one(".name").text.strip()
        company = profile.select_one(".subline-level-1").text.strip()
        location = profile.select_one(".subline-level-2").text.strip()

        agents.append({"name": name, "company": company, "location": location})

    return agents


if __name__ == "__main__":
    while True:
        html_content = scrape_linkedin()
        if html_content:
            data = extract_data(html_content)
            save_to_database(data)
        time.sleep(900)  # 每 15 分钟爬取一次
