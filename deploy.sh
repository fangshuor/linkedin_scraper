#!/bin/bash

# 设置错误中断
set -e

# 变量
GITHUB_REPO="github.com/fangshuor/linkedin_scraper"
PROJECT_DIR="/opt/linkedin_scraper"
PYTHON_VERSION="python3"

echo "📢 开始部署爬虫系统..."

# 更新系统 & 安装基础软件
echo "📦 更新系统 & 安装依赖..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y git $PYTHON_VERSION $PYTHON_VERSION-pip

# 克隆 GitHub 仓库
if [ ! -d "$PROJECT_DIR" ]; then
    echo "🔄 克隆项目代码..."
    sudo git clone $GITHUB_REPO $PROJECT_DIR
else
    echo "🔄 代码已存在，更新代码..."
    cd $PROJECT_DIR
    sudo git pull
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

# 配置 MySQL（可选，按需修改）
echo "💾 初始化数据库..."
$PYTHON_VERSION -c "from src.storage import create_tables; create_tables()"

# 设置爬虫服务（Gunicorn + Supervisor）
echo "🛠 配置爬虫 & Web 服务器..."

# 爬虫启动脚本
cat <<EOF | sudo tee /etc/systemd/system/linkedin_scraper.service
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

# Web 服务器启动脚本
cat <<EOF | sudo tee /etc/systemd/system/linkedin_web.service
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
sudo systemctl daemon-reload
sudo systemctl enable linkedin_scraper
sudo systemctl enable linkedin_web
sudo systemctl restart linkedin_scraper
sudo systemctl restart linkedin_web

# 防火墙设置（如果使用 UFW）
echo "🔒 配置防火墙（如适用）..."
if command -v ufw >/dev/null 2>&1; then
    sudo ufw allow 5000/tcp
    sudo ufw allow 22/tcp
    sudo ufw enable
fi

echo "🚀 部署完成！"
echo "🔗 Web 界面: http://<服务器IP>:5000"
echo "📌 爬虫已在后台运行，可用 'sudo systemctl status linkedin_scraper' 查看状态"