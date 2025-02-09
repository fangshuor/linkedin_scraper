#!/bin/bash

set -e  # 遇到错误时停止执行

# 变量
GITHUB_REPO="https://github.com/fangshuor/linkedin_scraper.git"
PROJECT_DIR="/opt/linkedin_scraper"
PYTHON_VERSION="python3"
MYSQL_ROOT_PASS="linkedin_scraper_pass"
MYSQL_DB_NAME="linkedin_scraper"
SCRAPER_SERVICE="linkedin_scraper"
WEB_SERVICE="linkedin_web"

# =============================
# 🔹 显示主菜单
# =============================
function show_menu() {
    echo "==========================================="
    echo "          LinkedIn Scraper 部署管理        "
    echo "==========================================="
    echo "1) 安装 / 更新爬虫"
    echo "2) 覆盖安装（删除旧版并重新安装）"
    echo "3) 卸载爬虫"
    echo "4) 检查运行状态"
    echo "5) 启动服务"
    echo "6) 停止服务"
    echo "7) 查看日志错误"
    echo "0) 退出"
    echo "-------------------------------------------"
}

# =============================
# 🔹 安装 / 更新爬虫
# =============================
function install_scraper() {
    echo "📢 开始安装爬虫系统..."

    # 更新系统 & 安装基础软件
    echo "📦 更新系统 & 安装依赖..."
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y git $PYTHON_VERSION $PYTHON_VERSION-pip python3-venv mysql-server

    # 检查 MySQL 是否已安装
    if ! command -v mysql &> /dev/null; then
        echo "💾 MySQL 未安装，开始安装..."
        sudo apt install -y mysql-server
        sudo systemctl enable mysql
        sudo systemctl start mysql
    fi

    # 配置 MySQL 数据库
    echo "🔧 配置 MySQL..."
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;"
    sudo mysql -e "CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '$MYSQL_ROOT_PASS';"
    sudo mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DB_NAME.* TO 'root'@'localhost';"
    sudo mysql -e "FLUSH PRIVILEGES;"

    # 检查是否已有安装
    if [ -d "$PROJECT_DIR" ]; then
        echo "🔄 更新代码..."
        cd $PROJECT_DIR
        sudo git pull origin main
    else
        echo "🔄 克隆项目代码..."
        sudo git clone $GITHUB_REPO $PROJECT_DIR
    fi

    # 进入项目目录
    cd $PROJECT_DIR

    # 创建 Python 虚拟环境
    if [ ! -d "venv" ]; then
        echo "🐍 创建 Python 虚拟环境..."
        $PYTHON_VERSION -m venv venv
    fi

    # 启动虚拟环境
    echo "🔧 激活虚拟环境..."
    source venv/bin/activate

    # 安装 Python 依赖
    echo "📦 安装 Python 依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt

    # 初始化数据库
    echo "💾 初始化数据库..."
    $PYTHON_VERSION -c "from src.storage import create_tables; create_tables()"

    # 启动服务
    start_services
}

# =============================
# 🔹 覆盖安装（删除旧版并重新安装）
# =============================
function reinstall_scraper() {
    echo "🗑️  删除旧版本..."
    stop_services
    sudo rm -rf $PROJECT_DIR
    install_scraper
}

# =============================
# 🔹 卸载爬虫
# =============================
function uninstall_scraper() {
    echo "🗑️  正在卸载 LinkedIn Scraper..."
    stop_services
    sudo rm -rf $PROJECT_DIR
    sudo systemctl disable $SCRAPER_SERVICE || true
    sudo systemctl disable $WEB_SERVICE || true
    echo "✅ 已成功卸载 LinkedIn Scraper"
}

# =============================
# 🔹 启动服务
# =============================
function start_services() {
    echo "🚀 启动爬虫 & Web 服务器..."
    sudo systemctl restart $SCRAPER_SERVICE || true
    sudo systemctl restart $WEB_SERVICE || true
    echo "✅ 爬虫已启动"
}

# =============================
# 🔹 停止服务
# =============================
function stop_services() {
    echo "🛑 停止爬虫 & Web 服务器..."
    sudo systemctl stop $SCRAPER_SERVICE || true
    sudo systemctl stop $WEB_SERVICE || true
    echo "✅ 服务已停止"
}

# =============================
# 🔹 检查运行状态
# =============================
function check_status() {
    echo "📌 爬虫运行状态："
    sudo systemctl status $SCRAPER_SERVICE || true
    echo "-------------------------------------------"
    echo "📌 Web 服务器运行状态："
    sudo systemctl status $WEB_SERVICE || true
}

# =============================
# 🔹 查看日志错误
# =============================
function check_logs() {
    echo "📜 最近的爬虫日志错误："
    journalctl -u $SCRAPER_SERVICE --no-pager --lines=20 || true
    echo "-------------------------------------------"
    echo "📜 最近的 Web 服务器日志错误："
    journalctl -u $WEB_SERVICE --no-pager --lines=20 || true
}

# =============================
# 🔹 主程序（交互界面）
# =============================
while true; do
    show_menu
    read -p "请选择操作 (0-7): " choice
    case $choice in
        1) install_scraper ;;
        2) reinstall_scraper ;;
        3) uninstall_scraper ;;
        4) check_status ;;
        5) start_services ;;
        6) stop_services ;;
        7) check_logs ;;
        0) echo "👋 退出"; exit 0 ;;
        *) echo "⚠️  无效选择，请重新输入！" ;;
    esac
    echo "==========================================="
done