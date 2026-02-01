#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLabel, QTextEdit,
    QTabWidget, QLineEdit, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPalette, QColor

class InstallThread(QThread):
    """安裝執行緒"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
    
    def run(self):
        try:
            process = subprocess.Popen(
                self.command, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            for line in process.stdout:
                self.progress.emit(line)
            process.wait()
            if process.returncode == 0:
                self.finished.emit(True, "操作成功！")
            else:
                self.finished.emit(False, f"失敗: {process.stderr.read()}")
        except Exception as e:
            self.finished.emit(False, str(e))

class FreeBSDAppStore(QMainWindow):
    def __init__(self):
        super().__init__()
        # 1. 基礎屬性初始化
        self.is_dark_mode = True
        self.current_language = 'zh_TW'
        self.init_translations()
        self.init_wine_apps()

        # 2. UI 骨架建立 (這會順便建立 self.pkg_list)
        self.init_ui()
        
        # 3. 套用主題與載入資料
        self.apply_theme()
        self.load_pkg_apps()

    def t(self, key):
        """翻譯輔助函式"""
        return self.translations.get(self.current_language, self.translations['en_US']).get(key, key)

    def init_translations(self):
        self.translations = {
            'zh_TW': {
                'title': 'FreeBSD 應用程式商店',
                'pkg_apps': 'PKG 應用程式',
                'wine_apps': 'Wine 應用程式',
                'search': '搜尋...',
                'install': '安裝',
                'uninstall': '移除',
                'refresh': '重新整理',
                'language': '語言',
                'status': '狀態',
                'install_log': '安裝日誌',
                'installed': '已安裝',
                'not_installed': '未安裝',
                'wine_support': 'Wine 支援的 Windows 應用程式',
            },
            'en_US': {
                'title': 'FreeBSD App Store',
                'pkg_apps': 'PKG Applications',
                'wine_apps': 'Wine Applications',
                'search': 'Search...',
                'install': 'Install',
                'uninstall': 'Uninstall',
                'refresh': 'Refresh',
                'language': 'Language',
                'status': 'Status',
                'install_log': 'Installation Log',
                'installed': 'Installed',
                'not_installed': 'Not Installed',
                'wine_support': 'Wine Supported Windows Apps',
            }
        }

    def init_wine_apps(self):
        self.wine_apps = {
            'LINE': {'name_zh': 'LINE', 'name_en': 'LINE', 'desc_zh': '通訊軟體', 'desc_en': 'Messenger', 'install_cmd': 'wine ~/Downloads/LineInst.exe', 'check_cmd': 'ls ~/.wine'},
            'PvZ': {'name_zh': '植物大戰殭屍', 'name_en': 'Plants vs Zombies', 'desc_zh': '經典遊戲', 'desc_en': 'Classic Game', 'install_cmd': 'wine ~/Downloads/PvZ.exe', 'check_cmd': 'ls ~/.wine'}
        }

    def apply_theme(self):
        palette = QPalette()
        if self.is_dark_mode:
            palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
            self.setStyleSheet("QWidget { background-color: #2d2d2d; color: white; } QPushButton { background-color: #3d3d3d; color: white; border: 1px solid #555; padding: 5px; }")
        else:
            self.setPalette(self.style().standardPalette())
            self.setStyleSheet("")
        self.setPalette(palette)

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle(self.t('title'))
        self.setGeometry(100, 100, 1000, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 頂部按鈕與工具列
        top_bar = QHBoxLayout()
        theme_btn = QPushButton("🌓 切換主題")
        theme_btn.clicked.connect(self.toggle_theme)
        top_bar.addWidget(theme_btn)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItem('繁體中文', 'zh_TW')
        self.lang_combo.addItem('English', 'en_US')
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        top_bar.addWidget(self.lang_combo)
        main_layout.addLayout(top_bar)

        # 分頁系統
        self.tabs = QTabWidget()
        self.pkg_tab = self.create_pkg_tab()
        self.wine_tab = self.create_wine_tab()
        
        self.tabs.addTab(self.pkg_tab, self.t('pkg_apps'))
        self.tabs.addTab(self.wine_tab, self.t('wine_apps'))
        main_layout.addWidget(self.tabs)
        
        # 安裝日誌區
        main_layout.addWidget(QLabel(self.t('install_log')))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        main_layout.addWidget(self.log_text)

    def create_pkg_tab(self):
        """正確創建 PKG 分頁，確保所有元件在 return 前完成初始化"""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        # 左側列表
        self.pkg_list = QListWidget()
        self.pkg_list.itemClicked.connect(self.on_pkg_selected)
        layout.addWidget(self.pkg_list, 1)

        # 右側控制面板
        right_panel = QVBoxLayout()
        self.pkg_info = QTextEdit()
        self.pkg_info.setReadOnly(True)
        right_panel.addWidget(self.pkg_info)

        btn_layout = QHBoxLayout()
        self.pkg_install_btn = QPushButton(self.t('install'))
        self.pkg_install_btn.clicked.connect(self.install_pkg)
        self.pkg_uninstall_btn = QPushButton(self.t('uninstall'))
        self.pkg_uninstall_btn.clicked.connect(self.uninstall_pkg)
        btn_layout.addWidget(self.pkg_install_btn)
        btn_layout.addWidget(self.pkg_uninstall_btn)
        
        right_panel.addLayout(btn_layout)
        layout.addLayout(right_panel, 2)
        return widget

    def create_wine_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.wine_list = QListWidget()
        self.wine_list.itemClicked.connect(self.on_wine_selected)
        layout.addWidget(self.wine_list, 1)

        right_panel = QVBoxLayout()
        self.wine_info = QTextEdit()
        self.wine_info.setReadOnly(True)
        self.wine_install_btn = QPushButton(self.t('install'))
        self.wine_install_btn.clicked.connect(self.install_wine_app)
        
        right_panel.addWidget(self.wine_info)
        right_panel.addWidget(self.wine_install_btn)
        layout.addLayout(right_panel, 2)
        self.load_wine_apps()
        return widget

    def load_pkg_apps(self):
        self.pkg_list.clear()
        try:
            res = subprocess.run(['pkg', 'query', '%n'], capture_output=True, text=True)
            if res.returncode == 0:
                pkgs = sorted(res.stdout.strip().split('\n'))
                self.pkg_list.addItems(pkgs)
        except Exception as e:
            self.log_text.append(f"讀取 PKG 失敗: {e}")

    def load_wine_apps(self):
        self.wine_list.clear()
        for app_id, data in self.wine_apps.items():
            name = data.get(f'name_{self.current_language.split("_")[0]}', app_id)
            self.wine_list.addItem(name)

    def on_pkg_selected(self, item):
        pkg_name = item.text()
        res = subprocess.run(['pkg', 'info', pkg_name], capture_output=True, text=True)
        self.pkg_info.setPlainText(res.stdout if res.returncode == 0 else "無法取得資訊")
        self.current_pkg = pkg_name

    def on_wine_selected(self, item):
        name = item.text()
        for app_id, data in self.wine_apps.items():
            if data.get('name_zh') == name or data.get('name_en') == name:
                self.current_wine_app = app_id
                self.wine_info.setHtml(f"<h3>{name}</h3><p>{data['desc_zh']}</p>")
                break

    def install_pkg(self):
        if hasattr(self, 'current_pkg'):
            self.run_install_command(f"sudo pkg install -y {self.current_pkg}")

    def uninstall_pkg(self):
        if hasattr(self, 'current_pkg'):
            self.run_install_command(f"sudo pkg remove -y {self.current_pkg}")

    def install_wine_app(self):
        if hasattr(self, 'current_wine_app'):
            cmd = self.wine_apps[self.current_wine_app]['install_cmd']
            self.run_install_command(cmd)

    def run_install_command(self, command):
        self.log_text.clear()
        self.thread = InstallThread(command)
        self.thread.progress.connect(lambda t: self.log_text.append(t.strip()))
        self.thread.finished.connect(lambda s, m: QMessageBox.information(self, "通知", m))
        self.thread.start()

    def change_language(self, index):
        self.current_language = self.lang_combo.itemData(index)
        self.update_ui_language()

    def update_ui_language(self):
        self.setWindowTitle(self.t('title'))
        self.tabs.setTabText(0, self.t('pkg_apps'))
        self.tabs.setTabText(1, self.t('wine_apps'))
        self.pkg_install_btn.setText(self.t('install'))
        self.pkg_uninstall_btn.setText(self.t('uninstall'))
        self.load_wine_apps()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FreeBSDAppStore()
    window.show()
    sys.exit(app.exec())
