import random

# LinkedIn 目标 URL
LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/people/?keywords=real%20estate%20agent%20australia"

# 代理池（可自行添加更多代理）
PROXY_POOL = ["http://proxy1:port", "http://proxy2:port", "http://proxy3:port"]

# User-Agent 池（每 15 分钟自动更换）
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
]


# 选择一个随机代理
def get_random_proxy():
    return random.choice(PROXY_POOL)


# 选择一个随机 User-Agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)


# 数据库配置（MySQL 或 SQLite）
DB_CONFIG = {
    "type": "sqlite",  # "mysql" 或 "sqlite"
    "sqlite_path": "database.db",  # SQLite 文件路径
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "password",
        "database": "linkedin_agents",
    },
}
