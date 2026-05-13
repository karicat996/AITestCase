from service.xmindChanger import *
from ai.deepseekAPI import *
from common.promptProcessing import fileProcessor
import os
import time
import json
from utils.logs import LogManager
from loguru import logger
LogManager(log_dir=r"D:\AIGeneration\utils\logs")
class interfaceAITestPoint:
    """
    ai生成测试点接口
    支持手动输入内容
    导出为测试点json
    """
    def __init__(self):
        self.DS = DeepSeekAPI()
        self.converter = TestcasePointJsonToXmind()
        self.get_json = fileProcessor()

    def get_test_point(self, user_input,output_path,storage_json,Storage_test_points = True):
        if output_path is None:
            output_dir = r"D:\AIGeneration\testcase"
            filename = "output.xmind"
            output_path = os.path.join(output_dir, filename)
        ds_res = self.DS.get_test_point_answer(user_input)
        
        # 先将 AI 返回的字符串解析为字典对象
        try:
            test_data = json.loads(ds_res) if isinstance(ds_res, str) else ds_res
        except json.JSONDecodeError:
            print(f"错误：AI 返回的内容不是有效的 JSON 格式: {ds_res[:100]}...")
            return False
        
        # 是否需要将数据存到测试点json文件中（传入已解析的字典对象）
        if Storage_test_points:
            self.get_json.write_file(storage_json, test_data, "json")
        
        # 一键转换并导出
        success = self.converter.convert_and_export_to_xmind(
            input_data=test_data,
            output_xmind_file = output_path,
            root_title="测试大纲",
            sheet_title="功能测试用例"
        )



