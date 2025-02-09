#!/bin/bash

set -e

# 变量
GITHUB_REPO="https://github.com/fangshuor/linkedin_scraper.git"
PROJECT_DIR="/opt/linkedin_scraper"
PYTHON_VERSION="python3"
MYSQL_ROOT_PASS="linkedin_scraper_pass"
MYSQL_DB_NAME="linkedin_scraper"

echo "📢 开始部署爬虫系统..."

# 更新系统 & 安装基础软件
echo "📦 更新系统 & 安装依赖..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git $PYTHON_VERSION $PYTHON_VERSION-pip

# 检查 MySQL 是否已安装
if ! command -v mysql &> /dev/null; then
    echo "💾 MySQL 未安装，开始安装..."
    sudo apt install -y mysql-server
    sudo systemctl enable mysql
    sudo systemctl start mysql
fi

# 设置 MySQL
echo "🔧 配置 MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '$MYSQL_ROOT_PASS';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DB_NAME.* TO 'root'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# 克隆 GitHub 仓库
if [ ! -d "$PROJECT_DIR" ]; then
    echo "🔄 克隆项目代码..."
    sudo git clone $GITHUB_REPO $PROJECT_DIR
else
    echo "🔄 代码已存在，更新代码..."
    cd $PROJECT_DIR
    sudo git pull origin main
fi

# 进入项目目录
cd $PROJECT_DIR

# 创建虚拟环境
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

# 配置数据库
echo "💾 初始化数据库..."
$PYTHON_VERSION -c "from src.storage import create_tables; create_tables()"

# 启动爬虫服务
sudo systemctl restart linkedin_scraper
sudo systemctl restart linkedin_web

echo "🚀 部署完成！"
echo "🔗 Web 界面: http://<服务器IP>:5000"
echo "📌 爬虫已在后台运行，可用 'sudo systemctl status linkedin_scraper' 查看状态"