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
        self.mainLayout = QVBoxLayout(parent)
        
        # 创建滚动区域
        self.scrollArea = QScrollArea(parent)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        
        # 创建滚动内容的容器widget
        self.scrollContent = QWidget()
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        
        # API配置分组
        self.apiGroup = QGroupBox("API配置")
        self.apiLayout = QVBoxLayout()
        
        self.apiKeyLabel = QLabel("DeepSeek API Key:")
        self.apiKeyInput = QLineEdit()
        self.apiKeyInput.setEchoMode(QLineEdit.Password)
        self.apiLayout.addWidget(self.apiKeyLabel)
        self.apiLayout.addWidget(self.apiKeyInput)
        
        self.modelLabel = QLabel("模型选择:")
        self.modelCombo = QComboBox()
        self.modelCombo.addItems(["deepseek-chat", "chatgpt","Gemining3.0"])
        self.apiLayout.addWidget(self.modelLabel)
        self.apiLayout.addWidget(self.modelCombo)
        
        self.apiGroup.setLayout(self.apiLayout)
        self.scrollLayout.addWidget(self.apiGroup)
        
        # 测试点路径配置分组
        self.pointPathGroup = QGroupBox("测试点配置")
        self.pointPathLayout = QVBoxLayout()
        
        self.pointJsonPathLabel = QLabel("输出JSON路径:")
        self.pointJsonPathInput = QLineEdit()
        self.pointJsonPathBrowseBtn = QPushButton("浏览")
        pointJsonPathLayout = QHBoxLayout()
        pointJsonPathLayout.addWidget(self.pointJsonPathInput)
        pointJsonPathLayout.addWidget(self.pointJsonPathBrowseBtn)
        self.pointPathLayout.addWidget(self.pointJsonPathLabel)
        self.pointPathLayout.addLayout(pointJsonPathLayout)
        
        self.pointTemplatePathLabel = QLabel("模板路径:")
        self.pointTemplatePathInput = QLineEdit()
        self.pointTemplatePathBrowseBtn = QPushButton("浏览")
        pointTemplatePathLayout = QHBoxLayout()
        pointTemplatePathLayout.addWidget(self.pointTemplatePathInput)
        pointTemplatePathLayout.addWidget(self.pointTemplatePathBrowseBtn)
        self.pointPathLayout.addWidget(self.pointTemplatePathLabel)
        self.pointPathLayout.addLayout(pointTemplatePathLayout)
        
        self.pointImgPathLabel = QLabel("图片路径:")
        self.pointImgPathInput = QLineEdit()
        self.pointImgPathBrowseBtn = QPushButton("浏览")
        pointImgPathLayout = QHBoxLayout()
        pointImgPathLayout.addWidget(self.pointImgPathInput)
        pointImgPathLayout.addWidget(self.pointImgPathBrowseBtn)
        self.pointPathLayout.addWidget(self.pointImgPathLabel)
        self.pointPathLayout.addLayout(pointImgPathLayout)
        
        self.pointPathGroup.setLayout(self.pointPathLayout)
        self.scrollLayout.addWidget(self.pointPathGroup)
        
        # 测试用例路径配置分组
        self.casePathGroup = QGroupBox("测试用例配置")
        self.casePathLayout = QVBoxLayout()

        self.caseJsonPathLabel = QLabel("输出JSON路径:")
        self.caseJsonPathInput = QLineEdit()
        self.caseJsonPathBrowseBtn = QPushButton("浏览")
        caseJsonPathLayout = QHBoxLayout()
        caseJsonPathLayout.addWidget(self.caseJsonPathInput)
        caseJsonPathLayout.addWidget(self.caseJsonPathBrowseBtn)
        self.casePathLayout.addWidget(self.caseJsonPathLabel)
        self.casePathLayout.addLayout(caseJsonPathLayout)

        self.caseXmindPathLabel = QLabel("XMind保存路径:")
        self.caseXmindPathInput = QLineEdit()
        self.caseXmindPathBrowseBtn = QPushButton("浏览")
        caseXmindPathLayout = QHBoxLayout()
        caseXmindPathLayout.addWidget(self.caseXmindPathInput)
        caseXmindPathLayout.addWidget(self.caseXmindPathBrowseBtn)
        self.casePathLayout.addWidget(self.caseXmindPathLabel)
        self.casePathLayout.addLayout(caseXmindPathLayout)

        self.caseExeclPathLabel = QLabel("Excel保存路径:")
        self.caseExeclPathInput = QLineEdit()
        self.caseExeclPathBrowseBtn = QPushButton("浏览")
        caseExeclPathLayout = QHBoxLayout()
        caseExeclPathLayout.addWidget(self.caseExeclPathInput)
        caseExeclPathLayout.addWidget(self.caseExeclPathBrowseBtn)
        self.casePathLayout.addWidget(self.caseExeclPathLabel)
        self.casePathLayout.addLayout(caseExeclPathLayout)

        self.casePathGroup.setLayout(self.casePathLayout)
        self.scrollLayout.addWidget(self.casePathGroup)

        # 其他功能路径配置
        self.otherPathGroup = QGroupBox("其他功能配置")
        self.otherPathLayout = QVBoxLayout()

        self.otherJsonPathLabel = QLabel("输出JSON路径:")
        self.otherJsonPathInput = QLineEdit()
        self.otherJsonPathBrowseBtn = QPushButton("浏览")
        otherJsonPathLayout = QHBoxLayout()
        otherJsonPathLayout.addWidget(self.otherJsonPathInput)
        otherJsonPathLayout.addWidget(self.otherJsonPathBrowseBtn)
        self.otherPathLayout.addWidget(self.otherJsonPathLabel)
        self.otherPathLayout.addLayout(otherJsonPathLayout)

        self.otherTemplatePathLabel = QLabel("模板路径:")
        self.otherTemplatePathInput = QLineEdit()
        self.otherTemplatePathBrowseBtn = QPushButton("浏览")
        otherTemplatePathLayout = QHBoxLayout()
        otherTemplatePathLayout.addWidget(self.otherTemplatePathInput)
        otherTemplatePathLayout.addWidget(self.otherTemplatePathBrowseBtn)
        self.otherPathLayout.addWidget(self.otherTemplatePathLabel)
        self.otherPathLayout.addLayout(otherTemplatePathLayout)

        self.otherImgPathLabel = QLabel("图片路径:")
        self.otherImgPathInput = QLineEdit()
        self.otherImgPathBrowseBtn = QPushButton("浏览")
        otherImgPathLayout = QHBoxLayout()
        otherImgPathLayout.addWidget(self.otherImgPathInput)
        otherImgPathLayout.addWidget(self.otherImgPathBrowseBtn)
        self.otherPathLayout.addWidget(self.otherImgPathLabel)
        self.otherPathLayout.addLayout(otherImgPathLayout)

        self.otherPathGroup.setLayout(self.otherPathLayout)
        self.scrollLayout.addWidget(self.otherPathGroup)

        # 操作按钮
        self.buttonLayout = QHBoxLayout()
        self.saveBtn = QPushButton("保存配置")
        self.loadBtn = QPushButton("初始化")
        self.buttonLayout.addWidget(self.saveBtn)
        self.buttonLayout.addWidget(self.loadBtn)
        self.buttonLayout.addStretch()
        self.scrollLayout.addLayout(self.buttonLayout)

        self.scrollLayout.addStretch()
        
        # 设置滚动内容
        self.scrollArea.setWidget(self.scrollContent)
        self.mainLayout.addWidget(self.scrollArea)




