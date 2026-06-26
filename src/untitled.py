# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QTabWidget, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton,
    QTextEdit, QGroupBox, QComboBox, QCheckBox, QSpinBox,
    QHBoxLayout, QFileDialog, QPlainTextEdit, QSplitter, QStyleFactory,
    QMainWindow, QRadioButton, QScrollArea)

class Ui_ConfigTab(QWidget):
    """配置项页面"""
    def setupUi(self, parent):
        # 创建主布局
        mainLayout = QVBoxLayout(parent)
        
        # 创建滚动区域
        self.scrollArea = QScrollArea(parent)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        
        # 创建滚动内容的容器widget
        scrollContent = QWidget()
        scrollLayout = QVBoxLayout(scrollContent)
        
        # API配置分组
        apiGroup = QGroupBox("API配置")
        apiLayout = QVBoxLayout()
        
        self.apiKeyLabel = QLabel("DeepSeek API Key:")
        self.apiKeyInput = QLineEdit()
        self.apiKeyInput.setEchoMode(QLineEdit.Password)
        apiLayout.addWidget(self.apiKeyLabel)
        apiLayout.addWidget(self.apiKeyInput)
        
        self.modelLabel = QLabel("模型选择:")
        self.modelCombo = QComboBox()
        self.modelCombo.addItems(["deepseek-chat", "chatgpt","Gemining3.0"])
        apiLayout.addWidget(self.modelLabel)
        apiLayout.addWidget(self.modelCombo)
        
        apiGroup.setLayout(apiLayout)
        scrollLayout.addWidget(apiGroup)
        
        # 测试点路径配置分组
        pointPathGroup = QGroupBox("测试点配置")
        pointPathLayout = QVBoxLayout()
        
        self.pointJsonPathLabel = QLabel("输出JSON路径:")
        self.pointJsonPathInput = QLineEdit()
        self.pointJsonPathBrowseBtn = QPushButton("浏览")
        pointJsonPathLayout = QHBoxLayout()
        pointJsonPathLayout.addWidget(self.pointJsonPathInput)
        pointJsonPathLayout.addWidget(self.pointJsonPathBrowseBtn)
        pointPathLayout.addWidget(self.pointJsonPathLabel)
        pointPathLayout.addLayout(pointJsonPathLayout)
        
        self.pointTemplatePathLabel = QLabel("模板路径:")
        self.pointTemplatePathInput = QLineEdit()
        self.pointTemplatePathBrowseBtn = QPushButton("浏览")
        pointTemplatePathLayout = QHBoxLayout()
        pointTemplatePathLayout.addWidget(self.pointTemplatePathInput)
        pointTemplatePathLayout.addWidget(self.pointTemplatePathBrowseBtn)
        pointPathLayout.addWidget(self.pointTemplatePathLabel)
        pointPathLayout.addLayout(pointTemplatePathLayout)
        
        self.pointImgPathLabel = QLabel("图片路径:")
        self.pointImgPathInput = QLineEdit()
        self.pointImgPathBrowseBtn = QPushButton("浏览")
        pointImgPathLayout = QHBoxLayout()
        pointImgPathLayout.addWidget(self.pointImgPathInput)
        pointImgPathLayout.addWidget(self.pointImgPathBrowseBtn)
        pointPathLayout.addWidget(self.pointImgPathLabel)
        pointPathLayout.addLayout(pointImgPathLayout)
        
        pointPathGroup.setLayout(pointPathLayout)
        scrollLayout.addWidget(pointPathGroup)
        
        # 测试用例路径配置分组
        casePathGroup = QGroupBox("测试用例配置")
        casePathLayout = QVBoxLayout()

        self.caseJsonPathLabel = QLabel("输出JSON路径:")
        self.caseJsonPathInput = QLineEdit()
        self.caseJsonPathBrowseBtn = QPushButton("浏览")
        caseJsonPathLayout = QHBoxLayout()
        caseJsonPathLayout.addWidget(self.caseJsonPathInput)
        caseJsonPathLayout.addWidget(self.caseJsonPathBrowseBtn)
        casePathLayout.addWidget(self.caseJsonPathLabel)
        casePathLayout.addLayout(caseJsonPathLayout)

        self.caseXmindPathLabel = QLabel("XMind保存路径:")
        self.caseXmindPathInput = QLineEdit()
        self.caseXmindPathBrowseBtn = QPushButton("浏览")
        caseXmindPathLayout = QHBoxLayout()
        caseXmindPathLayout.addWidget(self.caseXmindPathInput)
        caseXmindPathLayout.addWidget(self.caseXmindPathBrowseBtn)
        casePathLayout.addWidget(self.caseXmindPathLabel)
        casePathLayout.addLayout(caseXmindPathLayout)

        self.caseExeclPathLabel = QLabel("Excel保存路径:")
        self.caseExeclPathInput = QLineEdit()
        self.caseExeclPathBrowseBtn = QPushButton("浏览")
        caseExeclPathLayout = QHBoxLayout()
        caseExeclPathLayout.addWidget(self.caseExeclPathInput)
        caseExeclPathLayout.addWidget(self.caseExeclPathBrowseBtn)
        casePathLayout.addWidget(self.caseExeclPathLabel)
        casePathLayout.addLayout(caseExeclPathLayout)

        casePathGroup.setLayout(casePathLayout)
        scrollLayout.addWidget(casePathGroup)

        # 其他功能路径配置
        otherPathGroup = QGroupBox("其他功能配置")
        otherPathLayout = QVBoxLayout()

        self.otherJsonPathLabel = QLabel("输出JSON路径:")
        self.otherJsonPathInput = QLineEdit()
        self.otherJsonPathBrowseBtn = QPushButton("浏览")
        otherJsonPathLayout = QHBoxLayout()
        otherJsonPathLayout.addWidget(self.otherJsonPathInput)
        otherJsonPathLayout.addWidget(self.otherJsonPathBrowseBtn)
        otherPathLayout.addWidget(self.otherJsonPathLabel)
        otherPathLayout.addLayout(otherJsonPathLayout)

        self.otherTemplatePathLabel = QLabel("模板路径:")
        self.otherTemplatePathInput = QLineEdit()
        self.otherTemplatePathBrowseBtn = QPushButton("浏览")
        otherTemplatePathLayout = QHBoxLayout()
        otherTemplatePathLayout.addWidget(self.otherTemplatePathInput)
        otherTemplatePathLayout.addWidget(self.otherTemplatePathBrowseBtn)
        otherPathLayout.addWidget(self.otherTemplatePathLabel)
        otherPathLayout.addLayout(otherTemplatePathLayout)

        self.otherImgPathLabel = QLabel("图片路径:")
        self.otherImgPathInput = QLineEdit()
        self.otherImgPathBrowseBtn = QPushButton("浏览")
        otherImgPathLayout = QHBoxLayout()
        otherImgPathLayout.addWidget(self.otherImgPathInput)
        otherImgPathLayout.addWidget(self.otherImgPathBrowseBtn)
        otherPathLayout.addWidget(self.otherImgPathLabel)
        otherPathLayout.addLayout(otherImgPathLayout)

        otherPathGroup.setLayout(otherPathLayout)
        scrollLayout.addWidget(otherPathGroup)

        # 操作按钮
        buttonLayout = QHBoxLayout()
        self.saveBtn = QPushButton("保存配置")
        self.loadBtn = QPushButton("初始化")
        buttonLayout.addWidget(self.saveBtn)
        buttonLayout.addWidget(self.loadBtn)
        buttonLayout.addStretch()
        scrollLayout.addLayout(buttonLayout)

        scrollLayout.addStretch()
        
        # 设置滚动内容
        self.scrollArea.setWidget(scrollContent)
        mainLayout.addWidget(self.scrollArea)




