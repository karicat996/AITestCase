# -*- coding: utf-8 -*-
"""
控制器模块 - 业务逻辑层
Controller 继承 CommonTool，只负责业务逻辑槽函数
所有UI工具、配置管理、日志、Worker线程均在 commonTool.py 中定义
"""
import os

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMessageBox

from src.commonTool import (
    CommonTool,
    GenerateTestPointWorker,
    ExportTestPointWorker,
    GenerateTestCaseWorker,
    GenerateTextCaseWorker,
    TextToXmindWorker,
    ExportTestCaseXmindWorker,
    XmindToXlsxWorker,
    TestcaseXmindToXlsxWorker,
)


class Controller(CommonTool):
    """
    业务逻辑控制器
    继承 CommonTool 获得：init_ui、browse_file、select_image、toggle_*、
    save_config、load_config、append_log、clear_log、_start_worker 等工具方法
    本类只实现各按钮对应的业务逻辑槽函数
    """

    def __init__(self, ui, main_window):
        # CommonTool.__init__ 会完成 UI 引用绑定、信号槽连接和配置加载
        super().__init__(ui, main_window)

    # ==================== 配置变更处理 ====================

    def api_key_changed(self, text):
        """API Key变化时的处理"""
        pass

    def model_changed(self, index):
        """模型选择变化时的处理"""
        model_name = self.configTab.modelCombo.currentText()
        self.append_log(f"模型切换为：{model_name}")

    # ==================== 测试点业务逻辑 ====================

    def generate_test_points(self):
        """生成测试点（支持图片识别 / 文本输入两种模式）"""
        try:
            # 检查模板路径：空则确认是否使用默认配置路径
            template_path = self.configTab.pointTemplatePathInput.text()
            if not self._confirm_default_path(template_path, "模板路径"):
                return

            output_dir = self._get_output_dir()
            output_json = self.configTab.pointJsonPathInput.text() or os.path.join(output_dir, "测试点.json")
            output_xmind = os.path.join(output_dir, "测试点.xmind")

            if self.testPointTab.imageRadio.isChecked():
                # ---- 图片识别模式 ----
                img_path = self.testPointTab.imagePathInput.text()
                if not img_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择图片")
                    return
                worker = GenerateTestPointWorker(
                    image_path=img_path,
                    output_json=output_json,
                    output_xmind=output_xmind
                )
                self._start_worker(worker, f"开始从图片生成测试点：{img_path}")
            else:
                # ---- 文本输入模式 ----
                text = self.testPointTab.testPointTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试点内容")
                    return
                worker = GenerateTestPointWorker(
                    text_input=text,
                    output_json=output_json,
                    output_xmind=output_xmind
                )
                self._start_worker(worker, "开始从文本生成测试点...")

        except Exception as e:
            self.append_log(f"启动测试点生成失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

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
        """导出测试点JSON到XMind"""
        try:
            json_path = self.configTab.pointJsonPathInput.text()
            # 检查路径：空则确认是否使用默认配置路径
            if not self._confirm_default_path(json_path, "测试点JSON路径"):
                return
            if not json_path or not os.path.exists(json_path):
                QMessageBox.warning(self.main_window, "警告", "测试点JSON文件不存在，请先生成测试点")
                return

            output_dir = self._get_output_dir()
            output_xmind = os.path.join(output_dir, "测试点.xmind")

            worker = ExportTestPointWorker(json_path, output_xmind)
            self._start_worker(worker, f"导出测试点XMind：{output_xmind}")

        except Exception as e:
            self.append_log(f"启动导出失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    # ==================== 测试用例业务逻辑 ====================

    def generate_test_cases(self):
        """从测试点XMind文件生成测试用例XMind（或从文本走全链路）"""
        try:
            output_dir = self._get_output_dir()

            if self.testCaseTab.xmindRadio.isChecked():
                # 检查模板路径：空则确认是否使用默认配置路径
                template_path = self.testCaseTab.templateInput.text()
                if not self._confirm_default_path(template_path, "模板文件路径"):
                    return
                # ---- XMind导入模式：测试点XMind → AI → 测试用例XMind ----
                xmind_path = self.testCaseTab.xmindPathInput.text()
                if not xmind_path:
                    QMessageBox.warning(self.main_window, "警告", "请先选择测试点XMind文件")
                    return
                if not os.path.exists(xmind_path):
                    QMessageBox.warning(self.main_window, "警告", f"文件不存在：{xmind_path}")
                    return
                worker = GenerateTestCaseWorker(
                    xmind_path=xmind_path,
                    output_dir=output_dir
                )
                self._start_worker(worker, f"开始从XMind生成测试用例：{xmind_path}")
            else:
                # ---- 文本输入模式：文本 → 全链路 → XLSX ----
                # 检查输出路径：空则确认是否使用默认配置路径
                output_path = self.testCaseTab.outputPathInput.text()
                if not self._confirm_default_path(output_path, "输出路径"):
                    return
                text = self.testCaseTab.testCaseTextInput.toPlainText()
                if not text:
                    QMessageBox.warning(self.main_window, "警告", "请输入测试用例内容")
                    return
                out_dir = self.testCaseTab.outputPathInput.text() or output_dir
                worker = GenerateTextCaseWorker(text, out_dir)
                self._start_worker(worker, "开始从文本生成测试用例...")

        except Exception as e:
            self.append_log(f"启动测试用例生成失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def generate_text_cases(self):
        """测试点文本输入 → 一键生成测试用例XLSX（全链路）"""
        try:
            text = self.testCaseTab.testCaseTextInput.toPlainText()
            if not text:
                QMessageBox.warning(self.main_window, "警告", "请在文本输入区域输入需求描述")
                return

            output_dir = self.testCaseTab.outputPathInput.text() or self._get_output_dir()
            worker = GenerateTextCaseWorker(text, output_dir)
            self._start_worker(worker, "开始从文本一键生成测试用例...")

        except Exception as e:
            self.append_log(f"启动文本生成用例失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def clear_test_cases(self):
        """清空测试用例输入"""
        self.testCaseTab.xmindPathInput.clear()
        self.testCaseTab.testCaseXmindPathInput.clear()
        self.testCaseTab.templateInput.clear()
        self.testCaseTab.outputPathInput.clear()
        self.testCaseTab.testCaseTextInput.clear()
        self.append_log("已清空测试用例输入")

    def export_to_xmind(self):
        """测试用例JSON转XMind导出
        数据流：caseJsonPathInput(测试用例JSON) → TestcaseJsonToXmind → caseXmindPathInput(XMind输出)
        """
        try:
            # 读取测试用例JSON路径（配置页 → 测试用例配置 → 输出JSON路径）
            json_path = self.configTab.caseJsonPathInput.text()
            # 检查路径：空则确认是否使用默认配置路径
            if not self._confirm_default_path(json_path, "测试用例JSON路径"):
                return
            if not json_path or not os.path.exists(json_path):
                # 尝试使用默认路径
                json_path = os.path.join(self._get_output_dir(), "测试用例_output.json")
                if not os.path.exists(json_path):
                    QMessageBox.warning(self.main_window, "警告",
                                        "测试用例JSON文件不存在，请先生成测试用例或配置正确的JSON路径")
                    return

            # XMind输出路径（配置页 → 测试用例配置 → XMind保存路径）
            output_xmind = self.configTab.caseXmindPathInput.text()
            if not output_xmind:
                output_xmind = os.path.join(self._get_output_dir(), "测试用例.xmind")

            worker = ExportTestCaseXmindWorker(json_path, output_xmind)
            self._start_worker(worker, f"导出测试用例XMind：{json_path} → {output_xmind}")

        except Exception as e:
            self.append_log(f"启动XMind导出失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def export_to_xlsx(self):
        """XMind转Excel导出
        数据流：caseXmindPathInput(XMind文件) → TestPointXmindToTestcaseXlsx → 输出XLSX
        """
        try:
            # 读取XMind路径（配置页 → 测试用例配置 → XMind保存路径）
            xmind_path = self.configTab.caseXmindPathInput.text()
            if not xmind_path:
                # 尝试使用默认路径
                xmind_path = os.path.join(self._get_output_dir(), "测试用例.xmind")
            if not os.path.exists(xmind_path):
                QMessageBox.warning(self.main_window, "警告",
                                    f"XMind文件不存在：{xmind_path}\n请先选择测试用例XMind文件")
                return

            # Excel输出路径（测试用例页面 → outputPathInput）
            output_xlsx = self.testCaseTab.outputPathInput.text()
            if not output_xlsx:
                output_xlsx = os.path.join(self._get_output_dir(), "测试用例.xlsx")
            # 确保输出扩展名为xlsx
            if not output_xlsx.endswith('.xlsx'):
                output_xlsx = os.path.join(output_xlsx, "测试用例.xlsx")

            worker = XmindToXlsxWorker(xmind_path, output_xlsx)
            self._start_worker(worker, f"导出Excel：{xmind_path} → {output_xlsx}")

        except Exception as e:
            self.append_log(f"启动Excel导出失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def text_to_testcaseXmind(self):
        """需求文案一键生成测试用例XMind文件
        数据流：testCaseTextInput(文本) → interfaceAIAnyFlieToXmind → outputPathInput(输出目录)
        """
        try:
            # 检查输出路径：空则确认是否使用默认配置路径
            output_path = self.testCaseTab.outputPathInput.text()
            if not self._confirm_default_path(output_path, "输出路径"):
                return
            text = self.testCaseTab.testCaseTextInput.toPlainText()
            if not text:
                QMessageBox.warning(self.main_window, "警告", "请输入需求描述文本")
                return

            output_dir = self.testCaseTab.outputPathInput.text() or self._get_output_dir()
            worker = TextToXmindWorker(text, output_dir)
            self._start_worker(worker, "开始从文本一键生成测试用例XMind...")

        except Exception as e:
            self.append_log(f"启动文本生成测试用例XMind失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def export_xmind_to_xlsx(self):
        """测试用例XMind转Excel导出（使用 interfaceAITestCaseXlsx 转换器）
        数据流：testCaseXmindPathInput(测试用例XMind) → interfaceAITestCaseXlsx → outputPathInput(输出XLSX)
        其他中间路径由配置文件处理
        """
        try:
            # 读取测试用例XMind路径（测试用例页面 → testCaseXmindPathInput）
            xmind_path = self.testCaseTab.testCaseXmindPathInput.text()
            # 检查路径：空则确认是否使用默认配置路径
            if not self._confirm_default_path(xmind_path, "测试用例XMind路径"):
                return
            if not xmind_path:
                xmind_path = os.path.join(self._get_output_dir(), "测试用例.xmind")
            if not os.path.exists(xmind_path):
                QMessageBox.warning(self.main_window, "警告",
                                    f"XMind文件不存在：{xmind_path}\n请先选择测试用例XMind文件")
                return

            # Excel输出路径（测试用例页面 → outputPathInput）
            output_xlsx = self.testCaseTab.outputPathInput.text()
            if not output_xlsx:
                output_xlsx = os.path.join(self._get_output_dir(), "测试用例.xlsx")
            if not output_xlsx.endswith('.xlsx'):
                output_xlsx = os.path.join(output_xlsx, "测试用例.xlsx")

            worker = TestcaseXmindToXlsxWorker(
                xmind_path=xmind_path,
                output_xlsx=output_xlsx
            )
            self._start_worker(worker, f"导出Excel：{xmind_path} → {output_xlsx}")

        except Exception as e:
            self.append_log(f"启动Excel导出失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    # ==================== 其他功能业务逻辑 ====================

    def convert_xmind_to_xlsx(self):
        """转换XMind到Excel（其他功能页面）"""
        try:
            input_path = self.otherTab.inputXmindInput.text()
            output_path = self.otherTab.outputXlsxInput.text()

            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择输入的XMind文件")
                return
            if not os.path.exists(input_path):
                QMessageBox.warning(self.main_window, "警告", f"XMind文件不存在：{input_path}")
                return
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return

            worker = XmindToXlsxWorker(input_path, output_path)
            self._start_worker(worker, f"转换中：{input_path} -> {output_path}")

        except Exception as e:
            self.append_log(f"启动转换失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))

    def convert_testpoint_to_xlsx(self):
        """转换测试点XMind到Excel（其他功能页面）"""
        try:
            input_path = self.otherTab.testPointInput.text()
            output_path = self.otherTab.testPointOutput.text()

            if not input_path:
                QMessageBox.warning(self.main_window, "警告", "请选择测试点XMind文件")
                return
            if not os.path.exists(input_path):
                QMessageBox.warning(self.main_window, "警告", f"XMind文件不存在：{input_path}")
                return
            if not output_path:
                QMessageBox.warning(self.main_window, "警告", "请配置输出的Excel路径")
                return

            worker = XmindToXlsxWorker(input_path, output_path)
            self._start_worker(worker, f"转换测试点：{input_path} -> {output_path}")

        except Exception as e:
            self.append_log(f"启动转换失败：{str(e)}")
            QMessageBox.critical(self.main_window, "错误", str(e))