class Ui_TestPointTab(QWidget):
    """测试点功能页面"""
    def setupUi(self, parent):
        self.layout = QVBoxLayout(parent)
        
        # 输入方式选择
        self.inputGroup = QGroupBox("输入方式")
        self.inputLayout = QHBoxLayout()
        
        self.imageRadio = QRadioButton("图片识别")
        self.textRadio = QRadioButton("文本输入")
        self.imageRadio.setChecked(True)
        self.inputLayout.addWidget(self.imageRadio)
        self.inputLayout.addWidget(self.textRadio)
        self.inputLayout.addStretch()
        self.inputGroup.setLayout(self.inputLayout)
        self.layout.addWidget(self.inputGroup)
        
        # 图片输入区域
        self.imageGroup = QGroupBox("图片输入")
        self.imageLayout = QVBoxLayout()
        
        self.imagePathLabel = QLabel("图片路径:")
        self.imagePathInput = QLineEdit()
        self.imageBrowseBtn = QPushButton("选择图片")
        imagePathLayout = QHBoxLayout()
        imagePathLayout.addWidget(self.imagePathInput)
        imagePathLayout.addWidget(self.imageBrowseBtn)
        self.imageLayout.addLayout(imagePathLayout)
        
        self.imagePreviewLabel = QLabel("预览:")
        self.imagePreviewArea = QLabel("暂无预览")
        self.imagePreviewArea.setStyleSheet("border: 1px solid gray; background-color: white;")
        self.imagePreviewArea.setMinimumSize(400, 200)
        self.imagePreviewArea.setAlignment(Qt.AlignCenter)
        self.imageLayout.addWidget(self.imagePreviewLabel)
        self.imageLayout.addWidget(self.imagePreviewArea)
        
        self.imageGroup.setLayout(self.imageLayout)
        self.layout.addWidget(self.imageGroup)
        
        # 文本输入区域
        self.textGroup = QGroupBox("文本输入")
        self.textLayout = QVBoxLayout()
        
        self.testPointTextInput = QTextEdit()
        self.textLayout.addWidget(self.testPointTextInput)
        
        self.textGroup.setLayout(self.textLayout)
        self.textGroup.setVisible(False)
        self.layout.addWidget(self.textGroup)
        
        # 选项设置
        self.optionGroup = QGroupBox("生成选项")
        self.optionLayout = QVBoxLayout()
        
        self.strictCheck = QCheckBox("严格模式")
        self.detailedCheck = QCheckBox("详细输出")
        self.optionLayout.addWidget(self.strictCheck)
        self.optionLayout.addWidget(self.detailedCheck)
        
        self.optionGroup.setLayout(self.optionLayout)
        self.layout.addWidget(self.optionGroup)
        
        # 操作按钮
        self.buttonLayout = QHBoxLayout()
        self.generateBtn = QPushButton("生成测试点")
        self.clearBtn = QPushButton("清空")
        self.exportBtn = QPushButton("导出XMind")
        self.buttonLayout.addWidget(self.generateBtn)
        self.buttonLayout.addWidget(self.clearBtn)
        self.buttonLayout.addWidget(self.exportBtn)
        self.buttonLayout.addStretch()
        self.layout.addLayout(self.buttonLayout)
        
        self.layout.addStretch()