class Ui_TestPointTab(QWidget):
    """测试点功能页面"""
    def setupUi(self, parent):
        layout = QVBoxLayout(parent)
        
        # 输入方式选择
        inputGroup = QGroupBox("输入方式")
        inputLayout = QHBoxLayout()
        
        self.imageRadio = QRadioButton("图片识别")
        self.tp_textRadio = QRadioButton("文本输入")
        self.imageRadio.setChecked(True)
        inputLayout.addWidget(self.imageRadio)
        inputLayout.addWidget(self.tp_textRadio)
        inputLayout.addStretch()
        inputGroup.setLayout(inputLayout)
        layout.addWidget(inputGroup)
        
        # 图片输入区域
        self.imageGroup = QGroupBox("图片输入")
        imageLayout = QVBoxLayout()
        
        self.imagePathLabel = QLabel("图片路径:")
        self.imagePathInput = QLineEdit()
        self.imageBrowseBtn = QPushButton("选择图片")
        imagePathLayout = QHBoxLayout()
        imagePathLayout.addWidget(self.imagePathInput)
        imagePathLayout.addWidget(self.imageBrowseBtn)
        imageLayout.addLayout(imagePathLayout)
        
        self.imagePreviewLabel = QLabel("预览:")
        self.imagePreviewArea = QLabel("暂无预览")
        self.imagePreviewArea.setObjectName("imagePreviewArea")
        self.imagePreviewArea.setMinimumSize(400, 200)
        self.imagePreviewArea.setAlignment(Qt.AlignCenter)
        imageLayout.addWidget(self.imagePreviewLabel)
        imageLayout.addWidget(self.imagePreviewArea)
        
        self.imageGroup.setLayout(imageLayout)
        layout.addWidget(self.imageGroup)
        
        # 文本输入区域
        self.tp_textGroup = QGroupBox("文本输入")
        tp_textLayout = QVBoxLayout()
        
        self.testPointTextInput = QTextEdit()
        tp_textLayout.addWidget(self.testPointTextInput)
        
        self.tp_textGroup.setLayout(tp_textLayout)
        self.tp_textGroup.setVisible(False)
        layout.addWidget(self.tp_textGroup)
        
        # 选项设置
        optionGroup = QGroupBox("生成选项")
        optionLayout = QVBoxLayout()
        
        self.strictCheck = QCheckBox("严格模式")
        self.detailedCheck = QCheckBox("详细输出")
        optionLayout.addWidget(self.strictCheck)
        optionLayout.addWidget(self.detailedCheck)
        
        optionGroup.setLayout(optionLayout)
        layout.addWidget(optionGroup)
        
        # 操作按钮
        buttonLayout = QHBoxLayout()
        self.tp_generateBtn = QPushButton("生成测试点")
        self.tp_clearBtn = QPushButton("清空")
        self.exportBtn = QPushButton("导出XMind")
        buttonLayout.addWidget(self.tp_generateBtn)
        buttonLayout.addWidget(self.tp_clearBtn)
        buttonLayout.addWidget(self.exportBtn)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)
        
        layout.addStretch()