class interfaceAITestInput:
    """
    ai生成测试点接口
    支持手动输入内容
    导出为测试点xmind
    默认模板
    要支持自定义模板

    """
    def __init__(self):
        self.converter = TestPointToAIJson()
    def get_test_case_template(self, input_file, output_file, extract):
        """
        获取测试用例模板
        """
        try:
            # 一键转换数据并保存
            output_data = self.converter.convert_and_save(
                input_file,
                output_file,
                 extract
            )
            
            if not output_data:
                logger.error("没有输出存储json转换的数据")
                return False
            
            if extract and output_data is not None:
                # 读取转换后的JSON字符串
                ai_string = self.read_json_file_to_ai_string(output_file)
                print(type(ai_string))
                return ai_string
            elif not extract:
                # 直接读取JSON文件并转换
                ai_string = self.json_to_ai_string(output_data)
                print(type(ai_string))
                return ai_string
                
        except FileNotFoundError as e:
            print(f"✗ 文件未找到: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ JSON解析失败: {str(e)}")
            return False

    def read_json_file_to_ai_string(self, file_path, ensure_ascii=False):
        """
        读取JSON文件并转换为AI友好的紧凑字符串
        
        Args:
            file_path: JSON文件路径
            ensure_ascii: 是否确保ASCII编码，默认False（保留中文）
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return self.json_to_ai_string(json_data, ensure_ascii)

    def json_to_ai_string(self, json_data, ensure_ascii=False):
        # 如果输入是字符串，先解析为JSON对象
        if isinstance(json_data, str):
            try:
                json_data = json.loads(json_data)
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {str(e)}")
                raise ValueError(f"无效的JSON字符串: {str(e)}")
        
        # 转换为紧凑格式的JSON字符串
        compact_json = json.dumps(
            json_data,
            ensure_ascii=ensure_ascii,
            separators=(',', ':'),  # 去除冒号和逗号后的空格
            sort_keys=False  # 保持原始键顺序
        )
        
        return compact_json


class interfaceAITestCaseXmind:
    """
    ai生成测试用例xmind
    """
    def __init__(self):
        self.DS = DeepSeekAPI()
        self.converter = TestcaseJsonToXmind()
        self.get_json = fileProcessor()
        self.ai_test_input = interfaceAITestInput()
    def get_ai_testcase_write_json(self, user_input, output_path, extract, storage_file_path):
        """
        Args:
            user_input: 用户输入（测试点文件或数据）
            output_path: 输出路径
            extract: 是否提取为AI友好格式
            storage_file_path: 存储文件路径

        """
        try:
            # 1. 获取测试用例模板数据
            user_input = self.ai_test_input.get_test_case_template(user_input, output_path, extract)
            if not user_input:
                logger.error("没有获取到测试用例模板数据")
                return False
            
            # 2. 调用AI生成测试用例
            ds_res = self.DS.get_testcase_answer(user_input)
            if not ds_res:
                logger.error("AI未返回数据")
                return False
            logger.info(f"✓ AI返回数据，长度: {len(ds_res)} 字符")
            
            # 3. 清理和解析AI返回的数据
            cleaned_data = self.clean_ai_json_response(ds_res)
            if not cleaned_data:
                logger.error("无法解析AI返回的JSON数据")
                return False
            
            logger.info(f"✓ JSON数据解析成功，类型: {type(cleaned_data).__name__}")
            
            # 4. 写入JSON文件（传入字典对象，而非字符串）
            self.get_json.write_file(storage_file_path, cleaned_data, "json")
            
            logger.info(f"✓ 测试用例已保存到: {storage_file_path}")
            print("执行完毕")
            return True
            
        except Exception as e:
            logger.error(f"✗ 执行失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def clean_ai_json_response(self, ai_response: str):
        """
        清理和解析AI返回的JSON数据，兼容多种格式
        
        支持的格式：
        1. 纯JSON字符串: {"key": "value"}
        2. 带```json标记: ```json\n{...}\n```
        3. 带```标记: ```\n{...}\n```
        4. 前后有额外文本: "这是回答\n```json\n{...}\n```\n结束"
        
        Args:
            ai_response: AI返回的原始字符串
        Returns:
            dict or list: 解析后的JSON对象，失败返回None
        """
        if not ai_response or not isinstance(ai_response, str):
            logger.warning("AI返回数据为空或不是字符串")
            return None
        
        # 去除首尾空白
        ai_response = ai_response.strip()
        
        # 方法1：尝试直接解析（适用于纯JSON）
        try:
            data = json.loads(ai_response)
            logger.debug("直接解析JSON成功")
            return data
        except json.JSONDecodeError:
            logger.debug("直接解析失败，尝试提取代码块")
        
        # 方法2：提取```json ... ``` 或 ``` ... ``` 代码块
        import re
        
        # 匹配 ```json ... ``` 或 ``` ... ```
        patterns = [
            r'```json\s*([\s\S]*?)\s*```',  # ```json ... ```
            r'```\s*([\s\S]*?)\s*```',       # ``` ... ```
        ]
        
        for pattern in patterns:
            match = re.search(pattern, ai_response, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                logger.debug(f"通过正则提取到JSON字符串，长度: {len(json_str)}")
                
                # 尝试解析提取的JSON
                try:
                    data = json.loads(json_str)
                    logger.debug("解析提取的JSON成功")
                    return data
                except json.JSONDecodeError as e:
                    logger.warning(f"提取的JSON解析失败: {str(e)}")
                    continue
        
        # 方法3：尝试找到第一个 { 和最后一个 }
        logger.debug("尝试查找JSON对象边界")
        start_idx = ai_response.find('{')
        end_idx = ai_response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = ai_response[start_idx:end_idx+1]
            logger.debug(f"提取JSON对象，长度: {len(json_str)}")
            
            try:
                data = json.loads(json_str)
                logger.debug("解析JSON对象成功")
                return data
            except json.JSONDecodeError as e:
                logger.warning(f"JSON对象解析失败: {str(e)}")
        
        # 方法4：尝试找到第一个 [ 和最后一个 ]（数组格式）
        logger.debug("尝试查找JSON数组边界")
        start_idx = ai_response.find('[')
        end_idx = ai_response.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = ai_response[start_idx:end_idx+1]
            logger.debug(f"提取JSON数组，长度: {len(json_str)}")
            
            try:
                data = json.loads(json_str)
                logger.debug("解析JSON数组成功")
                return data
            except json.JSONDecodeError as e:
                logger.warning(f"JSON数组解析失败: {str(e)}")
        
        # 所有方法都失败
        logger.error("无法从AI响应中提取有效的JSON数据")
        logger.debug(f"AI响应前200字符: {ai_response[:200]}")
        return None

    def get_testcase_xmind(self):
        print("\n=== 测试用例JSON转化成xmind")
        # 读取测试用例JSON文件
        testcase_json_path = r"D:\AIGeneration\testcase\测试用例_output.json"
        testcase_data = self.get_json.find_and_read_file(testcase_json_path, type="json")

        # 转换并导出
        output_xmind = r"D:\AIGeneration\testcase\测试用例.xmind"
        success = self.converter.convert_and_export_to_xmind(
            input_data=testcase_data,
            output_xmind_file=output_xmind,
            root_title="测试用例",
            sheet_title="功能测试用例"
        )
        if success:
            print(f"✓ 测试用例XMind文件已生成：{output_xmind}")
        else:
            print("✗ 转换失败")


class interfaceAITestCaseXlsx:
    """
    导出为测试用例xlsx
    """
    def __init__(self):
        self.dc = MxindDataProcessor()
        self.converter =  TestcaseXmindToAIJson()
        self.to_xlsx = AIJsonToXlsx()


    def get_testcase_xlsx(self,output_json_path,json_file_path, output_xlsx_path):
        res = self.dc.write_to_json(output_json_path)

        xmind_data = self.converter.read_xmind_json(json_file_path)
        # 步骤2：转换为测试用例格式
        testcase_data = self.converter.convert_to_testcase_format(xmind_data)
        # 步骤3：保存数据
        self.converter.save_to_json(testcase_data, output_xlsx_path)
        # 步骤1：读取数据
        data = self.to_xlsx.read_data()
        # 步骤2：过滤数据
        test_cases = self.to_xlsx.filter_data()
        logger.info(f"共 {len(test_cases)} 条用例")
        # 步骤3：写入Excel
        success = self.to_xlsx.write_data(test_cases)
        if success:
            logger.info("转换成功！")


"""
测试用例xmind导出为xlsx
支持手动上传xmind文件
导出为测试用例xlsx