class Ui_TestCaseTab(QWidget):
    """测试用例页面"""
    def setupUi(self, parent):
        self.layout = QVBoxLayout(parent)
        
        # 输入方式选择
        self.inputGroup = QGroupBox("输入方式")
        self.inputLayout = QHBoxLayout()
        
        self.xmindRadio = QRadioButton("XMind导入")
        self.textRadio = QRadioButton("文本输入")
        self.xmindRadio.setChecked(True)
        self.inputLayout.addWidget(self.xmindRadio)
        self.inputLayout.addWidget(self.textRadio)
        self.inputLayout.addStretch()
        self.inputGroup.setLayout(self.inputLayout)
        self.layout.addWidget(self.inputGroup)
        
        # XMind输入区域
        self.xmindGroup = QGroupBox("XMind输入")
        self.xmindLayout = QVBoxLayout()
        
        self.xmindPathLabel = QLabel("测试点XMind路径:")
        self.xmindPathInput = QLineEdit()
        self.xmindBrowseBtn = QPushButton("选择文件")
        xmindPathLayout = QHBoxLayout()
        xmindPathLayout.addWidget(self.xmindPathInput)
        xmindPathLayout.addWidget(self.xmindBrowseBtn)
        self.xmindLayout.addLayout(xmindPathLayout)
        
        self.templateLabel = QLabel("模板文件:")
        self.templateInput = QLineEdit()
        self.templateBrowseBtn = QPushButton("选择文件")
        templateLayout = QHBoxLayout()
        templateLayout.addWidget(self.templateInput)
        templateLayout.addWidget(self.templateBrowseBtn)
        self.xmindLayout.addLayout(templateLayout)
        
        self.xmindGroup.setLayout(self.xmindLayout)
        self.layout.addWidget(self.xmindGroup)
        
        # 文本输入区域
        self.textGroup = QGroupBox("文本输入")
        self.textLayout = QVBoxLayout()
        
        self.testCaseTextInput = QTextEdit()
        self.textLayout.addWidget(self.testCaseTextInput)
        
        self.textGroup.setLayout(self.textLayout)
        self.textGroup.setVisible(False)
        self.layout.addWidget(self.textGroup)
        
        # 输出设置
        self.outputGroup = QGroupBox("输出设置")
        self.outputLayout = QVBoxLayout()
        
        self.outputPathLabel = QLabel("输出路径:")
        self.outputPathInput = QLineEdit()
        self.outputBrowseBtn = QPushButton("浏览")
        outputPathLayout = QHBoxLayout()
        outputPathLayout.addWidget(self.outputPathInput)
        outputPathLayout.addWidget(self.outputBrowseBtn)
        self.outputLayout.addWidget(self.outputPathLabel)
        self.outputLayout.addLayout(outputPathLayout)
        
        self.outputGroup.setLayout(self.outputLayout)
        self.layout.addWidget(self.outputGroup)
        
        # 操作按钮
        self.buttonLayout = QHBoxLayout()
        self.generateBtn = QPushButton("生成测试用例")
        self.clearBtn = QPushButton("清空")
        self.exportXmindBtn = QPushButton("导出XMind")
        self.exportXlsxBtn = QPushButton("导出Excel")
        self.buttonLayout.addWidget(self.generateBtn)
        self.buttonLayout.addWidget(self.clearBtn)
        self.buttonLayout.addWidget(self.exportXmindBtn)
        self.buttonLayout.addWidget(self.exportXlsxBtn)
        self.buttonLayout.addStretch()
        self.layout.addLayout(self.buttonLayout)
        
        self.layout.addStretch()


