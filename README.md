# Tack · 桌面悬浮待办工具 / Floating Desktop Todo

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green)

Tack 是一个桌面悬浮待办工具，核心是一个**透明悬浮时钟**，可随意拖动改变位置，双击打开**周历+待办**主窗口，可 Esc 退出主窗口和设置窗口。数据保存在本地 JSON 文件中，可配合 Google Drive / OneDrive / iCloud 实现多设备同步。

Tack is a desktop floating todo tool built around a **transparent floating clock** that you can drag anywhere on screen. Double-click to open the **weekly calendar + todo list** main window. Press Esc to close. Data is stored in a local JSON file and syncs across devices via Google Drive, OneDrive, or iCloud.

## 截图 / Screenshots

<img width="637" height="657" alt="dsaf" src="https://github.com/user-attachments/assets/024f4a86-82db-4f3f-83d5-0126805a661e" />

<img width="393" height="609" alt="Screedsafdnshot 2026-07-01 132722" src="https://github.com/user-attachments/assets/35113906-33da-47ba-8058-5f57a71be928" />

## 功能 / Features

| 中文 | English |
|---|---|
| 🕐 **透明悬浮时钟** — 实时时间 + 今日待办，始终置顶 | 🕐 **Floating clock** — real-time display, always on top |
| 📋 **周历 + 待办** — 增删改查、拖拽排序、勾选完成 | 📋 **Calendar + Todos** — full CRUD, drag & drop, check off |
| 🔍 **搜索过滤** — 实时搜索 | 🔍 **Search** — real-time filtering |
| 📦 **多行粘贴** — Ctrl+V 拆成多条 | 📦 **Multi-line paste** — split by newline |
| 🌐 **双语界面** — 中文 / English | 🌐 **Bilingual UI** — Chinese / English |
| 🎨 **可自定义** — 颜色、字号、透明度 | 🎨 **Customizable** — color, font size, opacity |
| 🚀 **开机自启** — 可选 | 🚀 **Autostart** — optional |
| 💾 **数据同步** — 通过云盘目录 | 💾 **Cloud sync** — via your local sync folder |

## 快速开始 / Quick Start

```bash
# 克隆 / Clone
git clone https://github.com/ewanll/Tack.git
cd Tack

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 运行 / Run
python main.py
```

### 打包成 exe / Build exe

```bash
pip install pyinstaller
python pack.py
```

运行后在 `dist/Tack.exe` 找到可执行文件。

## 技术栈 / Tech Stack

- **前端层** — PyQt6 + QWebEngineView（HTML/CSS/JS）
- **通信桥** — QWebChannel（Python ↔ JavaScript）
- **数据层** — 本地 JSON 文件 / Local JSON file

## 同步说明 / Sync

Tack 不直接对接云盘 API。在设置中选择 Google Drive / OneDrive / Dropbox / iCloud 的本地同步目录，云盘桌面客户端自动完成同步。

Tack does not integrate with any cloud drive API directly. Select your cloud drive's local sync folder in settings to enable cross-device sync.

## 许可证 / License

[MIT](LICENSE)
