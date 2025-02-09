import sqlite3
import pymysql
from config.settings import DB_CONFIG, log_info, log_error

# =============================
# 🔹 连接数据库
# =============================


def connect_db():
    """连接数据库（自动选择 MySQL 或 SQLite）"""
    if DB_CONFIG["type"] == "mysql":
        try:
            conn = pymysql.connect(
                host=DB_CONFIG["mysql"]["host"],
                user=DB_CONFIG["mysql"]["user"],
                password=DB_CONFIG["mysql"]["password"],
                database=DB_CONFIG["mysql"]["database"],
                charset="utf8mb4",
            )
            log_info("成功连接到 MySQL")
            return conn
        except pymysql.MySQLError as e:
            log_error(f"MySQL 连接失败: {e}")
            return None
    else:
        try:
            conn = sqlite3.connect(DB_CONFIG["sqlite_path"])
            log_info("成功连接到 SQLite")
            return conn
        except sqlite3.Error as e:
            log_error(f"SQLite 连接失败: {e}")
            return None


# =============================
# 🔹 创建数据表
# =============================


def create_tables():
    """创建数据库表"""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

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
        log_info("数据库表初始化完成")
    except Exception as e:
        log_error(f"创建数据表失败: {e}")
    finally:
        conn.close()


# =============================
# 🔹 存储 LinkedIn 爬取数据
# =============================


def save_to_database(data):
    """存储 LinkedIn 爬取的数据到数据库"""
    conn = connect_db()
    if not conn:
        return

    cursor = conn.cursor()

    insert_sql = (
        """
    INSERT INTO agents (name, company, location, phone, email, company_email, address, abn, company_website) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
        if DB_CONFIG["type"] == "mysql"
        else """
    INSERT INTO agents (name, company, location, phone, email, company_email, address, abn, company_website) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    )

    try:
        cursor.executemany(
            insert_sql,
            [
                (
                    agent.get("name", "N/A"),
                    agent.get("company", "N/A"),
                    agent.get("location", "N/A"),
                    agent.get("phone", "N/A"),
                    agent.get("email", "N/A"),
                    agent.get("company_email", "N/A"),
                    agent.get("address", "N/A"),
                    agent.get("abn", "N/A"),
                    agent.get("company_website", "N/A"),
                )
                for agent in data
            ],
        )

        conn.commit()
        log_info(f"成功存储 {len(data)} 条 LinkedIn 数据")
    except Exception as e:
        log_error(f"存储 LinkedIn 数据失败: {e}")
    finally:
        conn.close()


# =============================
# 🔹 存储 ABN 查询的公司信息
# =============================


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


# =============================
# 🔹 启动时创建表
# =============================

create_tables()
