from flask import Flask, render_template, jsonify, request, send_file
import os
import pandas as pd
import sqlite3
import pymysql
import time
from config.settings import DB_CONFIG, log_info, log_error
from src.storage import connect_db

app = Flask(__name__)

# =============================
# 🔹 获取数据库统计信息
# =============================


def get_db_status():
    conn = connect_db()
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM agents")
        total_agents = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM company_details")
        total_companies = cursor.fetchone()[0]

        cursor.execute("PRAGMA page_count;")  # SQLite 存储大小
        total_pages = cursor.fetchone()[0]
        cursor.execute("PRAGMA page_size;")
        page_size = cursor.fetchone()[0]
        db_size = (total_pages * page_size) / (1024 * 1024)  # 转换为 MB

        return {
            "total_agents": total_agents,
            "total_companies": total_companies,
            "db_size": round(db_size, 2) if db_size else "未知",
        }
    except Exception as e:
        log_error(f"数据库统计失败: {e}")
        return None
    finally:
        conn.close()


# =============================
# 🔹 Web 页面
# =============================


@app.route("/")
def index():
    db_status = get_db_status()
    return render_template("index.html", db_status=db_status)


# =============================
# 🔹 查重 ABN（查找重复公司）
# =============================


@app.route("/check_duplicates")
def check_duplicates():
    conn = connect_db()
    if not conn:
        return jsonify({"error": "数据库连接失败"})

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT abn, COUNT(*) FROM agents GROUP BY abn HAVING COUNT(*) > 1"
        )
        duplicates = cursor.fetchall()

        return jsonify({"duplicates": duplicates})
    except Exception as e:
        log_error(f"查重失败: {e}")
        return jsonify({"error": str(e)})
    finally:
        conn.close()


# =============================
# 🔹 一键导出 Excel
# =============================


@app.route("/export", methods=["POST"])
def export_data():
    data_type = request.form.get("type")
    amount = request.form.get("amount")

    conn = connect_db()
    if not conn:
        return jsonify({"error": "数据库连接失败"})

    cursor = conn.cursor()

    try:
        if data_type == "latest":
            cursor.execute(f"SELECT * FROM agents ORDER BY id DESC LIMIT {amount}")
        elif data_type == "days":
            cursor.execute(
                f"SELECT * FROM agents WHERE date_added >= date('now', '-{amount} days')"
            )
        else:
            return jsonify({"error": "无效的导出类型"})

        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=columns)

        export_path = "exported_data.xlsx"
        df.to_excel(export_path, index=False)

        return send_file(export_path, as_attachment=True)
    except Exception as e:
        log_error(f"导出失败: {e}")
        return jsonify({"error": str(e)})
    finally:
        conn.close()


# =============================
# 🔹 搜索数据库
# =============================


@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("q", "").strip()

    if not keyword:
        return jsonify({"error": "请输入搜索关键词"})

    conn = connect_db()
    if not conn:
        return jsonify({"error": "数据库连接失败"})

    cursor = conn.cursor()

    try:
        cursor.execute(
            f"SELECT * FROM agents WHERE name LIKE ? OR company LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"),
        )
        results = cursor.fetchall()

        return jsonify({"results": results})
    except Exception as e:
        log_error(f"搜索失败: {e}")
        return jsonify({"error": str(e)})
    finally:
        conn.close()


# =============================
# 🔹 仅保留 ABN 号码
# =============================


@app.route("/clean_db", methods=["POST"])
def clean_db():
    conn = connect_db()
    if not conn:
        return jsonify({"error": "数据库连接失败"})

    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM agents WHERE abn IS NULL OR abn = 'N/A'")
        conn.commit()
        log_info("数据库清理完成，仅保留 ABN")
        return jsonify({"status": "success"})
    except Exception as e:
        log_error(f"清理失败: {e}")
        return jsonify({"error": str(e)})
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