默认模板
要支持自定义模板

"""

class interfaceAITestCaseMd:
    """
    导出为测试用例md
    """
    def __init__(self):
        self.dc = MxindDataProcessor()
        self.processor = MarkdownProcess()

    def get_testcase_md(self,res_data,output_md_path):

        # 示例1: 从AI响应提取JSON并转换为Markdown
        ai_response = res_data
        try:
            # 转换为测试点Markdown
            output_path = self.processor.json_to_markdown(
                data=ai_response,
                output_file=output_md_path,
                # output_file=r"D:/AIGeneration/testcase/testpoint.md",
                title="测试点"
            )
            logger.debug(f"测试点文件生成成功: {output_path}")

            # 转换为测试用例Markdown（使用默认模板）
            testcase_path = self.processor.json_to_testcase(
                output_file=r"D:/AIGeneration/testcase/testcase.md",
                title="测试用例"
            )
            logger.debug(f"测试用例文件生成成功: {testcase_path}")

        except Exception as e:
            logger.error(f"处理失败: {str(e)}")




class interfaceAIAnyFlieToXlsx:
    """
    导入文案一键生成测试用例xlsx
    
    完整流程：
    1. 读取用户输入的文案（支持文本或文件）
    2. 调用AI生成测试点JSON
    3. 将测试点JSON转换为测试转化数据格式
    4. 调用AI生成测试用例JSON
    5. 将测试用例JSON转换为XMind格式
    6. 将XMind转换为测试用例JSON格式
    7. 最终导出为Excel文件
    """
    
    def __init__(self):
        """
        初始化接口集成类
        """
        self.deepseek_api = DeepSeekAPI()
        self.test_point_converter = TestcasePointJsonToXmind()
        self.test_point_to_ai = TestPointToAIJson()
        self.testcase_converter = TestcaseJsonToXmind()
        self.xmind_to_json = TestcaseXmindToAIJson()
        self.json_to_xlsx = AIJsonToXlsx()
        self.file_processor = fileProcessor()
    
    def generate_testcase_xlsx_from_text(self, user_input, output_dir=None, 
                                        test_point_file=None, 
                                        testcase_file=None,
                                        xmind_file=None,
                                        xlsx_file=None):
        """
        从用户输入文本一键生成测试用例xlsx
        
        Args:
            user_input: 用户输入的需求描述文本
            output_dir: 输出目录，默认为 D:\AIGeneration\testcase
            test_point_file: 测试点JSON文件路径（可选）
            testcase_file: 测试用例JSON文件路径（可选）
            xmind_file: XMind文件路径（可选）
            xlsx_file: Excel文件路径（可选）
            
        Returns:
            bool: 是否成功生成
        """
        try:
            # 设置默认输出目录
            if output_dir is None:
                output_dir = r"D:\AIGeneration\testcase"
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"创建输出目录: {output_dir}")
            
            # 步骤1: 调用AI生成测试点
            logger.info("步骤1: 调用AI生成测试点...")
            test_point_data = self._generate_test_points(user_input)
            if not test_point_data:
                logger.error("生成测试点失败")
                return False
            
            # 保存测试点JSON
            if test_point_file is None:
                test_point_file = os.path.join(output_dir, "测试点.json")
            self.file_processor.write_file(test_point_file, test_point_data, "json")
            logger.info(f"✓ 测试点已保存到: {test_point_file}")
            
            # 步骤2: 将测试点转换为测试转化数据格式
            logger.info("步骤2: 转换测试点为测试转化数据格式...")
            converted_data = self._convert_testpoint_to_ai_format(test_point_file)
            if not converted_data:
                logger.error("转换测试点格式失败")
                return False
            
            # 步骤3: 调用AI生成测试用例
            logger.info("步骤3: 调用AI生成测试用例...")
            testcase_data = self._generate_testcases(converted_data)
            if not testcase_data:
                logger.error("生成测试用例失败")
                return False
            
            # 保存测试用例JSON
            if testcase_file is None:
                testcase_file = os.path.join(output_dir, "测试用例_output.json")
            self.file_processor.write_file(testcase_file, testcase_data, "json")
            logger.info(f"✓ 测试用例已保存到: {testcase_file}")
            
            # 步骤4: 将测试用例JSON转换为XMind
            logger.info("步骤4: 转换测试用例为XMind格式...")
            if xmind_file is None:
                xmind_file = os.path.join(output_dir, "测试用例.xmind")
            success = self._convert_testcase_to_xmind(testcase_data, xmind_file)
            if not success:
                self.logger.error("转换XMind失败")
                return False
            logger.info(f"✓ XMind文件已生成: {xmind_file}")
            
            # 步骤5: 将XMind转换为测试用例JSON格式
            logger.info("步骤5: 转换XMind为测试用例JSON格式...")
            final_testcase_data = self._convert_xmind_to_testcase_json(xmind_file)
            if not final_testcase_data:
                self.logger.error("转换测试用例JSON格式失败")
                return False
            
            # 步骤6: 导出为Excel
            logger.info("步骤6: 导出为Excel文件...")
            if xlsx_file is None:
                xlsx_file = os.path.join(output_dir, "测试用例.xlsx")
            success = self._export_to_xlsx(final_testcase_data, xlsx_file)
            if not success:
                self.logger.error("导出Excel失败")
                return False
            
            logger.info(f"✓ 测试用例Excel已生成: {xlsx_file}")
            print(f"\n✓ 完成！测试用例Excel文件已生成: {xlsx_file}")
            return True
            
        except Exception as e:
            logger.error(f"✗ 生成测试用例Excel失败: {str(e)}", exc_info=True)
            print(f"✗ 生成失败: {str(e)}")
            return False
    
    def _generate_test_points(self, user_input):
        """
        调用AI生成测试点
        
        Args:
            user_input: 用户输入的需求描述
            
        Returns:
            dict: 测试点数据字典
        """
        try:
            ds_res = self.deepseek_api.get_test_point_answer(user_input)
            
            # 解析AI返回的JSON
            if isinstance(ds_res, str):
                try:
                    test_data = json.loads(ds_res)
                except json.JSONDecodeError:
                    self.logger.error(f"AI返回的内容不是有效的JSON格式: {ds_res[:100]}...")
                    return None
            else:
                test_data = ds_res
            
            logger.info(f"✓ 成功生成测试点，包含 {len(test_data)} 个产品/模块")
            return test_data
            
        except Exception as e:
            logger.error(f"生成测试点时发生错误: {str(e)}", exc_info=True)
            return None
    
    def _convert_testpoint_to_ai_format(self, test_point_file):
        """
        将测试点JSON转换为AI友好的格式
        
        Args:
            test_point_file: 测试点JSON文件路径
            
        Returns:
            str: AI友好的JSON字符串
        """
        try:
            # 使用TestPointToAIJson转换器
            converter = TestPointToAIJson()
            
            # 转换并获取数据（不保存到文件）
            output_file = test_point_file.replace('.json', '_converted.json')
            converted_data = converter.convert_and_save(
                input_file=test_point_file,
                output_file=output_file,
                extract=False  # 不保存，直接返回数据
            )
            
            if not converted_data:
                self.logger.error("转换测试点数据失败")
                return None
            
            # 转换为AI友好的紧凑格式
            ai_string = json.dumps(
                converted_data,
                ensure_ascii=False,
                separators=(',', ':'),
                sort_keys=False
            )
            
            logger.info(f"✓ 测试点转换完成，长度: {len(ai_string)} 字符")
            return ai_string
            
        except Exception as e:
            logger.error(f"转换测试点格式时发生错误: {str(e)}", exc_info=True)
            return None
    
    def _generate_testcases(self, test_point_data):
        """
        调用AI生成测试用例
        
        Args:
            test_point_data: 测试点数据（字符串或字典）
            
        Returns:
            dict: 测试用例数据字典
        """
        try:
            # 如果传入的是字典，转换为字符串
            if isinstance(test_point_data, dict):
                test_point_str = json.dumps(test_point_data, ensure_ascii=False)
            else:
                test_point_str = test_point_data
            
            # 调用AI生成测试用例
            ds_res = self.deepseek_api.get_testcase_answer(test_point_str)
            if not ds_res:
                logger.error("AI未返回数据")
                return None
            
            logger.info(f"✓ AI返回测试用例数据，长度: {len(ds_res)} 字符")
            
            # 清理和解析AI返回的数据
            cleaned_data = self._clean_ai_json_response(ds_res)
            if not cleaned_data:
                logger.error("无法解析AI返回的JSON数据")
                return None
            
            logger.info(f"✓ JSON数据解析成功，类型: {type(cleaned_data).__name__}")
            return cleaned_data
            
        except Exception as e:
            logger.error(f"生成测试用例时发生错误: {str(e)}", exc_info=True)
            return None
    
    def _clean_ai_json_response(self, ai_response):
        """
        清理和解析AI返回的JSON数据
        
        Args:
            ai_response: AI返回的原始字符串
            
        Returns:
            dict or list: 解析后的JSON对象
        """
        if not ai_response or not isinstance(ai_response, str):
            logger.warning("AI返回数据为空或不是字符串")
            return None
        
        ai_response = ai_response.strip()
        
        # 方法1：尝试直接解析
        try:
            data = json.loads(ai_response)
            return data
        except json.JSONDecodeError:
            pass
        
        # 方法2：提取代码块
        import re
        patterns = [
            r'```json\s*([\s\S]*?)\s*```',
            r'```\s*([\s\S]*?)\s*```',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, ai_response, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    data = json.loads(json_str)
                    return data
                except json.JSONDecodeError:
                    continue
        
        # 方法3：查找JSON对象边界
        start_idx = ai_response.find('{')
        end_idx = ai_response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = ai_response[start_idx:end_idx+1]
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError:
                pass
        
        # 方法4：查找JSON数组边界
        start_idx = ai_response.find('[')
        end_idx = ai_response.rfind(']')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = ai_response[start_idx:end_idx+1]
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError:
                pass
        
        logger.error("无法从AI响应中提取有效的JSON数据")
        return None
    
    def _convert_testcase_to_xmind(self, testcase_data, xmind_file):
        """
        将测试用例JSON转换为XMind文件
        
        Args:
            testcase_data: 测试用例数据字典
            xmind_file: 输出的XMind文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            converter = TestcaseJsonToXmind()
            success = converter.convert_and_export_to_xmind(
                input_data=testcase_data,
                output_xmind_file=xmind_file,
                root_title="测试用例",
                sheet_title="功能测试用例"
            )
            return success
            
        except Exception as e:
            self.logger.error(f"转换XMind时发生错误: {str(e)}", exc_info=True)
            return False
    
    def _convert_xmind_to_testcase_json(self, xmind_file):
        """
        将XMind文件转换为测试用例JSON格式
        
        Args:
            xmind_file: XMind文件路径
            
        Returns:
            dict: 测试用例数据字典
        """
        try:
            # 首先将XMind转换为JSON
            processor = MxindDataProcessor()
            temp_json_file = xmind_file.replace('.xmind', '.json')
            processor.xmind_file = xmind_file
            xmind_json = processor.xmind_to_json()
            
            if not xmind_json:
                self.logger.error("读取XMind数据失败")
                return None
            
            # 转换为测试用例格式
            converter = TestcaseXmindToAIJson()
            testcase_data = converter.convert_to_testcase_format(xmind_json)
            
            if not testcase_data or '测试用例' not in testcase_data:
                logger.error("转换测试用例格式失败")
                return None
            
            logger.info(f"✓ 成功转换 {len(testcase_data.get('测试用例', []))} 条测试用例")
            return testcase_data
            
        except Exception as e:
            logger.error(f"转换XMind为JSON时发生错误: {str(e)}", exc_info=True)
            return None
    
    def _export_to_xlsx(self, testcase_data, xlsx_file):
        """
        将测试用例数据导出为Excel文件
        
        Args:
            testcase_data: 测试用例数据字典
            xlsx_file: 输出的Excel文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 临时保存测试用例JSON
            temp_json_file = xlsx_file.replace('.xlsx', '.json')
            self.file_processor.write_file(temp_json_file, testcase_data, "json")
            
            # 使用AIJsonToXlsx导出
            exporter = AIJsonToXlsx()
            exporter.file_path = temp_json_file
            exporter.output_file = xlsx_file
            
            # 过滤数据
            test_cases = exporter.filter_data()
            if not test_cases:
                self.logger.error("没有可导出的测试用例数据")
                return False
            
            logger.info(f"共找到 {len(test_cases)} 条测试用例")
            
            # 写入Excel
            success = exporter.write_data(test_cases)
            
            # 清理临时文件
            if os.path.exists(temp_json_file):
                os.remove(temp_json_file)
            
            return success
            
        except Exception as e:
            logger.error(f"导出Excel时发生错误: {str(e)}", exc_info=True)
            return False



class interfaceAITestCaseXlsxOneKey:
    """
    导入测试点xmind一键生成测试用例xlsx
    """




if __name__ == '__main__':
    # #测试点
    # interfaceAITestPoint().get_test_point(user_input="电商下单界面功能",
    #                                       output_path=r"D:\AIGeneration\testcase\output.xmind",
    #                                       storage_json=r"D:\AIGeneration\testcase\测试点.json")
     #测试用例
     interfaceAITestCaseXmind().get_ai_testcase_write_json(user_input=r'D:\AIGeneration\testcase\output.json',
                                        output_path=r'D:\AIGeneration\testcase\测试转化数据.json',
                                        extract=False,
                                        storage_file_path=r'D:\AIGeneration\testcase\测试用例_output.json'
                                        )
     time.sleep(5)
     interfaceAITestCaseXmind().get_testcase_xmind()

     #测试用例xlsx
     # interfaceAITestCaseXlsx().get_testcase_xlsx(output_json_path=r"D:\AIGeneration\testcase\xmind_output.json",
     #                                             json_file_path=r"D:\AIGeneration\testcase\xmind_output.json",
     #                                             output_xlsx_path=r"D:\AIGeneration\testcase\output.json"
     #
     #                                          )
     #测试用例md

    # 简单用法 - 使用默认路径
    # converter = interfaceAIAnyFlieToXlsx()
    # success = converter.generate_testcase_xlsx_from_text(
    #     user_input="电商下单界面功能，包括商品选择、地址管理、优惠券、订单提交等模块"
    # )

    # 高级用法 - 自定义所有路径
    # success = converter.generate_testcase_xlsx_from_text(
    #     user_input="用户登录注册功能",
    #     output_dir=r"D:\MyProject\testcases",
    #     test_point_file=r"D:\MyProject\testpoints.json",
    #     testcase_file=r"D:\MyProject\testcases.json",
    #     xmind_file=r"D:\MyProject\testcases.xmind",
    #     xlsx_file=r"D:\MyProject\final_testcases.xlsx"
    # )