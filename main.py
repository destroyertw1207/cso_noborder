import os
import sys
import time
import ctypes

from pywinauto import Application
from pywinauto.win32functions import SetWindowLong
import win32gui
import win32con
import win32api
import win32clipboard
from screeninfo import get_monitors

import uiautomation as auto
import pygetwindow as gw

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QMessageBox, QDialog
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtCore import Qt, QMetaObject, Q_ARG
from window import Ui_Form

# 獲取所有顯示器資訊
monitors = get_monitors()
monitor = monitors[0]

def run_as_admin():
    # 檢查是否以管理員身份運行
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # 如果不是，重新啟動腳本以管理員身份運行
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
        sys.exit(0)

mainwindow = None

window_titles = [
      "Counter-Strike Online"
    , "Counter-Strike Nexon"
]

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global mainwindow
        mainwindow = self
        
        self.setFixedSize(self.width(), self.height())

        self.pushButton.clicked.connect(self.noborder)
        self.pushButton_2.clicked.connect(self.reset)
        self.pushButton_3.clicked.connect(self.center)

    def noborder(self):
        for window_title in window_titles:
            if gw.getWindowsWithTitle(window_title):
                hwnd = gw.getWindowsWithTitle(window_title)[0]._hWnd
                
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0] + round(16 / 2)
                y = rect[1] + 31
                width = rect[2] - rect[0] - 16
                height = rect[3] - rect[1] - 32 - 7
                
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                
                if style & win32con.WS_CAPTION:
                    
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style & ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME))
                    win32gui.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                    
                break
        
    def reset(self):
        for window_title in window_titles:
            if gw.getWindowsWithTitle(window_title):
                hwnd = gw.getWindowsWithTitle(window_title)[0]._hWnd
                
                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0] - round(16 / 2)
                y = rect[1] - 31
                width = rect[2] - rect[0] + 16
                height = rect[3] - rect[1] + 32 + 7
                
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                
                if not (style & win32con.WS_CAPTION):
                    
                    new_style = style | win32con.WS_CAPTION
                    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)
                    win32gui.SetWindowPos(hwnd, None, x, y, width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                    
                break
    
    def center(self):
        for window_title in window_titles:
            if gw.getWindowsWithTitle(window_title):
                hwnd = gw.getWindowsWithTitle(window_title)[0]._hWnd

                rect = win32gui.GetWindowRect(hwnd)
                x = rect[0]
                y = rect[1]
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                win32gui.SetWindowPos(hwnd, None, round(monitor.width / 2 - width / 2), round(monitor.height / 2 - height / 2), width, height, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
                
                break

    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    run_as_admin()

    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    
    sys.exit(app.exec())