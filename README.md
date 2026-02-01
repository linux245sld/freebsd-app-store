# FreeBSD 應用程式商店

這是一個專為 FreeBSD 設計的輕量化圖形化應用程式商店，支援 PKG 套件安裝和 Wine Windows 應用程式。

## 功能特色

✨ **雙語支援**：繁體中文和英文介面
📦 **PKG 整合**：直接從 FreeBSD pkg 源安裝軟體
🍷 **Wine 支援**：安裝以下 Windows 應用程式：
- LINE 通訊軟體
- WhatsApp
- WeChat (微信)
- QQ
- 植物大戰殭屍 (Plants vs. Zombies)

🎨 **輕量化設計**：基於 PyQt6，資源占用少
🔍 **搜尋功能**：快速找到需要的應用程式
📊 **即時日誌**：查看安裝進度和狀態

## 系統需求

- FreeBSD 12.0 或更高版本
- Python 3.8+
- PyQt6
- Wine (用於安裝 Windows 應用程式)

## 安裝步驟

### 1. 安裝依賴套件

```bash
# 更新 pkg 資料庫
sudo pkg update

# 安裝 Python 和 PyQt6
sudo pkg install python3 py39-pyqt6

# 安裝 Wine (用於 Windows 應用程式)
sudo pkg install wine
```

### 2. 下載並執行應用程式商店

```bash
# 賦予執行權限
chmod +x freebsd_app_store.py

# 執行應用程式
python3 freebsd_app_store.py
```

## 使用說明

### PKG 應用程式安裝

1. 點擊「PKG 應用程式」分頁
2. 瀏覽或搜尋想要的套件
3. 點擊套件查看詳細資訊
4. 點擊「安裝」按鈕進行安裝（需要 root 權限）

### Wine 應用程式安裝

1. 點擊「Wine 應用程式」分頁
2. **重要**：先下載對應的 Windows 安裝程式到 `~/Downloads/` 目錄：
   - LINE: `LineInst.exe`
   - WhatsApp: `WhatsAppSetup.exe`
   - WeChat: `WeChatSetup.exe`
   - QQ: `QQ.exe`
   - 植物大戰殭屍: `PlantsVsZombiesSetup.exe`
3. 選擇要安裝的應用程式
4. 點擊「安裝」按鈕，Wine 會啟動安裝程式

### 語言切換

點擊右上角的語言下拉選單，選擇「繁體中文」或「English」。

## Wine 應用程式下載來源

由於版權原因，本應用程式商店不提供 Windows 軟體的下載。請從以下官方來源下載：

- **LINE**: https://line.me/
- **WhatsApp**: https://www.whatsapp.com/
- **WeChat**: https://www.wechat.com/
- **QQ**: https://im.qq.com/
- **植物大戰殭屍**: 請從合法遊戲平台購買

## Wine 配置建議

首次使用 Wine 前，建議進行初始化：

```bash
# 初始化 Wine 環境
winecfg

# 安裝常用 Windows 組件
winetricks corefonts
winetricks vcrun2019
```

## 常見問題

### Q: 安裝 PKG 套件時提示權限不足？
在運行此腳本之前請在終端機上運行sudo -v

### Q: Wine 應用程式無法啟動？
**A**: 
1. 確認 Wine 已正確安裝：`wine --version`
2. 檢查安裝檔案路徑是否正確
3. 嘗試在終端機手動執行安裝命令以查看錯誤訊息

### Q: 如何新增其他 Wine 應用程式？
**A**: 編輯 `freebsd_app_store.py`，在 `init_wine_apps()` 函數中新增應用程式資訊。

### Q: 可以安裝哪些 PKG 套件？
**A**: 理論上可以安裝 FreeBSD pkg 倉庫中的所有套件。使用搜尋功能查找需要的軟體。

## 進階功能

### 自訂 Wine 前綴

如果你想為不同的應用程式使用不同的 Wine 環境：

```bash
# 為 LINE 創建專用環境
WINEPREFIX=~/.wine-line wine ~/Downloads/LineInst.exe
```

### 自動啟動

要讓應用程式商店隨系統啟動，可以將其加入自動啟動項目。

## 技術架構

- **介面框架**: PyQt6
- **套件管理**: FreeBSD pkg
- **Windows 相容層**: Wine
- **多執行緒**: QThread 用於非阻塞安裝過程

## 授權

本專案為開源軟體，歡迎自由使用和修改。

## 貢獻

歡迎提交問題報告和功能建議！

## 注意事項

⚠️ **重要提醒**:
- 安裝 PKG 套件需要 root 權限
- Wine 應用程式的相容性可能因版本而異
- 請從官方渠道下載 Windows 軟體，避免安全風險
- 某些 Wine 應用程式可能需要額外的 Windows 組件（使用 winetricks 安裝）

## 更新日誌

### v1.0.0 (2026-02-01)
- ✅ 初始版本發布
- ✅ 支援 PKG 套件管理
- ✅ 支援 5 款 Wine 應用程式
- ✅ 繁體中文/英文雙語介面
- ✅ 即時安裝日誌顯示

---

**祝您使用愉快！** 🎉
