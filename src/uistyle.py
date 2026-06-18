# -*- coding: utf-8 -*-
"""UI样式配置模块"""

from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtCore import Qt


class UIStyleConfig:
    """UI样式配置类"""
    
    # 主色调
    PRIMARY_COLOR = "#2196F3"
    SECONDARY_COLOR = "#4CAF50"
    ACCENT_COLOR = "#FF9800"
    DANGER_COLOR = "#F44336"
    
    # 背景色
    BACKGROUND_LIGHT = "#FFFFFF"
    BACKGROUND_GRAY = "#F5F5F5"
    BACKGROUND_DARK = "#333333"
    
    # 文本颜色
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    TEXT_DISABLED = "#BDBDBD"
    
    @staticmethod
    def applyDarkTheme(application):
        """应用暗色主题"""
        application.setStyle("fusion")
        
    @staticmethod
    def applyModernTheme(application):
        """应用现代主题样式 - 从QSS文件加载"""
        import os
        
        # 获取QSS文件路径
        qss_file_path = os.path.join(os.path.dirname(__file__), 'uistyle.qss')
        
        # 读取并应用QSS文件
        try:
            with open(qss_file_path, 'r', encoding='utf-8') as f:
                css = f.read()
            
            application.setStyleSheet(css)
        except FileNotFoundError:
            print(f"警告：样式文件未找到：{qss_file_path}")
            application.setStyle("Fusion")
        except Exception as e:
            print(f"加载样式文件失败：{str(e)}")
            application.setStyle("Fusion")
    
    @staticmethod
    def setupIconFonts(application):
        """设置图标字体（如果需要）"""
        pass
