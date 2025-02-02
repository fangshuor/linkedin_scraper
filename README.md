```
linkedin_scraper/
│── config/
│   ├── settings.py        # 统一管理 `USE_PROXY` 代理开关
│   ├── proxy.py           # 代理读取 & 缓存（从 `proxy.txt` 读取）
│   ├── cookies.py         # Cookies 读取（从 `cookies.json` 读取）
│── src/
│   ├── scraper.py         # 主爬虫程序
│   ├── rotate_identity.py # 伪装身份（User-Agent 轮换）
│   ├── storage.py         # 数据存储
│── web/
│   ├── app.py             # 运行管理面板的Web服务
│   ├── templates/         # 前端页面
│   ├── static/            # 静态资源（CSS/JS）
│── requirements.txt       # 依赖库清单
│── deploy.sh              # 一键部署脚本
│── README.md              # 项目介绍和使用说明
```