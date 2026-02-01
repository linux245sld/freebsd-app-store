#!/bin/sh
# FreeBSD 應用程式商店 - 快速安裝腳本

echo "======================================"
echo "FreeBSD 應用程式商店 - 安裝程式"
echo "======================================"
echo ""

# 檢查是否為 FreeBSD
if [ "$(uname -s)" != "FreeBSD" ]; then
    echo "❌ 錯誤: 此程式僅支援 FreeBSD 系統"
    exit 1
fi

echo "✓ 檢測到 FreeBSD 系統"
echo ""

# 檢查 Python 版本
echo "正在檢查 Python..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ 未檢測到 Python 3"
    echo "正在安裝 Python 3..."
    sudo pkg install -y python3
else
    echo "✓ Python 3 已安裝: $(python3 --version)"
fi
echo ""

# 檢查 PyQt6
echo "正在檢查 PyQt6..."
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "❌ 未檢測到 PyQt6"
    echo "正在安裝 PyQt6..."
    sudo pkg install -y py311-qt6-pyqt
else
    echo "✓ PyQt6 已安裝"
fi
echo ""

# 詢問是否安裝 Wine
echo "是否安裝 Wine（用於 Windows 應用程式支援）? (y/n)"
read -r install_wine

if [ "$install_wine" = "y" ] || [ "$install_wine" = "Y" ]; then
    echo "正在檢查 Wine..."
    if ! command -v wine >/dev/null 2>&1; then
        echo "正在安裝 Wine..."
        sudo pkg install -y wine
    else
        echo "✓ Wine 已安裝: $(wine --version)"
    fi
    
    echo ""
    echo "是否安裝 Wine 常用組件 (winetricks, 字型等)? (y/n)"
    read -r install_extras
    
    if [ "$install_extras" = "y" ] || [ "$install_extras" = "Y" ]; then
        echo "正在安裝 winetricks..."
        sudo pkg install -y winetricks
        
        echo "正在初始化 Wine 環境..."
        WINEARCH=win64 wineboot
        
        echo "正在安裝 Windows 字型..."
        winetricks -q corefonts
        
        echo "正在安裝 Visual C++ 運行庫..."
        winetricks -q vcrun2019
    fi
fi

echo ""
echo "======================================"
echo "✅ 安裝完成！"
echo "======================================"
echo ""
echo "執行以下命令啟動應用程式商店："
echo ""
echo "  python3 freebsd_app_store.py"
echo ""
echo "或者："
echo ""
echo "  ./freebsd_app_store.py"
echo ""
echo "======================================"
