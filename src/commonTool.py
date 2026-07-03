# -*- coding: utf-8 -*-
"""
通用工具模块
包含：UI初始化、文件浏览、配置管理、日志工具、后台Worker线程基类及各类Worker
"""
import os
from datetime import datetime

import yaml
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFileDialog, QMessageBox

from service.interfaceIntegration import (
    interfaceAITestPoint,
    interfaceImageAITestPointXmind,
    interfaceTestPointToAITestCaseXmind,
    interfaceAIAnyFlieToXlsx,
    interfaceAITestCaseXlsx,
    TestPointXmindToTestcaseXlsx,
)
from common.pathConfig import path_config, DEFAULT_OUTPUT_DIR


# ========================== CommonTool 基类 ==========================

class CommonTool:
    """控制器基类，提供UI初始化、文件浏览、配置管理、日志等通用工具方法"""

    def __init__(self, ui, main_window):
        self.ui = ui
        self.main_window = main_window

        # 引用各Tab实例
        self.configTab = ui.configTab
        self.testPointTab = ui.testPointTab
        self.testCaseTab = ui.testCaseTab
        self.otherTab = ui.otherTab

        # 配置文件路径
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'config', 'systemConfig.yaml'
        )

        # 当前活跃的Worker引用（防止被GC回收）
        self._active_worker = None

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
        self.testCaseTab.testcaseRadio.toggled.connect(self.toggle_case_input_method)
        self.testCaseTab.xmindBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.xmindPathInput))
        self.testCaseTab.testCaseXmindBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.testCaseXmindPathInput))
        self.testCaseTab.templateBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.templateInput))
        self.testCaseTab.outputBrowseBtn.clicked.connect(lambda: self.browse_file(self.testCaseTab.outputPathInput))
        self.testCaseTab.tc_text_generateBtn.clicked.connect(self.generate_text_cases)
        self.testCaseTab.tc_generateBtn.clicked.connect(self.generate_test_cases)
        self.testCaseTab.tc_clearBtn.clicked.connect(self.clear_test_cases)
        self.testCaseTab.exportXmindBtn.clicked.connect(self.export_to_xmind)
        self.testCaseTab.exportXlsxBtn.clicked.connect(self.export_xmind_to_xlsx)

        # ==================== 其他功能页面 ====================
        self.otherTab.inputXmindBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.inputXmindInput))
        self.otherTab.outputXlsxBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.outputXlsxInput))
        self.otherTab.xmindToXlsxBtn.clicked.connect(self.convert_xmind_to_xlsx)
        self.otherTab.testPointBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.testPointInput))
        self.otherTab.testPointOutputBrowse.clicked.connect(lambda: self.browse_file(self.otherTab.testPointOutput))
        self.otherTab.testPointToXlsxBtn.clicked.connect(self.convert_testpoint_to_xlsx)
        self.otherTab.clearLogBtn.clicked.connect(self.clear_log)

        # 设置测试用例页面初始按钮可见性（默认xmindRadio选中）
        self.toggle_case_input_method()

        # 加载已有配置
        self.load_config()

    # ==================== 文件浏览工具 ====================

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
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    400, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.testPointTab.imagePreviewArea.setPixmap(scaled_pixmap)
                self.testPointTab.imagePreviewArea.setAlignment(Qt.AlignCenter)

    # ==================== UI切换工具 ====================

    def toggle_input_method(self):
        """切换测试点输入方式"""
        if self.testPointTab.imageRadio.isChecked():
            self.testPointTab.imageGroup.setVisible(True)
            self.testPointTab.tp_textGroup.setVisible(False)
        else:
            self.testPointTab.imageGroup.setVisible(False)
            self.testPointTab.tp_textGroup.setVisible(True)

    def toggle_case_input_method(self):
        """切换测试用例输入方式，同时控制对应输入区域和操作按钮的可见性"""
        if self.testCaseTab.xmindRadio.isChecked():
            # 测试点XMind导入模式
            self.testCaseTab.xmindGroup.setVisible(True)
            self.testCaseTab.tc_textGroup.setVisible(False)
            self.testCaseTab.testCaseXmindGroup.setVisible(False)
            self.testCaseTab.outputGroup.setVisible(True)
            self.testCaseTab.tc_generateBtn.setVisible(True)
            self.testCaseTab.tc_text_generateBtn.setVisible(False)
            self.testCaseTab.exportXmindBtn.setVisible(True)
            self.testCaseTab.exportXlsxBtn.setVisible(True)
            self.testCaseTab.tc_clearBtn.setVisible(True)
        elif self.testCaseTab.testcaseRadio.isChecked():
            # 测试用例XMind导入模式：仅显示测试用例XMind输入、输出设置、转Excel和清空按钮
            self.testCaseTab.xmindGroup.setVisible(False)
            self.testCaseTab.tc_textGroup.setVisible(False)
            self.testCaseTab.testCaseXmindGroup.setVisible(True)
            self.testCaseTab.outputGroup.setVisible(True)
            self.testCaseTab.tc_generateBtn.setVisible(False)
            self.testCaseTab.tc_text_generateBtn.setVisible(False)
            self.testCaseTab.exportXmindBtn.setVisible(False)
            self.testCaseTab.exportXlsxBtn.setVisible(True)
            self.testCaseTab.tc_clearBtn.setVisible(True)
        else:
            # 文本输入模式
            self.testCaseTab.xmindGroup.setVisible(False)
            self.testCaseTab.tc_textGroup.setVisible(True)
            self.testCaseTab.testCaseXmindGroup.setVisible(False)
            self.testCaseTab.outputGroup.setVisible(True)
            self.testCaseTab.tc_generateBtn.setVisible(False)
            self.testCaseTab.tc_text_generateBtn.setVisible(True)
            self.testCaseTab.exportXmindBtn.setVisible(True)
            self.testCaseTab.exportXlsxBtn.setVisible(True)
            self.testCaseTab.tc_clearBtn.setVisible(True)

    # ==================== 配置管理 ====================

    def save_config(self):
        """保存配置到YAML文件"""
        try:
            config = {
                'DEEPSEEK_API_KEY': self.configTab.apiKeyInput.text(),
                'OUTPUT_JSON_PATH': self.configTab.pointJsonPathInput.text(),
                'DEFAULT_TEMPLATE_PATH': self.configTab.pointTemplatePathInput.text(),
                'IMG_PATH': self.configTab.pointImgPathInput.text(),
                # 测试用例页面：JSON输出路径 → TESTCASE_JSON_PATH
                'TESTCASE_JSON_PATH': self.configTab.caseJsonPathInput.text(),
                # 测试用例页面：XMind保存路径 → TEMPLATE_XMIND_PATH
                'TEMPLATE_XMIND_PATH': self.configTab.caseXmindPathInput.text(),
                # 测试用例页面：Excel保存路径 → TEST_XMIND_PATH
                'TEST_XMIND_PATH': self.configTab.caseExeclPathInput.text(),
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

    def _save_config_silent(self):
        """静默保存配置（不弹窗），确保API Key等配置即时生效"""
        try:
            config = {
                'DEEPSEEK_API_KEY': self.configTab.apiKeyInput.text(),
                'OUTPUT_JSON_PATH': self.configTab.pointJsonPathInput.text(),
                'DEFAULT_TEMPLATE_PATH': self.configTab.pointTemplatePathInput.text(),
                'IMG_PATH': self.configTab.pointImgPathInput.text(),
                'TESTCASE_JSON_PATH': self.configTab.caseJsonPathInput.text(),
                'TEMPLATE_XMIND_PATH': self.configTab.caseXmindPathInput.text(),
                'TEST_XMIND_PATH': self.configTab.caseExeclPathInput.text(),
                'CONVERTED_TESTCASES_JSON_PATH': self.configTab.otherJsonPathInput.text(),
                'TEMPLATE_PATH': self.configTab.otherTemplatePathInput.text(),
                'TEST_POINT_XMIND_FILE': self.configTab.otherImgPathInput.text()
            }
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            self.append_log(f"静默保存配置失败：{str(e)}")

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
                self.configTab.caseJsonPathInput.setText(config.get('TESTCASE_JSON_PATH', ''))
                self.configTab.caseXmindPathInput.setText(config.get('TEMPLATE_XMIND_PATH', ''))
                self.configTab.caseExeclPathInput.setText(config.get('TEST_XMIND_PATH', ''))
                self.configTab.otherJsonPathInput.setText(config.get('CONVERTED_TESTCASES_JSON_PATH', ''))
                self.configTab.otherTemplatePathInput.setText(config.get('TEMPLATE_PATH', ''))
                self.configTab.otherImgPathInput.setText(config.get('TEST_POINT_XMIND_FILE', ''))
                self.append_log("配置加载成功！")
        except Exception as e:
            error_msg = f"加载配置失败：{str(e)}"
            self.append_log(error_msg)
            QMessageBox.critical(self.main_window, "错误", error_msg)

    # ==================== 日志工具 ====================

    def append_log(self, message):
        """追加日志输出到OtherTab的日志区域"""
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

    # ==================== Worker管理工具 ====================

    def _get_output_dir(self):
        """获取默认输出目录（UI配置 → PathConfig默认）"""
        output_dir = os.path.dirname(self.configTab.pointJsonPathInput.text())
        if not output_dir:
            output_dir = path_config.resolve_output_dir()
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def _start_worker(self, worker, start_msg="开始执行..."):
        """
        通用的Worker启动方法
        1. 静默保存配置（确保API Key即时生效）
        2. 连接信号
        3. 启动线程
        """
        self._save_config_silent()
        self.append_log(start_msg)
        worker.log_signal.connect(self.append_log)
        worker.finished_signal.connect(self._on_worker_finished)
        self._active_worker = worker
        worker.start()

    def _on_worker_finished(self, success, message):
        """Worker完成后的统一回调"""
        if success:
            self.append_log(f"✓ {message}")
            QMessageBox.information(self.main_window, "成功", message)
        else:
            self.append_log(f"✗ {message}")
            QMessageBox.critical(self.main_window, "失败", message)
        self._active_worker = None


# ========================== Worker 线程基类 ==========================

class BaseWorker(QThread):
    """后台Worker基类，提供日志信号和完成信号的统一封装"""
    log_signal = Signal(str)
    finished_signal = Signal(bool, str)  # (是否成功, 结果消息)

    def __init__(self, parent=None):
        super().__init__(parent)


class GenerateTestPointWorker(BaseWorker):
    """生成测试点Worker"""

    def __init__(self, image_path=None, text_input=None,
                 output_json=None, output_xmind=None, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.text_input = text_input
        self.output_json = output_json
        self.output_xmind = output_xmind

    def run(self):
        try:
            if self.image_path:
                self.log_signal.emit(f"识别图片并生成测试点：{self.image_path}")
                converter = interfaceImageAITestPointXmind()
                result = converter.get_test_points_from_image(
                    image_path=self.image_path,
                    test_point_json=self.output_json,
                    xmind_output=self.output_xmind
                )
                if result:
                    self.finished_signal.emit(True, "图片测试点生成成功")
                else:
                    self.finished_signal.emit(False, "图片测试点生成失败")
            else:
                self.log_signal.emit("文本输入生成测试点...")
                converter = interfaceAITestPoint()
                converter.get_test_point(
                    user_input=self.text_input,
                    output_path=self.output_xmind,
                    storage_json=self.output_json
                )
                self.finished_signal.emit(True, "测试点生成成功")
        except Exception as e:
            self.finished_signal.emit(False, f"生成测试点失败：{str(e)}")


class ExportTestPointWorker(BaseWorker):
    """导出测试点JSON到XMind"""

    def __init__(self, json_path, output_xmind, parent=None):
        super().__init__(parent)
        self.json_path = json_path
        self.output_xmind = output_xmind

    def run(self):
        try:
            import json
            from service.xmindChanger import TestcasePointJsonToXmind

            with open(self.json_path, 'r', encoding='utf-8') as f:
                test_data = json.load(f)

            converter = TestcasePointJsonToXmind()
            success = converter.convert_and_export_to_xmind(
                input_data=test_data,
                output_xmind_file=self.output_xmind,
                root_title="测试大纲",
                sheet_title="功能测试用例"
            )
            if success:
                self.finished_signal.emit(True, f"测试点XMind导出成功：{self.output_xmind}")
            else:
                self.finished_signal.emit(False, "测试点XMind导出失败")
        except Exception as e:
            self.finished_signal.emit(False, f"导出测试点失败：{str(e)}")


class GenerateTestCaseWorker(BaseWorker):
    """从测试点XMind生成测试用例XMind"""

    def __init__(self, xmind_path, output_dir=None, parent=None):
        super().__init__(parent)
        self.xmind_path = xmind_path
        self.output_dir = output_dir

    def run(self):
        try:
            self.log_signal.emit(f"读取测试点XMind：{self.xmind_path}")
            converter = interfaceTestPointToAITestCaseXmind()
            kwargs = {'xmind_file': self.xmind_path}
            if self.output_dir:
                kwargs['output_dir'] = self.output_dir
            success = converter.convert_testpoint_to_testcase_xmind(**kwargs)
            if success:
                self.finished_signal.emit(True, "测试用例XMind生成成功")
            else:
                self.finished_signal.emit(False, "测试用例XMind生成失败")
        except Exception as e:
            self.finished_signal.emit(False, f"生成测试用例失败：{str(e)}")


class GenerateTextCaseWorker(BaseWorker):
    """从文本输入一键生成测试用例（全链路：文本→测试点→测试用例→XMind→XLSX）"""

    def __init__(self, text_input, output_dir=None, parent=None):
        super().__init__(parent)
        self.text_input = text_input
        self.output_dir = output_dir

    def run(self):
        try:
            self.log_signal.emit("文本输入一键生成测试用例...")
            converter = interfaceAIAnyFlieToXlsx()
            success = converter.generate_testcase_xlsx_from_text(
                user_input=self.text_input,
                output_dir=self.output_dir
            )
            if success:
                self.finished_signal.emit(True, "测试用例生成成功")
            else:
                self.finished_signal.emit(False, "测试用例生成失败")
        except Exception as e:
            self.finished_signal.emit(False, f"生成测试用例失败：{str(e)}")


class ExportTestCaseXmindWorker(BaseWorker):
    """测试用例JSON转XMind"""

    def __init__(self, json_path, output_xmind, parent=None):
        super().__init__(parent)
        self.json_path = json_path
        self.output_xmind = output_xmind

    def run(self):
        try:
            import json as json_mod
            from service.xmindChanger import TestcaseJsonToXmind

            # 直接读取绝对路径JSON文件
            with open(self.json_path, 'r', encoding='utf-8') as f:
                testcase_data = json_mod.load(f)
            if not testcase_data:
                self.finished_signal.emit(False, "读取测试用例JSON失败")
                return

            converter = TestcaseJsonToXmind()
            success = converter.convert_and_export_to_xmind(
                input_data=testcase_data,
                output_xmind_file=self.output_xmind,
                root_title="测试用例",
                sheet_title="功能测试用例"
            )
            if success:
                self.finished_signal.emit(True, f"测试用例XMind导出成功：{self.output_xmind}")
            else:
                self.finished_signal.emit(False, "测试用例XMind导出失败")
        except Exception as e:
            self.finished_signal.emit(False, f"导出XMind失败：{str(e)}")


class XmindToXlsxWorker(BaseWorker):
    """XMind转Excel通用Worker"""

    def __init__(self, xmind_path, output_xlsx, parent=None):
        super().__init__(parent)
        self.xmind_path = xmind_path
        self.output_xlsx = output_xlsx

    def run(self):
        try:
            converter = TestPointXmindToTestcaseXlsx()
            success = converter.convert_xmind_to_testcase_xlsx(
                xmind_file=self.xmind_path,
                output_xlsx_file=self.output_xlsx
            )
            if success:
                self.finished_signal.emit(True, f"Excel导出成功：{self.output_xlsx}")
            else:
                self.finished_signal.emit(False, "Excel导出失败")
        except Exception as e:
            self.finished_signal.emit(False, f"转换失败：{str(e)}")


class TestcaseXmindToXlsxWorker(BaseWorker):
    """测试用例XMind转Excel通用Worker"""

    def __init__(self, xmind_path, output_xlsx, parent=None):
        super().__init__(parent)
        self.xmind_path = xmind_path
        self.output_xlsx = output_xlsx

    def run(self):
        try:
            converter = interfaceAITestCaseXlsx()
            success = converter.get_testcase_xlsx(
                xmind_file_path=self.xmind_path,
                output_xlsx_path=self.output_xlsx
            )
            if success:
                self.finished_signal.emit(True, f"Excel导出成功：{self.output_xlsx}")
            else:
                self.finished_signal.emit(False, "Excel导出失败")
        except Exception as e:
            self.finished_signal.emit(False, f"转换失败：{str(e)}")