class Ui_OtherTab(QWidget):
    """其他功能页面"""
    def setupUi(self, parent):
        self.layout = QVBoxLayout(parent)
        
        # 格式转换工具分组
        self.convertGroup = QGroupBox("格式转换工具")
        self.convertLayout = QVBoxLayout()
        
        # XMind转XLSX
        self.xmindToXlsxGroup = QGroupBox("XMind转XLSX")
        self.xmindToXlsxLayout = QVBoxLayout()
        
        self.inputXmindLabel = QLabel("输入XMind:")
        self.inputXmindInput = QLineEdit()
        self.inputXmindBrowse = QPushButton("选择文件")
        inputXmindLayout = QHBoxLayout()
        inputXmindLayout.addWidget(self.inputXmindInput)
        inputXmindLayout.addWidget(self.inputXmindBrowse)
        self.xmindToXlsxLayout.addLayout(inputXmindLayout)
        
        self.outputXlsxLabel = QLabel("输出Excel:")
        self.outputXlsxInput = QLineEdit()
        self.outputXlsxBrowse = QPushButton("浏览")
        outputXlsxLayout = QHBoxLayout()
        outputXlsxLayout.addWidget(self.outputXlsxInput)
        outputXlsxLayout.addWidget(self.outputXlsxBrowse)
        self.xmindToXlsxLayout.addLayout(outputXlsxLayout)
        
        self.xmindToXlsxBtn = QPushButton("开始转换")
        self.xmindToXlsxLayout.addWidget(self.xmindToXlsxBtn)
        
        self.xmindToXlsxGroup.setLayout(self.xmindToXlsxLayout)
        self.convertLayout.addWidget(self.xmindToXlsxGroup)
        
        # 测试点转XLSX
        self.testPointToXlsxGroup = QGroupBox("测试点XMind转XLSX")
        self.testPointToXlsxLayout = QVBoxLayout()
        
        self.testPointInputLabel = QLabel("测试点XMind:")
        self.testPointInput = QLineEdit()
        self.testPointBrowse = QPushButton("选择文件")
        testPointLayout = QHBoxLayout()
        testPointLayout.addWidget(self.testPointInput)
        testPointLayout.addWidget(self.testPointBrowse)
        self.testPointToXlsxLayout.addLayout(testPointLayout)
        
        self.testPointOutputLabel = QLabel("输出Excel:")
        self.testPointOutput = QLineEdit()
        self.testPointOutputBrowse = QPushButton("浏览")
        testPointOutputLayout = QHBoxLayout()
        testPointOutputLayout.addWidget(self.testPointOutput)
        testPointOutputLayout.addWidget(self.testPointOutputBrowse)
        self.testPointToXlsxLayout.addLayout(testPointOutputLayout)
        
        self.testPointToXlsxBtn = QPushButton("开始转换")
        self.testPointToXlsxLayout.addWidget(self.testPointToXlsxBtn)
        
        self.testPointToXlsxGroup.setLayout(self.testPointToXlsxLayout)
        self.convertLayout.addWidget(self.testPointToXlsxGroup)
        
        self.convertGroup.setLayout(self.convertLayout)
        self.layout.addWidget(self.convertGroup)
        
        # 日志输出区域
        self.logGroup = QGroupBox("执行日志")
        self.logLayout = QVBoxLayout()
        
        self.logText = QPlainTextEdit()
        self.logText.setReadOnly(True)
        self.logLayout.addWidget(self.logText)
        
        self.clearLogBtn = QPushButton("清空日志")
        self.logLayout.addWidget(self.clearLogBtn)
        
        self.logGroup.setLayout(self.logLayout)
        self.layout.addWidget(self.logGroup)
        
        self.layout.addStretch()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1200, 700)
        
        # 创建主窗口（必须使用QMainWindow）
        if not isinstance(MainWindow, QMainWindow):
            MainWindow = QMainWindow()
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
        self.tabWidget = QTabWidget(MainWindow)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 30, 1180, 650))
        self.tabWidget.setTabsClosable(False)
        
        # 创建4个Tab页面
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