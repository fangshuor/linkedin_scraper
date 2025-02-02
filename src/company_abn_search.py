import requests
from bs4 import BeautifulSoup
import time
from config.settings import log_info, log_error
from src.storage import save_company_details

# ABN 搜索 URL 模板
ABN_SEARCH_URL = "https://abr.business.gov.au/ABN/View?abn={}"


def scrape_abn_details(abn):
    """访问 ABR 网站并提取 ABN 相关信息"""
    if not abn or abn == "N/A":
        return None

    url = ABN_SEARCH_URL.format(abn)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            log_error(f"无法访问 ABN 页面，状态码: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 解析 ABN 详情
        entity_name = (
            soup.find(text="Entity name:").find_next().text.strip()
            if soup.find(text="Entity name:")
            else "N/A"
        )
        abn_status = (
            soup.find(text="ABN status:").find_next().text.strip()
            if soup.find(text="ABN status:")
            else "N/A"
        )
        entity_type = (
            soup.find(text="Entity type:").find_next().text.strip()
            if soup.find(text="Entity type:")
            else "N/A"
        )
        gst_status = (
            soup.find(text="Goods & Services Tax (GST):").find_next().text.strip()
            if soup.find(text="Goods & Services Tax (GST):")
            else "N/A"
        )
        main_location = (
            soup.find(text="Main business location:").find_next().text.strip()
            if soup.find(text="Main business location:")
            else "N/A"
        )

        # 解析 Business Names
        business_names = []
        if soup.find(text="Business name(s) help"):
            business_table = soup.find(text="Business name(s) help").find_next("table")
            if business_table:
                for row in business_table.find_all("tr")[1:]:  # 跳过表头
                    cols = row.find_all("td")
                    if len(cols) >= 1:
                        business_names.append(cols[0].text.strip())

        # 解析 Trading Names
        trading_names = []
        if soup.find(text="Trading name(s) help"):
            trading_table = soup.find(text="Trading name(s) help").find_next("table")
            if trading_table:
                for row in trading_table.find_all("tr")[1:]:  # 跳过表头
                    cols = row.find_all("td")
                    if len(cols) >= 1:
                        trading_names.append(cols[0].text.strip())

        company_details = {
            "abn": abn,
            "entity_name": entity_name,
            "abn_status": abn_status,
            "entity_type": entity_type,
            "gst_status": gst_status,
            "main_location": main_location,
            "business_names": ", ".join(business_names) if business_names else "N/A",
            "trading_names": ", ".join(trading_names) if trading_names else "N/A",
        }

        log_info(f"成功获取 ABN {abn} 详情: {entity_name}")
        return company_details

    except requests.RequestException as e:
        log_error(f"ABN 查询失败: {e}")
        return None


def update_company_info(abn):
    """通过 ABN 查询公司信息并存入数据库"""
    details = scrape_abn_details(abn)
    if details:
        save_company_details(details)
