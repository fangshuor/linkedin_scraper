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

echo "📢 开始部署爬虫系统..."

# =============================
# 🔹 更新系统 & 安装基础软件
# =============================
echo "📦 更新系统 & 安装依赖..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git $PYTHON_VERSION $PYTHON_VERSION-pip python3-venv mysql-server

# =============================
# 🔹 检查 MySQL 是否已安装
# =============================
if ! command -v mysql &> /dev/null; then
    echo "💾 MySQL 未安装，开始安装..."
    sudo apt install -y mysql-server
    sudo systemctl enable mysql
    sudo systemctl start mysql
fi

# =============================
# 🔹 配置 MySQL 数据库
# =============================
echo "🔧 配置 MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DB_NAME;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'root'@'localhost' IDENTIFIED BY '$MYSQL_ROOT_PASS';"
sudo mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DB_NAME.* TO 'root'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# =============================
# 🔹 克隆 GitHub 仓库
# =============================
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

# =============================
# 🔹 创建 Python 虚拟环境（如果不存在）
# =============================
if [ ! -d "venv" ]; then
    echo "🐍 创建 Python 虚拟环境..."
    $PYTHON_VERSION -m venv venv
fi

# 确保虚拟环境存在
if [ ! -f "venv/bin/activate" ]; then
    echo "⚠️  发现虚拟环境丢失，重新创建..."
    rm -rf venv
    $PYTHON_VERSION -m venv venv
fi

# 启动虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# =============================
# 🔹 安装 Python 依赖
# =============================
echo "📦 安装 Python 依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# =============================
# 🔹 初始化数据库
# =============================
echo "💾 初始化数据库..."
$PYTHON_VERSION -c "from src.storage import create_tables; create_tables()"

# =============================
# 🔹 配置 systemd 服务
# =============================

echo "🛠 配置爬虫 & Web 服务器服务..."

# 🔹 爬虫服务
cat <<EOF | sudo tee /etc/systemd/system/$SCRAPER_SERVICE.service
[Unit]
Description=LinkedIn Scraper Service
After=network.target

[Service]
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python3 $PROJECT_DIR/src/scraper.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 🔹 Web 服务器服务
cat <<EOF | sudo tee /etc/systemd/system/$WEB_SERVICE.service
[Unit]
Description=LinkedIn Web Interface
After=network.target

[Service]
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 web.app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd & 启动服务
echo "🔄 重新加载 systemd 并启动服务..."
sudo systemctl daemon-reload
sudo systemctl enable $SCRAPER_SERVICE
sudo systemctl enable $WEB_SERVICE
sudo systemctl restart $SCRAPER_SERVICE
sudo systemctl restart $WEB_SERVICE

# =============================
# 🔹 防火墙配置（如果使用 UFW）
# =============================
echo "🔒 配置防火墙（如适用）..."
if command -v ufw >/dev/null 2>&1; then
    sudo ufw allow 5000/tcp
    sudo ufw allow 22/tcp
    sudo ufw enable
fi

echo "🚀 部署完成！"
echo "🔗 Web 界面: http://<服务器IP>:5000"
echo "📌 爬虫已在后台运行，可用 'sudo systemctl status $SCRAPER_SERVICE' 查看状态"