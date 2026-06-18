from src.untitled import *
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Qt, Signal
import os
import yaml

class Controller(Ui_ConfigTab, Ui_TestPointTab, Ui_TestCaseTab, Ui_OtherTab, Ui_MainWindow):
    def __init__(self):
        super(Controller, self).__init__()
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'systemConfig.yaml')
        self.current_image_path = None
        
    # ==================== 初始化方法 ====================
    def init_controller(self, main_window):
        """初始化控制器，连接所有信号和槽"""
        # 设置主窗口引用
        self.main_window = main_window
        
        # 由于setupUi已经将控件设置到main_window上，我们需要通过main_window访问这些控件
        # 或者直接从父类继承的控件（因为它们已经被setupUi初始化了）
        
        # 连接菜单栏动作 - 使用 hasattr 检查属性是否存在
        if hasattr(self, 'actionsave'):
            self.actionsave.triggered.connect(self.save_config)
        
        # 连接配置页按钮 - 检查属性存在性
        if hasattr(self, 'saveBtn'):
            self.saveBtn.clicked.connect(self.save_config)
        if hasattr(self, 'loadBtn'):
            self.loadBtn.clicked.connect(self.load_config)
        
        # 连接配置页按钮
        self.saveBtn.clicked.connect(self.save_config)
        self.loadBtn.clicked.connect(self.load_config)
        
        # 连接配置页浏览按钮
        if hasattr(self, 'pointJsonPathBrowseBtn'):
            self.pointJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.pointJsonPathInput))
        if hasattr(self, 'pointTemplatePathBrowseBtn'):
            self.pointTemplatePathBrowseBtn.clicked.connect(lambda: self.browse_file(self.pointTemplatePathInput))
        if hasattr(self, 'pointImgPathBrowseBtn'):
            self.pointImgPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.pointImgPathInput))
        if hasattr(self, 'caseJsonPathBrowseBtn'):
            self.caseJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.caseJsonPathInput))
        if hasattr(self, 'caseXmindPathBrowseBtn'):
            self.caseXmindPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.caseXmindPathInput))
        if hasattr(self, 'caseExeclPathBrowseBtn'):
            self.caseExeclPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.caseExeclPathInput))
        if hasattr(self, 'otherJsonPathBrowseBtn'):
            self.otherJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.otherJsonPathInput))
        if hasattr(self, 'otherTemplatePathBrowseBtn'):
            self.otherTemplatePathBrowseBtn.clicked.connect(lambda: self.browse_file(self.otherTemplatePathInput))
        if hasattr(self, 'otherImgPathBrowseBtn'):
            self.otherImgPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.otherImgPathInput))
        
        # 连接测试点功能页按钮
        if hasattr(self, 'imageRadio'):
            self.imageRadio.toggled.connect(self.toggle_input_method)
        if hasattr(self, 'textRadio'):
            self.textRadio.toggled.connect(self.toggle_input_method)
        if hasattr(self, 'imageBrowseBtn'):
            self.imageBrowseBtn.clicked.connect(self.select_image)
        if hasattr(self, 'generateBtn'):
            self.generateBtn.clicked.connect(self.generate_test_points)
        if hasattr(self, 'clearBtn'):
            self.clearBtn.clicked.connect(self.clear_test_points)
        if hasattr(self, 'exportBtn'):
            self.exportBtn.clicked.connect(self.export_test_points)
        
        # 连接测试用例页按钮
        if hasattr(self, 'xmindRadio'):
            self.xmindRadio.toggled.connect(self.toggle_case_input_method)
        if hasattr(self, 'textRadio'):
            self.textRadio.toggled.connect(self.toggle_case_input_method)
        if hasattr(self, 'xmindBrowseBtn'):
            self.xmindBrowseBtn.clicked.connect(lambda: self.browse_file(self.xmindPathInput))
        if hasattr(self, 'templateBrowseBtn'):
            self.templateBrowseBtn.clicked.connect(lambda: self.browse_file(self.templateInput))
        if hasattr(self, 'outputBrowseBtn'):
            self.outputBrowseBtn.clicked.connect(lambda: self.browse_file(self.outputPathInput))
        if hasattr(self, 'generateBtn'):
            self.generateBtn.clicked.connect(self.generate_test_cases)
        if hasattr(self, 'clearBtn'):
            self.clearBtn.clicked.connect(self.clear_test_cases)
        if hasattr(self, 'exportXmindBtn'):
            self.exportXmindBtn.clicked.connect(self.export_to_xmind)
        if hasattr(self, 'exportXlsxBtn'):
            self.exportXlsxBtn.clicked.connect(self.export_to_xlsx)
        
        # 连接其他功能页按钮
        if hasattr(self, 'inputXmindBrowse'):
            self.inputXmindBrowse.clicked.connect(lambda: self.browse_file(self.inputXmindInput))
        if hasattr(self, 'outputXlsxBrowse'):
            self.outputXlsxBrowse.clicked.connect(lambda: self.browse_file(self.outputXlsxInput))
        if hasattr(self, 'xmindToXlsxBtn'):
            self.xmindToXlsxBtn.clicked.connect(self.convert_xmind_to_xlsx)
        if hasattr(self, 'testPointBrowse'):
            self.testPointBrowse.clicked.connect(lambda: self.browse_file(self.testPointInput))
        if hasattr(self, 'testPointOutputBrowse'):
            self.testPointOutputBrowse.clicked.connect(lambda: self.browse_file(self.testPointOutput))
        if hasattr(self, 'testPointToXlsxBtn'):
            self.testPointToXlsxBtn.clicked.connect(self.convert_testpoint_to_xlsx)
        if hasattr(self, 'clearLogBtn'):
            self.clearLogBtn.clicked.connect(self.clear_log)
        
        # 加载配置
        self.load_config()
    
    # ==================== 工具方法 ====================
    def browse_file(self, line_edit):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择文件",
            line_edit.text() or "",
            "所有文件 (*.*)|JSON文件 (*.json)|XMind文件 (*.xmind)|Excel文件 (*.xlsx)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def select_image(self):
        """选择图片并显示预览"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择图片",
            "",
            "图片文件 (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            self.current_image_path = file_path
            self.imagePathInput.setText(file_path)
            
            # 显示图片预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.imagePreviewArea.setPixmap(scaled_pixmap)
                self.imagePreviewArea.setAlignment(Qt.AlignCenter)
    
    def toggle_input_method(self):
        """切换测试点输入方式"""
        if self.imageRadio.isChecked():
            self.imageGroup.setVisible(True)
            self.textGroup.setVisible(False)
        else:
            self.imageGroup.setVisible(False)
            self.textGroup.setVisible(True)
    
    def toggle_case_input_method(self):
        """切换测试用例输入方式"""
        if self.xmindRadio.isChecked():
            self.xmindGroup.setVisible(True)
            self.textGroup.setVisible(False)
        else:
            self.xmindGroup.setVisible(False)
            self.textGroup.setVisible(True)
    
    def save_config(self):
        """保存配置到YAML文件"""
        try:
            config = {
                'DEEPSEEK_API_KEY': self.apiKeyInput.text(),
                'OUTPUT_JSON_PATH': self.pointJsonPathInput.text(),
                'DEFAULT_TEMPLATE_PATH': self.pointTemplatePathInput.text(),
                'IMG_PATH': self.pointImgPathInput.text(),
                'TEST_XMIND_PATH': self.caseJsonPathInput.text(),
                'TEMPLATE_XMIND_PATH': self.caseXmindPathInput.text(),
                'TESTCASE_JSON_PATH': self.caseExeclPathInput.text(),
                'CONVERTED_TESTCASES_JSON_PATH': self.otherJsonPathInput.text(),
                'TEMPLATE_PATH': self.otherTemplatePathInput.text(),
                'TEST_POINT_XMIND_FILE': self.otherImgPathInput.text()
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            
            self.append_log("配置保存成功！")
            QMessageBox.information(self.main_window, "成功", "配置保存成功！")
        except Exception as e:
            error_msg = f"保存配置失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    def load_config(self):
        """从YAML文件加载配置"""
        try:
            if not os.path.exists(self.config_path):
                self.append_log("配置文件不存在，使用默认配置")
                return
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config:
                self.apiKeyInput.setText(config.get('DEEPSEEK_API_KEY', ''))
                self.pointJsonPathInput.setText(config.get('OUTPUT_JSON_PATH', ''))
                self.pointTemplatePathInput.setText(config.get('DEFAULT_TEMPLATE_PATH', ''))
                self.pointImgPathInput.setText(config.get('IMG_PATH', ''))
                self.caseJsonPathInput.setText(config.get('TEST_XMIND_PATH', ''))
                self.caseXmindPathInput.setText(config.get('TEMPLATE_XMIND_PATH', ''))
                self.caseExeclPathInput.setText(config.get('TESTCASE_JSON_PATH', ''))
                self.otherJsonPathInput.setText(config.get('CONVERTED_TESTCASES_JSON_PATH', ''))
                self.otherTemplatePathInput.setText(config.get('TEMPLATE_PATH', ''))
                self.otherImgPathInput.setText(config.get('TEST_POINT_XMIND_FILE', ''))
                
                self.append_log("配置加载成功！")
        except Exception as e:
            error_msg = f"加载配置失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    # ==================== 工具方法 ====================
    def append_log(self, message):
        """追加日志输出 - 尝试多个可能的 logText 来源"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 尝试从不同的UI父类中获取logText
        try:
            if hasattr(self, 'logText'):
                self.logText.appendPlainText(f"[{timestamp}] {message}")
        except Exception as e:
            print(f"[时间戳] {timestamp} {message} - Log error: {e}")
    
    def clear_log(self):
        """清空日志 - 尝试从不同的UI父类中获取logText"""
        try:
            if hasattr(self, 'logText'):
                self.logText.clear()
        except Exception as e:
            print(f"Clear log error: {e}")
    
    # ==================== 业务逻辑方法 ====================
    def generate_test_points(self):
        """生成测试点"""
        try:
            self.append_log("开始生成测试点...")
            
            # 这里应该调用实际的测试点生成逻辑
            # 暂时显示提示信息
            if self.imageRadio.isChecked():
                img_path = self.imagePathInput.text()
                if not img_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择图片")
                    return
                self.append_log(f"识别图片：{img_path}")
            else:
                text = self.testPointTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试点内容")
                    return
                self.append_log("处理文本输入")
            
            # 检查选项
            options = []
            if self.strictCheck.isChecked():
                options.append("严格模式")
            if self.detailedCheck.isChecked():
                options.append("详细输出")
            if options:
                self.append_log(f"选项：{', '.join(options)}")
            
            self.append_log("测试点生成完成（示例）")
            QMessageBox.information(self.main_window, "成功", "测试点生成完成（示例）")
            
        except Exception as e:
            error_msg = f"生成测试点失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    def clear_test_points(self):
        """清空测试点输入"""
        self.imagePathInput.clear()
        self.testPointTextInput.clear()
        self.imagePreviewArea.setText("暂无预览")
        self.imagePreviewArea.setPixmap(QPixmap())
        self.current_image_path = None
        self.strictCheck.setChecked(False)
        self.detailedCheck.setChecked(False)
        self.append_log("已清空测试点输入")
    
    def export_test_points(self):
        """导出测试点到XMind"""
        try:
            output_path = self.pointJsonPathInput.text()
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请先配置输出JSON路径")
                return
            
            self.append_log(f"导出测试点到：{output_path}")
            # 这里应该实现实际的导出逻辑
            QMessageBox.information(self.main_window, "成功", "导出功能待实现")
            
        except Exception as e:
            error_msg = f"导出测试点失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    def generate_test_cases(self):
        """生成测试用例"""
        try:
            self.append_log("开始生成测试用例...")
            
            # 检查输入
            if self.xmindRadio.isChecked():
                xmind_path = self.xmindPathInput.text()
                if not xmind_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择XMind文件")
                    return
                self.append_log(f"读取XMind文件：{xmind_path}")
            else:
                text = self.testCaseTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试用例内容")
                    return
                self.append_log("处理文本输入")
            
            # 检查输出路径
            output_path = self.outputPathInput.text()
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请先配置输出路径")
                return
            
            self.append_log(f"输出路径：{output_path}")
            self.append_log("测试用例生成完成（示例）")
            QMessageBox.information(self.main_window, "成功", "测试用例生成完成（示例）")
            
        except Exception as e:
            error_msg = f"生成测试用例失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    def clear_test_cases(self):
        """清空测试用例输入"""
        self.xmindPathInput.clear()
        self.templateInput.clear()
        self.outputPathInput.clear()
        self.testCaseTextInput.clear()
        self.append_log("已清空测试用例输入")
    
    def export_to_xmind(self):
        """导出为XMind格式"""
        QMessageBox.information(self.main_window, "提示", "导出XMind功能待实现")
        self.append_log("导出XMind功能待实现")
    
    def export_to_xlsx(self):
        """导出为Excel格式"""
        QMessageBox.information(self.main_window, "提示", "导出Excel功能待实现")
        self.append_log("导出Excel功能待实现")
    
    def convert_xmind_to_xlsx(self):
        """转换XMind到Excel"""
        try:
            input_path = self.inputXmindInput.text()
            output_path = self.outputXlsxInput.text()
            
            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择输入的XMind文件")
                return
            
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return
            
            self.append_log(f"转换中：{input_path} -> {output_path}")
            
            # 这里应该调用实际的转换逻辑
            QMessageBox.information(self.main_window, "成功", "转换功能待实现")
            
        except Exception as e:
            error_msg = f"转换失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
    
    def convert_testpoint_to_xlsx(self):
        """转换测试点XMind到Excel"""
        try:
            input_path = self.testPointInput.text()
            output_path = self.testPointOutput.text()
            
            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择测试点XMind文件")
                return
            
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return
            
            self.append_log(f"转换测试点：{input_path} -> {output_path}")
            
            # 这里应该调用实际的转换逻辑
            QMessageBox.information(self.main_window, "成功", "转换功能待实现")
            
        except Exception as e:
            error_msg = f"转换失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
