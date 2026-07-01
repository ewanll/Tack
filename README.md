# Tack · 桌面悬浮待办工具

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green)

Tack 是一个桌面悬浮待办工具，核心是一个**透明悬浮时钟**，可随意拖动改变位置，双击打开**周历+待办**主窗口，可Esc退出主窗口和设置窗口。数据保存在本地 JSON 文件中，可配合 Google Drive / OneDrive / iCloud 实现多设备同步。

## 截图

<img width="637" height="657" alt="dsaf" src="https://github.com/user-attachments/assets/024f4a86-82db-4f3f-83d5-0126805a661e" />

<img width="393" height="609" alt="Screedsafdnshot 2026-07-01 132722" src="https://github.com/user-attachments/assets/35113906-33da-47ba-8058-5f57a71be928" />


## 功能

- 🕐 **透明悬浮时钟** — 实时显示时间 + 今日待办计数，始终置顶
- 📋 **周历 + 待办** — 增删改查、勾选完成、双击编辑、拖拽排序
- 🔍 **搜索过滤** — 实时搜索待办
- 📦 **多行粘贴** — 一键粘贴多行拆成多条待办
- 🌐 **双语界面** — 中文简体 / English
- 🎨 **可自定义** — 字体颜色、字号、透明度、是否显示周数
- 🚀 **开机自启** — 可选
- 💾 **数据同步** — 通过云盘目录实现多设备同步

## 快速开始

```bash
# 1. 克隆项目
git clone https://github.com/<你的用户名>/tack.git
cd tack

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py
```

### 打包成 exe

```bash
pip install pyinstaller
pyinstaller Tack.spec
```

运行后在 `dist/Tack/` 目录找到 `Tack.exe`。

## 技术栈

- **前端层** — PyQt6 + QWebEngineView（HTML/CSS/JS）
- **通信桥** — QWebChannel（Python ↔ JavaScript）
- **数据层** — 本地 JSON 文件

## 同步说明

Tack 不直接对接任何云盘 API。在设置中选择 Google Drive / OneDrive / Dropbox / iCloud 的本地同步目录，云盘桌面客户端自动完成同步。

## 许可证

[MIT](LICENSE)
