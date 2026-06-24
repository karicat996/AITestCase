from src.untitled import Ui_MainWindow
from PySide6.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Qt, Signal
import os
import yaml

class Controller:
    def __init__(self, ui: Ui_MainWindow, main_window):
        """初始化控制器，引用Ui_MainWindow中的Tab实例"""
        self.ui = ui
        self.main_window = main_window
        
        # 引用各Tab实例，通过它们访问各自的控件
        self.configTab = ui.configTab
        self.testPointTab = ui.testPointTab
        self.testCaseTab = ui.testCaseTab
        self.otherTab = ui.otherTab
        
        # 配置文件路径
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'systemConfig.yaml')
        
        # 连接信号与槽
        self.init_ui()

    def init_ui(self):
        """连接所有信号和槽"""
        # ==================== 配置页面 ====================
        self.configTab.apiKeyInput.textChanged.connect(self.api_key_changed)
        self.configTab.modelCombo.currentIndexChanged.connect(self.model_changed)
        self.configTab.pointJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.pointJsonPathInput))
        self.configTab.pointTemplatePathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.pointTemplatePathInput))
        self.configTab.pointImgPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.pointImgPathInput))
        self.configTab.caseJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.caseJsonPathInput))
        self.configTab.caseXmindPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.caseXmindPathInput))
        self.configTab.caseExeclPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.caseExeclPathInput))
        self.configTab.otherJsonPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.otherJsonPathInput))
        self.configTab.otherTemplatePathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.otherTemplatePathInput))
        self.configTab.otherImgPathBrowseBtn.clicked.connect(lambda: self.browse_file(self.configTab.otherImgPathInput))
        # 保存配置和初始化按钮
        self.configTab.saveBtn.clicked.connect(self.save_config)
        self.configTab.loadBtn.clicked.connect(self.load_config)

        # ==================== 测试点功能页面 ====================
        self.testPointTab.imageRadio.toggled.connect(self.toggle_input_method)
        self.testPointTab.tp_textRadio.toggled.connect(self.toggle_input_method)
        self.testPointTab.imageBrowseBtn.clicked.connect(self.select_image)
        self.testPointTab.tp_generateBtn.clicked.connect(self.generate_test_points)
        self.testPointTab.tp_clearBtn.clicked.connect(self.clear_test_points)
        self.testPointTab.exportBtn.clicked.connect(self.export_test_points)

        # ==================== 测试用例功能页面 ====================
        self.testCaseTab.xmindRadio.toggled.connect(self.toggle_case_input_method)
        self.testCaseTab.tc_textRadio.toggled.connect(self.toggle_case_input_method)
        self.testCaseTab.xmindBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.xmindPathInput))
        self.testCaseTab.templateBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.templateInput))
        self.testCaseTab.outputBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.outputPathInput))
        self.testCaseTab.tc_generateBtn.clicked.connect(self.generate_test_cases)
        self.testCaseTab.tc_clearBtn.clicked.connect(self.clear_test_cases)
        self.testCaseTab.exportXmindBtn.clicked.connect(self.export_to_xmind)
        self.testCaseTab.exportXlsxBtn.clicked.connect(self.export_to_xlsx)

        # ==================== 其他功能页面 ====================
        self.otherTab.inputXmindBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.inputXmindInput))
        self.otherTab.outputXlsxBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.outputXlsxInput))
        self.otherTab.xmindToXlsxBtn.clicked.connect(self.convert_xmind_to_xlsx)
        self.otherTab.testPointBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.testPointInput))
        self.otherTab.testPointOutputBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.testPointOutput))
        self.otherTab.testPointToXlsxBtn.clicked.connect(self.convert_testpoint_to_xlsx)
        self.otherTab.clearLogBtn.clicked.connect(self.clear_log)

        # 加载已有配置
        self.load_config()

    # ==================== 工具方法 ====================
    def browse_file(self, line_edit):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "选择文件",
            line_edit.text() or "",
            "所有文件 (*.*);;JSON文件 (*.json);;XMind文件 (*.xmind);;Excel文件 (*.xlsx)"
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
            self.testPointTab.imagePathInput.setText(file_path)

            # 显示图片预览
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 200,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.testPointTab.imagePreviewArea.setPixmap(scaled_pixmap)
                self.testPointTab.imagePreviewArea.setAlignment(Qt.AlignCenter)

    def toggle_input_method(self):
        """切换测试点输入方式"""
        if self.testPointTab.imageRadio.isChecked():
            self.testPointTab.imageGroup.setVisible(True)
            self.testPointTab.tp_textGroup.setVisible(False)
        else:
            self.testPointTab.imageGroup.setVisible(False)
            self.testPointTab.tp_textGroup.setVisible(True)

    def toggle_case_input_method(self):
        """切换测试用例输入方式"""
        if self.testCaseTab.xmindRadio.isChecked():
            self.testCaseTab.xmindGroup.setVisible(True)
            self.testCaseTab.tc_textGroup.setVisible(False)
        else:
            self.testCaseTab.xmindGroup.setVisible(False)
            self.testCaseTab.tc_textGroup.setVisible(True)

    def save_config(self):
        """保存配置到YAML文件"""
        try:
            config = {
                'DEEPSEEK_API_KEY': self.configTab.apiKeyInput.text(),
                'OUTPUT_JSON_PATH': self.configTab.pointJsonPathInput.text(),
                'DEFAULT_TEMPLATE_PATH': self.configTab.pointTemplatePathInput.text(),
                'IMG_PATH': self.configTab.pointImgPathInput.text(),
                'TEST_XMIND_PATH': self.configTab.caseJsonPathInput.text(),
                'TEMPLATE_XMIND_PATH': self.configTab.caseXmindPathInput.text(),
                'TESTCASE_JSON_PATH': self.configTab.caseExeclPathInput.text(),
                'CONVERTED_TESTCASES_JSON_PATH': self.configTab.otherJsonPathInput.text(),
                'TEMPLATE_PATH': self.configTab.otherTemplatePathInput.text(),
                'TEST_POINT_XMIND_FILE': self.configTab.otherImgPathInput.text()
            }

            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
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
                self.configTab.apiKeyInput.setText(config.get('DEEPSEEK_API_KEY', ''))
                self.configTab.pointJsonPathInput.setText(config.get('OUTPUT_JSON_PATH', ''))
                self.configTab.pointTemplatePathInput.setText(config.get('DEFAULT_TEMPLATE_PATH', ''))
                self.configTab.pointImgPathInput.setText(config.get('IMG_PATH', ''))
                self.configTab.caseJsonPathInput.setText(config.get('TEST_XMIND_PATH', ''))
                self.configTab.caseXmindPathInput.setText(config.get('TEMPLATE_XMIND_PATH', ''))
                self.configTab.caseExeclPathInput.setText(config.get('TESTCASE_JSON_PATH', ''))
                self.configTab.otherJsonPathInput.setText(config.get('CONVERTED_TESTCASES_JSON_PATH', ''))
                self.configTab.otherTemplatePathInput.setText(config.get('TEMPLATE_PATH', ''))
                self.configTab.otherImgPathInput.setText(config.get('TEST_POINT_XMIND_FILE', ''))

                self.append_log("配置加载成功！")
        except Exception as e:
            error_msg = f"加载配置失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)

    # ==================== 日志方法 ====================
    def append_log(self, message):
        """追加日志输出到OtherTab的日志区域"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.otherTab.logText.appendPlainText(f"[{timestamp}] {message}")
        except Exception as e:
            print(f"[{timestamp}] {message} - Log error: {e}")

    def clear_log(self):
        """清空日志"""
        try:
            self.otherTab.logText.clear()
        except Exception as e:
            print(f"Clear log error: {e}")

    # ==================== 业务逻辑方法 ====================
    def api_key_changed(self, text):
        """API Key变化时的处理"""
        pass

    def model_changed(self, index):
        """模型选择变化时的处理"""
        model_name = self.configTab.modelCombo.currentText()
        self.append_log(f"模型切换为：{model_name}")

    def generate_test_points(self):
        """生成测试点"""
        try:
            self.append_log("开始生成测试点...")

            if self.testPointTab.imageRadio.isChecked():
                img_path = self.testPointTab.imagePathInput.text()
                if not img_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择图片")
                    return
                self.append_log(f"识别图片：{img_path}")
            else:
                text = self.testPointTab.testPointTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试点内容")
                    return
                self.append_log("处理文本输入")

            # 检查选项
            options = []
            if self.testPointTab.strictCheck.isChecked():
                options.append("严格模式")
            if self.testPointTab.detailedCheck.isChecked():
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
        self.testPointTab.imagePathInput.clear()
        self.testPointTab.testPointTextInput.clear()
        self.testPointTab.imagePreviewArea.setText("暂无预览")
        self.testPointTab.imagePreviewArea.setPixmap(QPixmap())
        self.current_image_path = None
        self.testPointTab.strictCheck.setChecked(False)
        self.testPointTab.detailedCheck.setChecked(False)
        self.append_log("已清空测试点输入")

    def export_test_points(self):
        """导出测试点到XMind"""
        try:
            output_path = self.configTab.pointJsonPathInput.text()
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请先配置输出JSON路径")
                return

            self.append_log(f"导出测试点到：{output_path}")
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
            if self.testCaseTab.xmindRadio.isChecked():
                xmind_path = self.testCaseTab.xmindPathInput.text()
                if not xmind_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择XMind文件")
                    return
                self.append_log(f"读取XMind文件：{xmind_path}")
            else:
                text = self.testCaseTab.testCaseTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试用例内容")
                    return
                self.append_log("处理文本输入")

            # 检查输出路径
            output_path = self.testCaseTab.outputPathInput.text()
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
        self.testCaseTab.xmindPathInput.clear()
        self.testCaseTab.templateInput.clear()
        self.testCaseTab.outputPathInput.clear()
        self.testCaseTab.testCaseTextInput.clear()
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
            input_path = self.otherTab.inputXmindInput.text()
            output_path = self.otherTab.outputXlsxInput.text()

            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择输入的XMind文件")
                return

            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return

            self.append_log(f"转换中：{input_path} -> {output_path}")
            QMessageBox.information(self.main_window, "成功", "转换功能待实现")

        except Exception as e:
            error_msg = f"转换失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)

    def convert_testpoint_to_xlsx(self):
        """转换测试点XMind到Excel"""
        try:
            input_path = self.otherTab.testPointInput.text()
            output_path = self.otherTab.testPointOutput.text()

            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择测试点XMind文件")
                return

            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return

            self.append_log(f"转换测试点：{input_path} -> {output_path}")
            QMessageBox.information(self.main_window, "成功", "转换功能待实现")

        except Exception as e:
            error_msg = f"转换失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)
