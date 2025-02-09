import sqlite3
import pymysql
import os
from config.settings import log_info, log_error

# =============================
# 🔹 自动检测数据库配置
# =============================

DB_CONFIG = {
    "type": "mysql",  # 默认使用 MySQL
    "sqlite_path": "/opt/linkedin_scraper/database.db",  # SQLite 备选
    "mysql": {
        "host": "localhost",
        "user": "root",
        "password": "linkedin_scraper_pass",
        "database": "linkedin_scraper",
    },
}


# 检查 MySQL 是否可用
def check_mysql():
    try:
        conn = pymysql.connect(
            host=DB_CONFIG["mysql"]["host"],
            user=DB_CONFIG["mysql"]["user"],
            password=DB_CONFIG["mysql"]["password"],
        )
        conn.close()
        return True
    except pymysql.MySQLError:
        return False


# 如果 MySQL 不可用，切换到 SQLite
if not check_mysql():
    log_error("MySQL 不可用，切换到 SQLite")
    DB_CONFIG["type"] = "sqlite"

# =============================
# 🔹 数据库连接
# =============================


def connect_db():
    """连接数据库"""
    if DB_CONFIG["type"] == "mysql":
        try:
            conn = pymysql.connect(
                host=DB_CONFIG["mysql"]["host"],
                user=DB_CONFIG["mysql"]["user"],
                password=DB_CONFIG["mysql"]["password"],
                database=DB_CONFIG["mysql"]["database"],
                charset="utf8mb4",
            )
            log_info("成功连接 MySQL")
            return conn
        except pymysql.MySQLError as e:
            log_error(f"MySQL 连接失败: {e}")
            return None
    else:
        try:
            conn = sqlite3.connect(DB_CONFIG["sqlite_path"])
            log_info("成功连接 SQLite")
            return conn
        except sqlite3.Error as e:
            log_error(f"SQLite 连接失败: {e}")
            return None


# =============================
# 🔹 创建数据库表
# =============================


def create_tables():
    """创建数据表（如果不存在）"""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    # `agents` 表（LinkedIn 爬取数据）
    create_agents_table = (
        """
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        company VARCHAR(100),
        location VARCHAR(100),
        phone VARCHAR(100),
        email VARCHAR(100),
        company_email VARCHAR(100),
        address VARCHAR(100),
        abn VARCHAR(100),
        company_website VARCHAR(100)
    );
    """
        if DB_CONFIG["type"] == "mysql"
        else """
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT(100),
        company TEXT(100),
        location TEXT(100),
        phone TEXT(100),
        email TEXT(100),
        company_email TEXT(100),
        address TEXT(100),
        abn TEXT(100),
        company_website TEXT(100)
    );
    """
    )

    # `company_details` 表（ABN 查询结果）
    create_company_table = (
        """
    CREATE TABLE IF NOT EXISTS company_details (
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        abn VARCHAR(100) UNIQUE,
        entity_name VARCHAR(100),
        abn_status VARCHAR(100),
        entity_type VARCHAR(100),
        gst_status VARCHAR(100),
        main_location VARCHAR(100),
        business_names VARCHAR(255),
        trading_names VARCHAR(255)
    );
    """
        if DB_CONFIG["type"] == "mysql"
        else """
    CREATE TABLE IF NOT EXISTS company_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        abn TEXT(100) UNIQUE,
        entity_name TEXT(100),
        abn_status TEXT(100),
        entity_type TEXT(100),
        gst_status TEXT(100),
        main_location TEXT(100),
        business_names TEXT(255),
        trading_names TEXT(255)
    );
    """
    )

    try:
        cursor.execute(create_agents_table)
        cursor.execute(create_company_table)
        conn.commit()
        log_info("数据库表初始化完成")
    except Exception as e:
        log_error(f"创建数据表失败: {e}")
    finally:
        conn.close()


# 启动时创建表
create_tables()
