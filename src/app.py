import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from src.controller import Controller
from src.uistyle import UIStyleConfig
from PySide6.QtCore import Qt

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def main():
    """主函数 - 应用程序入口"""
    # PySide6 自动启用高 DPI 支持,无需手动设置
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    # 应用现代主题样式
    UIStyleConfig.applyModernTheme(app)
    
    # 创建主窗口和控制器
    controller = Controller()
    
    # 显示主窗口
    from src.untitled import QMainWindow
    main_window = QMainWindow()
    controller.setupUi(main_window)
    controller.init_controller(main_window)
    
    main_window.show()
    
    # 设置窗口标题和图标（可选）
    main_window.setWindowIcon(QIcon())
    
    # 执行应用事件循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()