class Ui_TestCaseTab(QWidget):
    """测试用例页面"""
    def setupUi(self, parent):
        layout = QVBoxLayout(parent)
        
        # 输入方式选择
        inputGroup = QGroupBox("输入方式")
        inputLayout = QHBoxLayout()
        
        self.xmindRadio = QRadioButton("XMind导入")
        self.tc_textRadio = QRadioButton("文本输入")
        self.xmindRadio.setChecked(True)
        inputLayout.addWidget(self.xmindRadio)
        inputLayout.addWidget(self.tc_textRadio)
        inputLayout.addStretch()
        inputGroup.setLayout(inputLayout)
        layout.addWidget(inputGroup)
        
        # XMind输入区域
        self.xmindGroup = QGroupBox("XMind输入")
        xmindLayout = QVBoxLayout()
        
        self.xmindPathLabel = QLabel("测试点XMind路径:")
        self.xmindPathInput = QLineEdit()
        self.xmindBrowseBtn = QPushButton("选择文件")
        xmindPathLayout = QHBoxLayout()
        xmindPathLayout.addWidget(self.xmindPathInput)
        xmindPathLayout.addWidget(self.xmindBrowseBtn)
        xmindLayout.addLayout(xmindPathLayout)
        
        self.templateLabel = QLabel("模板文件:")
        self.templateInput = QLineEdit()
        self.templateBrowseBtn = QPushButton("选择模板文件")
        templateLayout = QHBoxLayout()
        templateLayout.addWidget(self.templateInput)
        templateLayout.addWidget(self.templateBrowseBtn)
        xmindLayout.addLayout(templateLayout)
        
        self.xmindGroup.setLayout(xmindLayout)
        layout.addWidget(self.xmindGroup)
        
        # 文本输入区域
        self.tc_textGroup = QGroupBox("文本输入")
        tc_textLayout = QVBoxLayout()
        
        self.testCaseTextInput = QTextEdit()
        tc_textLayout.addWidget(self.testCaseTextInput)
        
        self.tc_textGroup.setLayout(tc_textLayout)
        self.tc_textGroup.setVisible(False)
        layout.addWidget(self.tc_textGroup)
        
        # 输出设置
        outputGroup = QGroupBox("输出设置")
        outputLayout = QVBoxLayout()
        
        self.outputPathLabel = QLabel("输出路径:")
        self.outputPathInput = QLineEdit()
        self.outputBrowseBtn = QPushButton("浏览")
        outputPathLayout = QHBoxLayout()
        outputPathLayout.addWidget(self.outputPathInput)
        outputPathLayout.addWidget(self.outputBrowseBtn)
        outputLayout.addWidget(self.outputPathLabel)
        outputLayout.addLayout(outputPathLayout)
        
        outputGroup.setLayout(outputLayout)
        layout.addWidget(outputGroup)
        
        # 操作按钮
        buttonLayout = QHBoxLayout()
        self.tc_text_generateBtn = QPushButton("测试点文本生成测试用例XMind")
        self.tc_generateBtn = QPushButton("测试点XMind生成测试用例")
        self.tc_clearBtn = QPushButton("清空")
        self.exportXmindBtn = QPushButton("测试用例json转XMind")
        self.exportXlsxBtn = QPushButton("测试用例XMind转Excel")
        buttonLayout.addWidget(self.tc_text_generateBtn)
        buttonLayout.addWidget(self.tc_generateBtn)
        buttonLayout.addWidget(self.exportXmindBtn)
        buttonLayout.addWidget(self.exportXlsxBtn)
        buttonLayout.addWidget(self.tc_clearBtn)
        buttonLayout.addStretch()
        layout.addLayout(buttonLayout)
        
        layout.addStretch()


