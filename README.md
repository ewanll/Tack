# Tack · 桌面悬浮待办工具

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green)

Tack 是一个桌面悬浮待办工具，核心是一个**透明悬浮时钟**，双击打开**周历+待办**主窗口。数据保存在本地 JSON 文件中，可配合 Google Drive / OneDrive / iCloud 实现多设备同步。

## 截图

_（待补充）_

## 功能

- 🕐 **透明悬浮时钟** — 实时显示时间 + 今日待办计数，始终置顶
- 📋 **周历 + 待办** — 增删改查、勾选完成、双击编辑、拖拽排序
- 🔍 **搜索过滤** — 实时搜索待办
- 📦 **多行粘贴** — 一键粘贴多行拆成多条待办
- 📤 **导出本周待办** — 复制到剪贴板
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
