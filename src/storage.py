import sqlite3
import pymysql
from config.settings import DB_CONFIG, log_info, log_error


def connect_db():
    """根据配置连接数据库（MySQL / SQLite）"""
    if DB_CONFIG["type"] == "mysql":
        try:
            conn = pymysql.connect(
                host=DB_CONFIG["mysql"]["host"],
                user=DB_CONFIG["mysql"]["user"],
                password=DB_CONFIG["mysql"]["password"],
                database=DB_CONFIG["mysql"]["database"],
                charset="utf8mb4",
            )
            log_info("成功连接到 MySQL 数据库")
            return conn
        except pymysql.MySQLError as e:
            log_error(f"MySQL 连接错误: {e}")
            return None
    else:
        try:
            conn = sqlite3.connect(DB_CONFIG["sqlite_path"])
            log_info("成功连接到 SQLite 数据库")
            return conn
        except sqlite3.Error as e:
            log_error(f"SQLite 连接错误: {e}")
            return None


def create_tables():
    """创建数据表（如果不存在）"""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    # `agents` 表（LinkedIn 爬取的数据）
    create_agents_table = """
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

    # `company_details` 表（ABN 查询结果）
    create_company_table = """
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

    try:
        cursor.execute(create_agents_table)
        cursor.execute(create_company_table)
        conn.commit()
        log_info("数据库表检查完成")
    except Exception as e:
        log_error(f"创建数据表失败: {e}")
    finally:
        conn.close()


def save_company_details(details):
    """存储 ABN 查询到的公司详细信息"""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO company_details (abn, entity_name, abn_status, entity_type, gst_status, main_location, business_names, trading_names) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(abn) DO UPDATE SET
    entity_name = excluded.entity_name,
    abn_status = excluded.abn_status,
    entity_type = excluded.entity_type,
    gst_status = excluded.gst_status,
    main_location = excluded.main_location,
    business_names = excluded.business_names,
    trading_names = excluded.trading_names;
    """

    try:
        cursor.execute(
            insert_sql,
            (
                details["abn"],
                details["entity_name"],
                details["abn_status"],
                details["entity_type"],
                details["gst_status"],
                details["main_location"],
                details["business_names"],
                details["trading_names"],
            ),
        )

        conn.commit()
        log_info(f"成功存储 ABN 数据: {details['abn']}")
    except Exception as e:
        log_error(f"存储 ABN 数据失败: {e}")
    finally:
        conn.close()


# 启动时创建表
create_tables()