class Ui_OtherTab(QWidget):
    """其他功能页面"""
    def setupUi(self, parent):
        layout = QVBoxLayout(parent)
        
        # 格式转换工具分组
        convertGroup = QGroupBox("格式转换工具")
        convertLayout = QVBoxLayout()
        
        # XMind转XLSX
        xmindToXlsxGroup = QGroupBox("XMind转XLSX")
        xmindToXlsxLayout = QVBoxLayout()
        
        self.inputXmindLabel = QLabel("输入XMind:")
        self.inputXmindInput = QLineEdit()
        self.inputXmindBrowse = QPushButton("选择文件")
        inputXmindLayout = QHBoxLayout()
        inputXmindLayout.addWidget(self.inputXmindInput)
        inputXmindLayout.addWidget(self.inputXmindBrowse)
        xmindToXlsxLayout.addLayout(inputXmindLayout)
        
        self.outputXlsxLabel = QLabel("输出Excel:")
        self.outputXlsxInput = QLineEdit()
        self.outputXlsxBrowse = QPushButton("浏览")
        outputXlsxLayout = QHBoxLayout()
        outputXlsxLayout.addWidget(self.outputXlsxInput)
        outputXlsxLayout.addWidget(self.outputXlsxBrowse)
        xmindToXlsxLayout.addLayout(outputXlsxLayout)
        
        self.xmindToXlsxBtn = QPushButton("开始转换")
        xmindToXlsxLayout.addWidget(self.xmindToXlsxBtn)
        
        xmindToXlsxGroup.setLayout(xmindToXlsxLayout)
        convertLayout.addWidget(xmindToXlsxGroup)
        
        # 测试点转XLSX
        testPointToXlsxGroup = QGroupBox("测试点XMind转XLSX")
        testPointToXlsxLayout = QVBoxLayout()
        
        self.testPointInputLabel = QLabel("测试点XMind:")
        self.testPointInput = QLineEdit()
        self.testPointBrowse = QPushButton("选择文件")
        testPointLayout = QHBoxLayout()
        testPointLayout.addWidget(self.testPointInput)
        testPointLayout.addWidget(self.testPointBrowse)
        testPointToXlsxLayout.addLayout(testPointLayout)
        
        self.testPointOutputLabel = QLabel("输出Excel:")
        self.testPointOutput = QLineEdit()
        self.testPointOutputBrowse = QPushButton("浏览")
        testPointOutputLayout = QHBoxLayout()
        testPointOutputLayout.addWidget(self.testPointOutput)
        testPointOutputLayout.addWidget(self.testPointOutputBrowse)
        testPointToXlsxLayout.addLayout(testPointOutputLayout)
        
        self.testPointToXlsxBtn = QPushButton("开始转换")
        testPointToXlsxLayout.addWidget(self.testPointToXlsxBtn)
        
        testPointToXlsxGroup.setLayout(testPointToXlsxLayout)
        convertLayout.addWidget(testPointToXlsxGroup)
        
        convertGroup.setLayout(convertLayout)
        layout.addWidget(convertGroup)
        
        # 日志输出区域
        logGroup = QGroupBox("执行日志")
        logLayout = QVBoxLayout()
        
        self.logText = QPlainTextEdit()
        self.logText.setObjectName("logText")
        self.logText.setReadOnly(True)
        logLayout.addWidget(self.logText)
        
        self.clearLogBtn = QPushButton("清空日志")
        logLayout.addWidget(self.clearLogBtn)
        
        logGroup.setLayout(logLayout)
        layout.addWidget(logGroup)
        
        layout.addStretch()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1200, 700)
        
        # 创建菜单栏
        self.menubar = MainWindow.menuBar()
        self.fileMenu = self.menubar.addMenu("文件")
        self.actionsave = QAction(MainWindow)
        self.actionsave.setObjectName(u"actionsave")
        self.fileMenu.addAction(self.actionsave)
        
        # 创建主窗口部件
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # 创建主TabWidget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1200, 650))
        self.tabWidget.setTabsClosable(False)
        
        # 创建4个Tab页面 - 存储Tab实例供Controller使用
        self.configTab = Ui_ConfigTab()
        self.configTabWidget = QWidget()
        self.configTab.setupUi(self.configTabWidget)
        
        self.testPointTab = Ui_TestPointTab()
        self.testPointWidget = QWidget()
        self.testPointTab.setupUi(self.testPointWidget)
        
        self.testCaseTab = Ui_TestCaseTab()
        self.testCaseWidget = QWidget()
        self.testCaseTab.setupUi(self.testCaseWidget)
        
        self.otherTab = Ui_OtherTab()
        self.otherWidget = QWidget()
        self.otherTab.setupUi(self.otherWidget)
        
        # 添加到TabWidget
        self.tabWidget.addTab(self.configTabWidget, "配置项")
        self.tabWidget.addTab(self.testPointWidget, "测试点功能")
        self.tabWidget.addTab(self.testCaseWidget, "测试用例")
        self.tabWidget.addTab(self.otherWidget, "其他功能")
        
        # 设置中心部件
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"AI测试用例自动生成工具", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configTabWidget), QCoreApplication.translate("MainWindow", u"配置项", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.testPointWidget), QCoreApplication.translate("MainWindow", u"测试点功能", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.testCaseWidget), QCoreApplication.translate("MainWindow", u"测试用例", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.otherWidget), QCoreApplication.translate("MainWindow", u"其他功能", None))
        # retranslateUi


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
