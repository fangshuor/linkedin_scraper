linkedin_scraper/
│── config/
│   ├── settings.py        # 配置文件，存放代理池、User-Agent池、数据库信息等
│── src/
│   ├── scraper.py         # 爬虫主逻辑，处理LinkedIn的反爬和数据采集
│   ├── rotate_identity.py # 伪装身份，定期更换指纹
│   ├── parser.py          # 解析网页内容，提取目标信息
│   ├── storage.py         # 负责存储爬取到的数据到数据库
│── web/
│   ├── app.py             # 运行管理面板的Web服务
│   ├── templates/         # 前端页面
│   ├── static/            # 静态资源（CSS/JS）
│── requirements.txt       # 依赖库清单
│── deploy.sh              # 一键部署脚本
│── README.md              # 项目介绍和使用说明
