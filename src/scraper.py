import requests
import time
from bs4 import BeautifulSoup
from config.settings import (
    LINKEDIN_SEARCH_URL,
    get_headers,
    get_proxy,
    log_info,
    log_error,
)
from config.cookies import get_cookies
from src.storage import save_to_database
from src.find_company_website import find_company_website  # 新增：查找公司官网

# 15 分钟轮换身份
IDENTITY_ROTATION_TIME = 900  # 900 秒 = 15 分钟


def scrape_linkedin():
    """爬取 LinkedIn 页面"""
    headers = get_headers()
    cookies = get_cookies()
    proxy = get_proxy()

    log_info(f"使用代理: {proxy if proxy else '直连模式'} 访问 {LINKEDIN_SEARCH_URL}")

    try:
        response = requests.get(
            LINKEDIN_SEARCH_URL,
            headers=headers,
            cookies=cookies,
            proxies={"http": proxy, "https": proxy} if proxy else None,
            timeout=10,
        )

        if response.status_code == 200:
            log_info("成功获取 LinkedIn 数据")
            return response.text
        else:
            log_error(f"请求失败，状态码: {response.status_code}")
            return None

    except requests.RequestException as e:
        log_error(f"请求异常: {e}")
        return None


def extract_data(html):
    """解析 HTML 并提取完整信息"""
    soup = BeautifulSoup(html, "html.parser")
    agents = []

    for profile in soup.select(".search-result__info"):
        name = (
            profile.select_one(".name").text.strip()
            if profile.select_one(".name")
            else "N/A"
        )
        company = (
            profile.select_one(".subline-level-1").text.strip()
            if profile.select_one(".subline-level-1")
            else "N/A"
        )
        location = (
            profile.select_one(".subline-level-2").text.strip()
            if profile.select_one(".subline-level-2")
            else "N/A"
        )
        phone = (
            profile.select_one(".phone").text.strip()
            if profile.select_one(".phone")
            else "N/A"
        )
        email = (
            profile.select_one(".email").text.strip()
            if profile.select_one(".email")
            else "N/A"
        )
        company_email = (
            profile.select_one(".company-email").text.strip()
            if profile.select_one(".company-email")
            else "N/A"
        )
        address = (
            profile.select_one(".address").text.strip()
            if profile.select_one(".address")
            else "N/A"
        )
        abn = (
            profile.select_one(".abn").text.strip()
            if profile.select_one(".abn")
            else "N/A"
        )

        # 通过公司名称 & 地址查找官网
        website = find_company_website(company, address, abn)
        extra_info = website if website else "N/A"

        agents.append(
            {
                "name": name,
                "company": company,
                "location": location,
                "phone": phone,
                "email": email,
                "company_email": company_email,
                "address": address,
                "abn": abn,
                "extra_info": extra_info,  # 添加官网
            }
        )

    log_info(f"提取到 {len(agents)} 条数据")
    return agents


def main():
    """主循环，定期爬取数据"""
    while True:
        html_content = scrape_linkedin()
        if html_content:
            data = extract_data(html_content)
            if data:
                save_to_database(data)
        time.sleep(IDENTITY_ROTATION_TIME)


if __name__ == "__main__":
    main()
