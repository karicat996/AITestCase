import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from src.untitled import Ui_MainWindow
from src.controller import Controller

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def main():
    """主函数 - 应用程序入口"""
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    # 创建控制器，连接所有信号与槽
    controller = Controller(ui, MainWindow)
    
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
