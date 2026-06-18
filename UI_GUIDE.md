# UI功能使用说明

## 概述

本项目已完成UI功能的全面完善，包括信号槽连接、样式控制、用户体验优化等。

## 主要改进

### 1. UI样式配置 (uistyle.py)

**现代主题样式**：
- 应用了现代化的UI设计
- 自定义颜色方案（主蓝色、绿色、橙色等）
- 优化的按钮、输入框、下拉框样式
- 美化的滚动条和Tab标签页
- 高DPI屏幕支持

**样式特点**：
- ✅ 统一的配色方案
- ✅ 平滑的悬停效果
- ✅ 清晰的焦点指示
- ✅ 响应式布局

### 2. Controller控制器增强 (controller.py)

**信号槽连接**：
- 菜单栏：保存配置动作
- 配置页：保存/加载配置、文件浏览按钮
- 测试点页：输入方式切换、图片选择、生成/清空/导出
- 测试用例页：输入方式切换、文件选择、生成/导出功能
- 其他功能页：格式转换、日志管理

**核心功能方法**：

#### 工具方法
- `browse_file()` - 文件选择对话框
- `select_image()` - 图片选择与预览
- `toggle_input_method()` - 切换测试点输入方式
- `toggle_case_input_method()` - 切换测试用例输入方式
- `save_config()` - 保存配置到YAML
- `load_config()` - 从YAML加载配置
- `append_log()` - 追加日志输出
- `clear_log()` - 清空日志

#### 业务逻辑方法
- `generate_test_points()` - 生成测试点
- `clear_test_points()` - 清空测试点输入
- `export_test_points()` - 导出测试点到XMind
- `generate_test_cases()` - 生成测试用例
- `clear_test_cases()` - 清空测试用例输入
- `export_to_xmind()` - 导出为XMind格式
- `export_to_xlsx()` - 导出为Excel格式
- `convert_xmind_to_xlsx()` - 转换XMind到Excel
- `convert_testpoint_to_xlsx()` - 转换测试点XMind到Excel

### 3. 应用程序入口 (app.py)

**启动流程**：
1. 启用高DPI支持
2. 设置全局字体（微软雅黑 10pt）
3. 应用现代主题样式
4. 创建Controller实例
5. 初始化主窗口并连接信号槽
6. 显示主窗口

## UI界面说明

### 配置项页面

**功能配置组**：
- DeepSeek API Key - AI接口密钥
- 模型选择 - 支持deepseek-chat等

**测试点配置组**：
- 输出JSON路径
- 模板路径
- 图片路径

**测试用例配置组**：
- 输出JSON路径
- XMind保存路径
- Excel保存路径

**其他功能配置组**：
- 输出JSON路径
- 模板路径
- 图片路径

**操作按钮**：
- 保存配置 - 保存当前配置到YAML文件
- 初始化 - 从YAML文件加载配置

### 测试点功能页面

**输入方式**：
- 图片识别 - 上传图片进行识别
- 文本输入 - 直接输入文本内容

**图片预览区**：
- 支持图片选择
- 实时预览（最大400x200）
- 保持宽高比缩放

**生成选项**：
- 严格模式
- 详细输出

**操作按钮**：
- 生成测试点
- 清空输入
- 导出XMind

### 测试用例页面

**输入方式**：
- XMind导入 - 从XMind文件导入
- 文本输入 - 直接输入文本

**配置项**：
- 测试点XMind路径
- 模板文件路径
- 输出路径

**操作按钮**：
- 生成测试用例
- 清空输入
- 导出XMind
- 导出Excel

### 其他功能页面

**格式转换工具**：
1. XMind转XLSX
   - 输入XMind文件
   - 输出Excel路径
   
2. 测试点XMind转XLSX
   - 测试点XMind文件
   - 输出Excel路径

**执行日志**：
- 实时显示操作日志
- 带时间戳
- 可清空日志

## 使用示例

### 启动应用

```bash
cd D:\AIGeneration
python -m src.app
```

或直接运行：

```bash
python src/app.py
```

### 配置步骤

1. **打开配置项页面**
2. **填写必要配置**：
   - API Key
   - 各路径配置
3. **点击"保存配置"**

### 生成测试点流程

1. 切换到"测试点功能"页面
2. 选择输入方式（图片/文本）
3. 如使用图片，点击"选择图片"
4. 勾选生成选项（可选）
5. 点击"生成测试点"
6. 如需导出，点击"导出XMind"

### 生成测试用例流程

1. 切换到"测试用例"页面
2. 选择输入方式（XMind/文本）
3. 输入相关文件路径
4. 点击"生成测试用例"
5. 选择导出格式（XMind/Excel）

## 配置文件说明

配置文件位置：`config/systemConfig.yaml`

```yaml
DEEPSEEK_API_KEY: "your-api-key"
OUTPUT_JSON_PATH: "输出JSON路径"
DEFAULT_TEMPLATE_PATH: "默认模板路径"
IMG_PATH: "图片路径"
TEST_XMIND_PATH: "测试XMind路径"
TEMPLATE_XMIND_PATH: "模板XMind路径"
TESTCASE_JSON_PATH: "测试用例JSON路径"
CONVERTED_TESTCASES_JSON_PATH: "转换后的测试用例路径"
TEMPLATE_PATH: "模板路径"
TEST_POINT_XMIND_FILE: "测试点XMind文件"
```

## 样式自定义

如需修改样式，编辑 `src/uistyle.py`：

```python
# 修改主色调
PRIMARY_COLOR = "#2196F3"      # 蓝色
SECONDARY_COLOR = "#4CAF50"    # 绿色
ACCENT_COLOR = "#FF9800"       # 橙色
```

## 扩展开发

### 添加新功能按钮

1. 在 `untitled.py` 中添加UI组件
2. 在 `controller.py` 的 `init_controller()` 中连接信号：
   ```python
   self.newButton.clicked.connect(self.new_function)
   ```
3. 实现功能方法：
   ```python
   def new_function(self):
       try:
           self.append_log("执行新功能")
           # 业务逻辑
       except Exception as e:
           self.append_log(f"错误：{str(e)}")
           QMessageBox.critical(self.main_window, "错误", str(e))
   ```

### 添加新的配置项

1. 在 `untitled.py` 的 `Ui_ConfigTab` 中添加控件
2. 在 `controller.py` 的 `save_config()` 和 `load_config()` 中添加对应项
3. 在 `systemConfig.yaml` 中添加配置键

## 注意事项

1. **首次使用**：请先在"配置项"页面配置必要的路径和API Key
2. **图片预览**：支持PNG、JPG、JPEG、BMP格式
3. **配置文件**：自动保存在 `config/systemConfig.yaml`
4. **日志输出**：所有操作都会在"执行日志"区域显示
5. **错误处理**：异常情况会弹出错误提示并记录日志

## 技术栈

- **GUI框架**：PySide6 6.10.0
- **样式**：QSS（Qt Style Sheets）
- **配置**：YAML
- **日志**：时间戳 + 日志消息

## 后续优化建议

1. 添加批量文件处理功能
2. 实现文件拖拽支持
3. 添加快捷键支持
4. 实现配置模板管理
5. 添加进度条显示
6. 实现后台任务处理
7. 添加撤销/重做功能
8. 支持多语言界面

## 联系与支持

如有问题或建议，请参考项目文档或联系开发团队。
