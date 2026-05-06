import json
import os
import re
from typing import Optional, List, Union, Dict, Any
from common.fileProcessor import fileProcessor
from utils.logs import LogManager
from loguru import logger

LogManager(log_dir=r"D:\AIGeneration\utils\logs")

# JSON数据转Markdown处理器
class MarkdownProcess:

    def __init__(self, template_path: str = "config/template.json"):
        """
        初始化Markdown处理器
        
        Args:
            template_path: 测试用例模板文件路径，默认为 config/template.json
        """
        try:
            self.ts = fileProcessor().find_and_read_file(template_path, type="json")
            logger.info(f"成功加载模板文件: {template_path}")
        except Exception as e:
            logger.error(f"加载模板文件失败: {template_path}, 错误: {str(e)}")
            self.ts = {}
            raise

    def extract_json_from_ai_response(self, text: str) -> str:
        """
        从AI响应中提取JSON字符串
        
        Args:
            text: AI响应的原始文本，可能包含```json代码块标记
            
        Returns:
            str: 提取并清理后的JSON字符串
            
        Raises:
            ValueError: 当无法从文本中提取JSON时抛出
            TypeError: 当输入不是字符串时抛出
        """
        if not isinstance(text, str):
            raise TypeError(f"期望输入类型为str，实际得到: {type(text).__name__}")
        
        if not text.strip():
            raise ValueError("输入文本为空")
        
        pattern = r"```json\s*({[\s\S]*?})\s*```"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            json_str = match.group(1)
            # 修复双大括号问题（Jinja2模板语法）
            valid_json = json_str.replace("{{", "{").replace("}}", "}")
            logger.debug("成功从AI响应中提取JSON")
            return valid_json
        else:
            logger.warning("未匹配到JSON代码块，尝试直接解析")
            # 尝试直接查找JSON对象
            direct_match = re.search(r"({[\s\S]*})", text, re.DOTALL)
            if direct_match:
                json_str = direct_match.group(1)
                valid_json = json_str.replace("{{", "{").replace("}}", "}")
                return valid_json
            raise ValueError("无法从响应中提取JSON内容")

    def testpoint_to_list(self, data: Union[Dict, List]) -> List[Any]:
        """
        将嵌套的测试点数据转换为扁平化列表
        
        Args:
            data: 测试点数据，可以是字典或列表结构
            
        Returns:
            List[Any]: 扁平化的测试点列表
            
        Raises:
            TypeError: 当输入数据类型不支持时抛出
        """
        if not isinstance(data, (dict, list)):
            raise TypeError(f"不支持的数据类型: {type(data).__name__}，期望 dict 或 list")
        
        test_points = []
        self._flatten_data(data, test_points)
        logger.debug(f"成功转换测试点，共 {len(test_points)} 条")
        return test_points
    
    def _flatten_data(self, data: Any, result: List[Any]) -> None:
        """
        递归展平数据结构（内部辅助方法）
        
        Args:
            data: 待展平的数据
            result: 存储结果的列表（引用传递）
        """
        if isinstance(data, dict):
            for value in data.values():
                self._flatten_data(value, result)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._flatten_data(item, result)
                else:
                    result.append(item)


    def json_to_markdown(self, data: Union[str, Dict, List], output_file: str, 
                         title: str = "测试点", auto_extract: bool = True) -> str:
        """
        将JSON数据转换为Markdown格式并写入文件
        
        Args:
            data: JSON数据，可以是字符串（含或不含```json标记）、字典或列表
            output_file: 输出的Markdown文件路径（必填）
            title: Markdown文档标题，默认为"测试点"
            auto_extract: 是否自动从AI响应中提取JSON，默认为True
            
        Returns:
            str: 生成的Markdown文件绝对路径
            
        Raises:
            ValueError: 当数据为空或输出文件路径无效时抛出
            json.JSONDecodeError: 当JSON解析失败时抛出
            IOError: 当文件写入失败时抛出
        """
        if not output_file:
            raise ValueError("输出文件路径不能为空")
        
        if data is None:
            raise ValueError("输入数据不能为空")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"创建输出目录: {output_dir}")
        
        # 如果data是字符串且需要自动提取，则提取JSON
        if isinstance(data, str) and auto_extract:
            try:
                extracted_json = self.extract_json_from_ai_response(data)
                data = json.loads(extracted_json)
                logger.info("成功从字符串中提取并解析JSON")
            except (ValueError, json.JSONDecodeError) as e:
                logger.error(f"JSON提取或解析失败: {str(e)}")
                raise
        elif isinstance(data, str):
            # 不自动提取，直接尝试解析为JSON字符串
            try:
                data = json.loads(data)
                logger.info("成功解析JSON字符串")
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {str(e)}")
                raise
        
        # 验证数据类型
        if not isinstance(data, (dict, list)):
            raise TypeError(f"不支持的数据类型: {type(data).__name__}，期望 dict、list 或 str")
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                self._write_markdown_recursive(data, f, level=0)
            
            abs_path = os.path.abspath(output_file)
            logger.info(f"Markdown文件生成成功: {abs_path}")
            return abs_path
            
        except IOError as e:
            logger.error(f"文件写入失败: {output_file}, 错误: {str(e)}")
            raise

    def _write_markdown_recursive(self, data: Any, file_handle, level: int = 0) -> None:
        """
        递归写入Markdown格式数据（内部方法）
        
        Args:
            data: 要写入的数据（字典、列表或基本类型）
            file_handle: 文件句柄
            level: 当前递归层级，用于确定标题级别
        """
        indent = "#" * (level + 2)  # 使用标题层级，从##开始
        
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    # 写入标题
                    file_handle.write(f"{indent} {key}\n\n")
                    # 递归处理子元素
                    self._write_markdown_recursive(value, file_handle, level + 1)
                else:
                    # 简单键值对
                    file_handle.write(f"{indent} {key}: {value}\n\n")
                    
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    file_handle.write("\n")
                    self._write_markdown_recursive(item, file_handle, level + 1)
                else:
                    # 列表项使用Markdown列表格式
                    file_handle.write(f"{indent} {item}\n")
            file_handle.write("\n")

    def json_to_testcase(self, data: Optional[Union[Dict, List]] = None, 
                         output_file: str = None, title: str = "测试用例") -> str:
        """
        将JSON数据转换为测试用例格式并写入文件
        
        Args:
            data: 测试用例数据（字典或列表），如果为None则使用默认模板
            output_file: 输出的Markdown文件路径（必填）
            title: Markdown文档标题，默认为"测试用例"
            
        Returns:
            str: 生成的Markdown文件绝对路径
            
        Raises:
            ValueError: 当输出文件路径为空时抛出
            IOError: 当文件写入失败时抛出
        """
        if not output_file:
            raise ValueError("输出文件路径不能为空")
        
        # 如果data为None，使用默认模板
        if data is None:
            if not self.ts:
                raise ValueError("默认模板数据为空，请提供data参数或检查模板文件")
            data = self.ts
            logger.info("使用默认模板数据")
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.info(f"创建输出目录: {output_dir}")
        
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n")
                self._write_testcase_recursive(data, f, level=0)

            abs_path = os.path.abspath(output_file)
            logger.info(f"测试用例文件生成成功: {abs_path}")
            return abs_path
            
        except IOError as e:
            logger.error(f"文件写入失败: {output_file}, 错误: {str(e)}")
            raise

    def _write_testcase_recursive(self, data: Any, file_handle, level: int = 0) -> None:
        """
        递归写入测试用例格式数据（内部方法）
        
        Args:
            data: 测试用例数据（字典、列表或基本类型）
            file_handle: 文件句柄
            level: 当前递归层级（保留参数以兼容，但实际使用title_levels映射）
        """
        # 定义标题级别映射
        title_levels = {
            "测试模块": 2,    # ## 级别
            "标题": 3,        # ### 级别
            "前置条件": 4,    # #### 级别
            "操作步骤": 5,    # ##### 级别
            "预期结果": 6     # ###### 级别
        }

        if isinstance(data, dict):
            for key, value in data.items():
                if key in title_levels:
                    level_num = title_levels[key]
                    indent = "#" * level_num

                    if key in ["前置条件", "操作步骤", "预期结果"]:
                        # 对于列表类型的值，将其格式化为编号列表并连接为一行
                        if isinstance(value, list):
                            formatted_items = " ".join(
                                [f"{i + 1}.{item}" for i, item in enumerate(value)]
                            )
                            file_handle.write(f"{indent} {formatted_items}\n\n")
                        else:
                            # 如果不是列表，直接输出
                            file_handle.write(f"{indent} {value}\n\n")
                    else:
                        # 对于非列表类型的值，直接输出
                        file_handle.write(f"{indent} {value}\n\n")
                        
                elif isinstance(value, (dict, list)):
                    # 递归处理其他嵌套结构
                    self._write_testcase_recursive(value, file_handle, level)
                    
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._write_testcase_recursive(item, file_handle, level)
                elif isinstance(item, list):
                    # 处理嵌套列表
                    for sub_item in item:
                        file_handle.write(f"{sub_item}\n")
                else:
                    # 列表项处理
                    file_handle.write(f"{item}\n")





if __name__ == "__main__":
    # 示例用法
    processor = MarkdownProcess()
    
    # 示例1: 从AI响应提取JSON并转换为Markdown
    ai_response = '''
    这是AI的响应
    ```json
    {
        "模块1": {
            "功能点1": ["测试点1", "测试点2"],
            "功能点2": ["测试点3"]
        }
    }
    ```
    '''
    
    try:
        # 转换为测试点Markdown
        output_path = processor.json_to_markdown(
            data=ai_response,
            output_file=r"D:/AIGeneration/testcase/testpoint.md",
            title="测试点"
        )
        print(f"测试点文件生成成功: {output_path}")
        
        # 转换为测试用例Markdown（使用默认模板）
        testcase_path = processor.json_to_testcase(
            output_file=r"D:/AIGeneration/testcase/testcase.md",
            title="测试用例"
        )
        print(f"测试用例文件生成成功: {testcase_path}")
        
    except Exception as e:
        print(f"处理失败: {str(e)}")

