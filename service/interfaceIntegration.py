from ai.deepseekAPI import DeepSeekAPI
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
    导出为测试点xmind
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
                    # 尝试修复后再解析
                    fixed_data = self._try_fix_json(json_str)
                    if fixed_data is not None:
                        logger.debug("修复后解析成功")
                        return fixed_data
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
                # 尝试修复后再解析
                fixed_data = self._try_fix_json(json_str)
                if fixed_data is not None:
                    logger.debug("修复后解析成功")
                    return fixed_data
        
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
                # 尝试修复后再解析
                fixed_data = self._try_fix_json(json_str)
                if fixed_data is not None:
                    logger.debug("修复后解析成功")
                    return fixed_data
        
        # 所有方法都失败
        logger.error("无法从AI响应中提取有效的JSON数据")
        logger.debug(f"AI响应前200字符: {ai_response[:200]}")
        logger.debug(f"AI响应后200字符: {ai_response[-200:]}")
        return None
    
    def _try_fix_json(self, json_str: str):
        """
        尝试修复常见的JSON格式错误
        
        Args:
            json_str: 可能有错误的JSON字符串
        Returns:
            dict or list or None: 修复并解析后的对象，失败返回None
        """
        import re
        
        if not json_str or not isinstance(json_str, str):
            return None
        
        original = json_str
        fixes_applied = []
        
        try:
            # 尝试1: 移除尾部逗号 (在 } 或 ] 之前的逗号)
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            if json_str != original:
                fixes_applied.append("移除尾部逗号")
            
            try:
                data = json.loads(json_str)
                logger.debug(f"修复成功 ({', '.join(fixes_applied)})")
                return data
            except json.JSONDecodeError:
                pass
            
            # 尝试2: 补全缺失的逗号 (在 } 或 ] 之后，" 或 { 或 [ 之前)
            json_str_fixed = re.sub(r'([}\]])\s*(?=["\{\[])', r'\1,', json_str)
            if json_str_fixed != json_str:
                fixes_applied.append("补全缺失逗号")
                try:
                    data = json.loads(json_str_fixed)
                    logger.debug(f"修复成功 ({', '.join(fixes_applied)})")
                    return data
                except json.JSONDecodeError:
                    pass
            
            # 尝试3: 处理未闭合的字符串 - 查找可能被截断的位置
            # 如果JSON被截断，尝试找到最后一个完整的元素
            if json_str.rstrip().endswith(','):
                json_str = json_str.rstrip(',')
                fixes_applied.append("移除末尾逗号")
                try:
                    data = json.loads(json_str + '}' if '{' in original else json_str + ']')
                    logger.debug(f"修复成功 ({', '.join(fixes_applied)})")
                    return data
                except json.JSONDecodeError:
                    pass
            
            # 尝试4: 如果是对象但被截断，尝试补全
            if original.strip().startswith('{') and not original.strip().endswith('}'):
                # 找到最后一个完整的键值对
                last_brace = original.rfind('}')
                if last_brace > 0:
                    truncated = original[:last_brace+1]
                    try:
                        data = json.loads(truncated)
                        logger.debug("使用截断的部分JSON解析成功")
                        return data
                    except json.JSONDecodeError:
                        pass
            
            # 尝试5: 如果是数组但被截断
            if original.strip().startswith('[') and not original.strip().endswith(']'):
                last_bracket = original.rfind(']')
                if last_bracket > 0:
                    truncated = original[:last_bracket+1]
                    try:
                        data = json.loads(truncated)
                        logger.debug("使用截断的部分JSON解析成功")
                        return data
                    except json.JSONDecodeError:
                        pass
            
            logger.debug(f"所有修复尝试均失败 (已尝试: {', '.join(fixes_applied) if fixes_applied else '无'})")
            return None
            
        except Exception as e:
            logger.debug(f"修复JSON时出错: {str(e)}")
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
    Xmind导出为测试用例xlsx
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


class interfaceAITestCaseMd:
    """
    Xmind导出为测试用例md
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
            output_dir: 输出目录,默认为 D:\\AIGeneration\\testcase
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


class TestPointXmindToTestcaseXlsx:
    """
    导入测试点XMind文件，一键生成测试用例XLSX文件
    """


    def __init__(self):
        """
        初始化转换器
        """
        self.deepseek_api = DeepSeekAPI()
        self.test_point_xmind_to_json = XmindPointJson()
        self.test_point_to_ai = TestPointToAIJson()
        self.json_to_xlsx = AIJsonToXlsx()
        self.file_processor = fileProcessor()

    def convert_xmind_to_testcase_xlsx(
            self,
            xmind_file: str,
            output_xlsx_file: str = None,
            temp_json_dir: str = None
    ) -> bool:
        """
        主方法：从测试点XMind文件一键生成测试用例XLSX文件

        Args:
            xmind_file: 输入的测试点XMind文件路径
            output_xlsx_file: 输出的测试用例XLSX文件路径（可选，默认自动生成）
            temp_json_dir: 临时JSON文件存储目录（可选，默认使用testcase目录）

        Returns:
            bool: 转换是否成功

        Raises:
            FileNotFoundError: 当XMind文件不存在时抛出
            ValueError: 当参数无效时抛出
            Exception: 其他异常
        """
        # 入参校验
        if not xmind_file or not isinstance(xmind_file, str):
            logger.error("xmind_file参数不能为空且必须为字符串类型")
            raise ValueError("xmind_file参数不能为空且必须为字符串类型")

        if not os.path.exists(xmind_file):
            logger.error(f"XMind文件不存在: {xmind_file}")
            raise FileNotFoundError(f"XMind文件不存在: {xmind_file}")

        try:
            logger.info(f"=" * 60)
            logger.info(f"开始执行测试点XMind到测试用例XLSX的转换")
            logger.info(f"输入文件: {xmind_file}")
            logger.info(f"=" * 60)

            # 设置默认输出路径
            if not output_xlsx_file:
                base_name = os.path.splitext(os.path.basename(xmind_file))[0]
                output_xlsx_file = os.path.join(
                    os.path.dirname(xmind_file),
                    f"{base_name}_测试用例.xlsx"
                )

            if not temp_json_dir:
                temp_json_dir = os.path.dirname(TESTCASE_JSON_PATH)

            # 确保临时目录存在
            if not os.path.exists(temp_json_dir):
                os.makedirs(temp_json_dir, exist_ok=True)
                logger.info(f"创建临时目录: {temp_json_dir}")

            # 步骤1: XMind转JSON
            logger.info(f"\n步骤1/5: 将测试点XMind转换为JSON...")
            test_points_json = self._step1_xmind_to_json(xmind_file)
            if not test_points_json:
                logger.error("步骤1失败：XMind转JSON失败")
                return False

            # 保存中间结果
            test_points_json_path = os.path.join(temp_json_dir, "测试点.json")
            with open(test_points_json_path, 'w', encoding='utf-8') as f:
                json.dump(test_points_json, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ 测试点JSON已保存: {test_points_json_path}")

            # 步骤2: 转换为AI可理解的格式
            logger.info(f"\n步骤2/5: 将测试点数据转换为AI输入格式...")
            ai_input_data = self._step2_convert_to_ai_format(test_points_json)
            if not ai_input_data:
                logger.error("步骤2失败：数据格式转换失败")
                return False

            # 保存中间结果
            ai_input_path = os.path.join(temp_json_dir, "测试转化数据.json")
            with open(ai_input_path, 'w', encoding='utf-8') as f:
                json.dump(ai_input_data, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ AI输入数据已保存: {ai_input_path}")

            # 步骤3: 调用AI生成测试用例
            logger.info(f"\n步骤3/5: 调用AI生成测试用例（可能需要几分钟）...")
            testcase_json_str = self._step3_call_ai_to_generate_testcases(ai_input_data)
            if not testcase_json_str:
                logger.error("步骤3失败：AI生成测试用例失败")
                return False

            # 步骤4: 解析AI返回的JSON
            logger.info(f"\n步骤4/5: 解析AI返回的测试用例数据...")
            testcase_data = self._step4_parse_ai_response(testcase_json_str)
            if not testcase_data:
                logger.error("步骤4失败：解析AI响应失败")
                return False

            # 保存中间结果
            testcase_json_path = os.path.join(temp_json_dir, "测试用例_output.json")
            with open(testcase_json_path, 'w', encoding='utf-8') as f:
                json.dump(testcase_data, f, ensure_ascii=False, indent=2)
            logger.info(f"✓ 测试用例JSON已保存: {testcase_json_path}")

            # 步骤5: 转换为XLSX
            logger.info(f"\n步骤5/5: 将测试用例JSON转换为XLSX...")
            success = self._step5_json_to_xlsx(testcase_data, output_xlsx_file)
            if not success:
                logger.error("步骤5失败：JSON转XLSX失败")
                return False

            logger.info(f"\n{'=' * 60}")
            logger.info(f"✓ 转换完成！")
            logger.info(f"输出文件: {output_xlsx_file}")
            logger.info(f"{'=' * 60}")
            print(f"\n✓ 测试用例XLSX文件已成功生成: {output_xlsx_file}")
            return True

        except FileNotFoundError as e:
            logger.error(f"文件未找到: {str(e)}")
            raise
        except ValueError as e:
            logger.error(f"参数错误: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"转换过程中发生错误: {str(e)}", exc_info=True)
            raise

    def _step1_xmind_to_json(self, xmind_file: str) -> dict:
        """
        步骤1: 将XMind文件转换为JSON格式

        Args:
            xmind_file: XMind文件路径

        Returns:
            dict: 测试点JSON数据
        """
        try:
            # 创建XmindPointJson实例并指定文件
            converter = XmindPointJson(xmind_file=xmind_file)

            # 读取XMind数据
            xmind_data = converter.read_xmind_data()
            if not xmind_data:
                logger.error("读取XMind数据失败")
                return {}

            # 提取测试点数据
            test_points_data = converter._extract_test_points_data(xmind_data)
            if not test_points_data:
                logger.error("提取测试点数据失败")
                return {}

            logger.info(f"✓ 成功提取 {len(test_points_data)} 个产品的测试点数据")
            return test_points_data

        except Exception as e:
            logger.error(f"XMind转JSON失败: {str(e)}", exc_info=True)
            return {}

    def _step2_convert_to_ai_format(self, test_points_data: dict) -> dict:
        """
        步骤2: 将测试点数据转换为AI可理解的格式

        Args:
            test_points_data: 测试点JSON数据

        Returns:
            dict: 转换后的AI输入数据
        """
        try:
            # 使用TestPointToAIJson转换器
            converter = TestPointToAIJson()

            # 转换为简化格式
            ai_input_data = converter.convert_testpoint_to_simple_format(test_points_data)

            if not ai_input_data:
                logger.error("转换为AI格式失败")
                return {}

            logger.info(f"✓ 成功转换 {len(ai_input_data)} 个测试点为AI输入格式")
            return ai_input_data

        except Exception as e:
            logger.error(f"转换为AI格式失败: {str(e)}", exc_info=True)
            return {}

    def _step3_call_ai_to_generate_testcases(self, ai_input_data: dict) -> str:
        """
        步骤3: 调用AI生成测试用例

        Args:
            ai_input_data: AI输入数据

        Returns:
            str: AI返回的测试用例JSON字符串
        """
        try:
            # 将字典转换为字符串作为AI输入
            import json
            ai_input_str = json.dumps(ai_input_data, ensure_ascii=False, indent=2)

            # 调用DeepSeek API生成测试用例
            logger.info("正在调用DeepSeek API生成测试用例...")
            testcase_json_str = self.deepseek_api.get_testcase_answer(ai_input_str)

            if not testcase_json_str:
                logger.error("AI返回结果为空")
                return ""

            logger.info(f"✓ AI生成完成，返回内容长度: {len(testcase_json_str)} 字符")
            return testcase_json_str

        except Exception as e:
            logger.error(f"调用AI生成测试用例失败: {str(e)}", exc_info=True)
            return ""

    def _step4_parse_ai_response(self, ai_response: str) -> dict:
        """
        步骤4: 解析AI返回的响应

        Args:
            ai_response: AI返回的字符串

        Returns:
            dict: 解析后的测试用例数据
        """
        try:
            # 尝试直接解析JSON
            try:
                testcase_data = json.loads(ai_response)
                logger.info("✓ 成功解析AI返回的JSON数据")
                return testcase_data
            except json.JSONDecodeError:
                # 如果直接解析失败，尝试提取JSON部分
                logger.warning("直接JSON解析失败，尝试提取JSON内容...")

                # 查找JSON代码块
                import re
                json_pattern = r'```json\s*(.*?)\s*```'
                match = re.search(json_pattern, ai_response, re.DOTALL)

                if match:
                    json_str = match.group(1)
                    testcase_data = json.loads(json_str)
                    logger.info("✓ 从代码块中成功提取并解析JSON")
                    return testcase_data
                else:
                    # 尝试查找第一个{和最后一个}
                    start_idx = ai_response.find('{')
                    end_idx = ai_response.rfind('}')

                    if start_idx != -1 and end_idx != -1:
                        json_str = ai_response[start_idx:end_idx + 1]
                        testcase_data = json.loads(json_str)
                        logger.info("✓ 从文本中提取并解析JSON")
                        return testcase_data
                    else:
                        logger.error("无法从AI响应中提取JSON数据")
                        return {}

        except Exception as e:
            logger.error(f"解析AI响应失败: {str(e)}", exc_info=True)
            return {}

    def _step5_json_to_xlsx(self, testcase_data: dict, output_file: str) -> bool:
        """
        步骤5: 将测试用例JSON转换为XLSX

        Args:
            testcase_data: 测试用例JSON数据
            output_file: 输出XLSX文件路径

        Returns:
            bool: 转换是否成功
        """
        try:
            # 创建AIJsonToXlsx实例
            converter = AIJsonToXlsx()

            # 设置输出文件路径
            converter.output_file = output_file

            # 确保输出目录存在
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"创建输出目录: {output_dir}")

            # 提取测试用例列表
            test_cases = []
            
            # 直接从传入的testcase_data中提取测试用例
            if isinstance(testcase_data, dict):
                # 尝试多种可能的键名（标准格式）
                for key in ['测试用例', 'testcases', '用例', '测试用例列表']:
                    test_cases = testcase_data.get(key, [])
                    if test_cases and isinstance(test_cases, list):
                        logger.info(f"✓ 从键 '{key}' 中提取到 {len(test_cases)} 条测试用例")
                        break
                
                # 如果还是没有找到，检查是否是嵌套结构（按测试点分组）
                if not test_cases:
                    logger.info("检测到嵌套结构，正在合并所有测试点的用例...")
                    all_test_cases = []
                    
                    for key, value in testcase_data.items():
                        if isinstance(value, list) and len(value) > 0:
                            # 检查列表中的元素是否是测试用例字典
                            first_item = value[0]
                            if isinstance(first_item, dict) and any(k in first_item for k in ['标题', 'title', '测试模块', 'module']):
                                # 为每个用例添加测试点名称作为模块标识
                                for case in value:
                                    if isinstance(case, dict):
                                        # 如果用例中没有模块信息，使用测试点名称
                                        if not case.get('测试模块') and not case.get('module'):
                                            case['测试模块'] = key
                                        all_test_cases.append(case)
                                
                                logger.info(f"  - 从测试点 '{key}' 中提取到 {len(value)} 条用例")
                    
                    test_cases = all_test_cases
                    if test_cases:
                        logger.info(f"✓ 共合并 {len(test_cases)} 条测试用例（来自 {len([k for k, v in testcase_data.items() if isinstance(v, list)])} 个测试点）")
                        
            elif isinstance(testcase_data, list):
                test_cases = testcase_data
                logger.info(f"✓ 直接使用列表数据，共 {len(test_cases)} 条测试用例")
            
            # 如果仍然没有找到，记录详细的调试信息
            if not test_cases:
                logger.error("没有找到有效的测试用例数据")
                logger.error(f"testcase_data类型: {type(testcase_data)}")
                logger.error(f"testcase_data内容预览: {str(testcase_data)[:500]}")
                if isinstance(testcase_data, dict):
                    logger.error(f"testcase_data的键: {list(testcase_data.keys())}")
                return False

            logger.info(f"准备写入 {len(test_cases)} 条测试用例到Excel")

            # 写入数据
            success = converter.write_data(test_cases)

            if success:
                logger.info(f"✓ 测试用例已成功导出到: {output_file}")
            else:
                logger.error("写入Excel失败")

            return success

        except Exception as e:
            logger.error(f"JSON转XLSX失败: {str(e)}", exc_info=True)
            return False



class interfaceTestPointToTestCaseXmind:
    """
    从测试点XMind一键生成测试用例XMind
    
    流程：
    1. AI生成测试点并保存为XMind和JSON
    2. XMind转JSON格式
    3. AI生成测试用例
    4. 测试用例转XMind
    """
    
    def __init__(self):
        """
        初始化转换器
        """
        self.test_point_interface = interfaceAITestPoint()
        self.xmind_converter = XmindPointJson()
        self.testcase_interface = interfaceAITestCaseXmind()
        self.file_processor = fileProcessor()
        logger.info("interfacePointToTestCaseXmind初始化完成")
    
    def generate_testcase_from_point(
        self,
        user_input: str,
        output_dir: str = None,
        xmind_output: str = None,
        test_point_json: str = None,
        xmind_json_output: str = None,
        testcase_json_output: str = None,
        testcase_xmind_output: str = None,
        storage_test_points: bool = True,
        extract_ai_format: bool = True,
        sleep_time: int = 5
    ) -> bool:
        """
        公开方法：从用户输入一键生成测试用例XMind
        
        Args:
            user_input: 用户输入的需求描述（必填）
            output_dir: 输出目录（可选，默认 D:\\AIGeneration\\testcase）
            xmind_output: 测试点XMind输出路径（可选）
            test_point_json: 测试点JSON保存路径（可选）
            xmind_json_output: XMind转JSON输出路径（可选）
            testcase_json_output: 测试用例JSON输出路径（可选）
            testcase_xmind_output: 测试用例XMind输出路径（可选）
            storage_test_points: 是否保存测试点到JSON文件（默认True）
            extract_ai_format: 是否提取为AI友好格式（默认True）
            sleep_time: AI调用间隔时间（秒，默认5秒）
            
        Returns:
            bool: 转换是否成功
            
        Raises:
            ValueError: 当参数无效时抛出
            Exception: 其他异常
        """
        # 入参校验
        if not user_input or not isinstance(user_input, str):
            logger.error("user_input参数不能为空且必须为字符串类型")
            raise ValueError("user_input参数不能为空且必须为字符串类型")
        
        if len(user_input.strip()) < 5:
            logger.error("user_input参数内容过短，至少需要5个字符")
            raise ValueError("user_input参数内容过短，至少需要5个字符")
        
        try:
            logger.info(f"{'='*60}")
            logger.info(f"开始执行测试点到测试用例的转换流程")
            logger.info(f"用户输入: {user_input[:50]}...")
            logger.info(f"{'='*60}")
            
            # 设置默认输出目录
            if not output_dir:
                output_dir = r"D:\AIGeneration\testcase"
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"创建输出目录: {output_dir}")
            
            # 设置默认文件路径
            if not xmind_output:
                xmind_output = os.path.join(output_dir, "output.xmind")
            if not test_point_json:
                test_point_json = os.path.join(output_dir, "测试点.json")
            if not xmind_json_output:
                xmind_json_output = os.path.join(output_dir, "output.json")
            if not testcase_json_output:
                testcase_json_output = os.path.join(output_dir, "测试用例_output.json")
            if not testcase_xmind_output:
                testcase_xmind_output = os.path.join(output_dir, "测试用例.xmind")
            
            # 步骤1: AI生成测试点
            logger.info(f"\n步骤1/4: AI生成测试点...")
            success = self._step1_generate_test_points(
                user_input=user_input,
                output_path=xmind_output,
                storage_json=test_point_json,
                storage_test_points=storage_test_points
            )
            if not success:
                logger.error("步骤1失败：AI生成测试点失败")
                return False
            
            # 步骤2: XMind转JSON
            logger.info(f"\n步骤2/4: 将测试点XMind转换为JSON...")
            test_point_data = self._step2_xmind_to_json(
                xmind_file=xmind_output,
                output_json=xmind_json_output
            )
            if not test_point_data:
                logger.error("步骤2失败：XMind转JSON失败")
                return False
            
            # 步骤3: AI生成测试用例
            logger.info(f"\n步骤3/4: AI生成测试用例（可能需要几分钟）...")
            success = self._step3_generate_testcases(
                input_file=xmind_json_output,
                output_path=testcase_json_output,
                extract=extract_ai_format,
                storage_file_path=testcase_json_output
            )
            if not success:
                logger.error("步骤3失败：AI生成测试用例失败")
                return False
            
            # 等待AI响应稳定
            if sleep_time > 0:
                logger.info(f"等待 {sleep_time} 秒...")
                time.sleep(sleep_time)
            
            # 步骤4: 测试用例转XMind
            logger.info(f"\n步骤4/4: 将测试用例JSON转换为XMind...")
            success = self._step4_testcase_to_xmind(
                testcase_json=testcase_json_output,
                output_xmind=testcase_xmind_output
            )
            if not success:
                logger.error("步骤4失败：测试用例转XMind失败")
                return False
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ 转换完成！")
            logger.info(f"测试点XMind: {xmind_output}")
            logger.info(f"测试用例XMind: {testcase_xmind_output}")
            logger.info(f"{'='*60}")
            print(f"\n✓ 测试用例XMind文件已成功生成: {testcase_xmind_output}")
            return True
            
        except ValueError as e:
            logger.error(f"参数错误: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"转换过程中发生错误: {str(e)}", exc_info=True)
            raise
    
    def _step1_generate_test_points(
        self,
        user_input: str,
        output_path: str,
        storage_json: str,
        storage_test_points: bool
    ) -> bool:
        """
        私有方法：步骤1 - 调用AI生成测试点并保存
        
        Args:
            user_input: 用户输入
            output_path: XMind输出路径
            storage_json: JSON保存路径
            storage_test_points: 是否保存JSON
            
        Returns:
            bool: 是否成功
        """
        try:
            self.test_point_interface.get_test_point(
                user_input=user_input,
                output_path=output_path,
                storage_json=storage_json,
                Storage_test_points=storage_test_points
            )
            
            # 验证文件是否生成
            if not os.path.exists(output_path):
                logger.error(f"测试点XMind文件未生成: {output_path}")
                return False
            
            logger.info(f"✓ 测试点XMind已生成: {output_path}")
            if storage_test_points and os.path.exists(storage_json):
                logger.info(f"✓ 测试点JSON已保存: {storage_json}")
            
            return True
            
        except Exception as e:
            logger.error(f"生成测试点失败: {str(e)}", exc_info=True)
            return False
    
    def _step2_xmind_to_json(
        self,
        xmind_file: str,
        output_json: str
    ) -> dict:
        """
        私有方法：步骤2 - 将XMind文件转换为JSON格式
        
        Args:
            xmind_file: XMind文件路径
            output_json: JSON输出路径
            
        Returns:
            dict: 转换后的JSON数据，失败返回空字典
        """
        try:
            # 验证XMind文件存在
            if not os.path.exists(xmind_file):
                logger.error(f"XMind文件不存在: {xmind_file}")
                return {}
            
            # 创建转换器并执行转换
            converter = XmindPointJson(xmind_file=xmind_file)
            result = converter.process_and_save(output_file=output_json)
            
            if not result:
                logger.error("XMind转JSON返回空结果")
                return {}
            
            logger.info(f"✓ XMind转JSON成功: {output_json}")
            return result
            
        except Exception as e:
            logger.error(f"XMind转JSON失败: {str(e)}", exc_info=True)
            return {}
    
    def _step3_generate_testcases(
        self,
        input_file: str,
        output_path: str,
        extract: bool,
        storage_file_path: str
    ) -> bool:
        """
        私有方法：步骤3 - 调用AI生成测试用例
        
        Args:
            input_file: 输入文件路径（测试点JSON）
            output_path: 输出路径
            extract: 是否提取为AI友好格式
            storage_file_path: 存储文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证输入文件存在
            if not os.path.exists(input_file):
                logger.error(f"输入文件不存在: {input_file}")
                return False
            
            success = self.testcase_interface.get_ai_testcase_write_json(
                user_input=input_file,
                output_path=output_path,
                extract=extract,
                storage_file_path=storage_file_path
            )
            
            if not success:
                logger.error("AI生成测试用例返回失败")
                return False
            
            # 验证输出文件是否生成
            if not os.path.exists(storage_file_path):
                logger.error(f"测试用例JSON文件未生成: {storage_file_path}")
                return False
            
            logger.info(f"✓ 测试用例JSON已生成: {storage_file_path}")
            return True
            
        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}", exc_info=True)
            return False
    
    def _step4_testcase_to_xmind(
        self,
        testcase_json: str,
        output_xmind: str
    ) -> bool:
        """
        私有方法：步骤4 - 将测试用例JSON转换为XMind
        
        Args:
            testcase_json: 测试用例JSON文件路径
            output_xmind: XMind输出路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证JSON文件存在
            if not os.path.exists(testcase_json):
                logger.error(f"测试用例JSON文件不存在: {testcase_json}")
                return False
            
            # 读取JSON数据
            testcase_data = self.file_processor.find_and_read_file(testcase_json, type="json")
            if not testcase_data:
                logger.error("读取测试用例JSON数据失败")
                return False
            
            # 转换并导出
            success = self.testcase_interface.converter.convert_and_export_to_xmind(
                input_data=testcase_data,
                output_xmind_file=output_xmind,
                root_title="测试用例",
                sheet_title="功能测试用例"
            )
            
            if not success:
                logger.error("转换XMind失败")
                return False
            
            # 验证XMind文件是否生成
            if not os.path.exists(output_xmind):
                logger.error(f"测试用例XMind文件未生成: {output_xmind}")
                return False
            
            logger.info(f"✓ 测试用例XMind已生成: {output_xmind}")
            return True
            
        except Exception as e:
            logger.error(f"测试用例转XMind失败: {str(e)}", exc_info=True)
            return False




class interfaceTestPointToAITestCaseXmind:
    """
    从测试点XMind文件一键生成测试用例XMind
    
    流程：
    1. XMind转JSON格式
    2. AI生成测试用例
    3. 测试用例转XMind
    """
    
    def __init__(self):
        """
        初始化转换器
        """
        self.xmind_converter = XmindPointJson()
        self.testcase_interface = interfaceAITestCaseXmind()
        self.file_processor = fileProcessor()
        logger.info("interfaceTestPointToAITestCaseXmind初始化完成")
    
    def convert_testpoint_to_testcase_xmind(
        self,
        xmind_file: str,
        output_dir: str = None,
        xmind_json_output: str = None,
        testcase_json_output: str = None,
        testcase_xmind_output: str = None,
        extract_ai_format: bool = True,
        sleep_time: int = 5
    ) -> bool:
        """
        公开方法：从测试点XMind文件一键生成测试用例XMind
        
        Args:
            xmind_file: 输入的测试点XMind文件路径（必填）
            output_dir: 输出目录（可选，默认与xmind_file同目录）
            xmind_json_output: XMind转JSON输出路径（可选）
            testcase_json_output: 测试用例JSON输出路径（可选）
            testcase_xmind_output: 测试用例XMind输出路径（可选）
            extract_ai_format: 是否提取为AI友好格式（默认True）
            sleep_time: AI调用间隔时间（秒，默认5秒）
            
        Returns:
            bool: 转换是否成功
            
        Raises:
            ValueError: 当参数无效时抛出
            FileNotFoundError: 当文件不存在时抛出
            Exception: 其他异常
        """
        # 入参校验
        if not xmind_file or not isinstance(xmind_file, str):
            logger.error("xmind_file参数不能为空且必须为字符串类型")
            raise ValueError("xmind_file参数不能为空且必须为字符串类型")
        
        if not os.path.exists(xmind_file):
            logger.error(f"XMind文件不存在: {xmind_file}")
            raise FileNotFoundError(f"XMind文件不存在: {xmind_file}")
        
        # 验证文件扩展名
        if not xmind_file.lower().endswith('.xmind'):
            logger.warning(f"输入文件可能不是XMind格式: {xmind_file}")
        
        try:
            logger.info(f"{'='*60}")
            logger.info(f"开始执行测试点XMind到测试用例XMind的转换")
            logger.info(f"输入文件: {xmind_file}")
            logger.info(f"{'='*60}")
            
            # 设置默认输出目录
            if not output_dir:
                output_dir = os.path.dirname(xmind_file)
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
                logger.info(f"创建输出目录: {output_dir}")
            
            # 设置默认文件路径
            base_name = os.path.splitext(os.path.basename(xmind_file))[0]
            if not xmind_json_output:
                xmind_json_output = os.path.join(output_dir, f"{base_name}.json")
            if not testcase_json_output:
                testcase_json_output = os.path.join(output_dir, "测试用例_output.json")
            if not testcase_xmind_output:
                testcase_xmind_output = os.path.join(output_dir, "测试用例.xmind")
            
            # 步骤1: XMind转JSON
            logger.info(f"\n步骤1/3: 将测试点XMind转换为JSON...")
            test_point_data = self._step1_xmind_to_json(
                xmind_file=xmind_file,
                output_json=xmind_json_output
            )
            if not test_point_data:
                logger.error("步骤1失败：XMind转JSON失败")
                return False
            
            # 步骤2: AI生成测试用例
            logger.info(f"\n步骤2/3: AI生成测试用例（可能需要几分钟）...")
            success = self._step2_generate_testcases(
                input_file=xmind_json_output,
                output_path=testcase_json_output,
                extract=extract_ai_format,
                storage_file_path=testcase_json_output
            )
            if not success:
                logger.error("步骤2失败：AI生成测试用例失败")
                return False
            
            # 等待AI响应稳定
            if sleep_time > 0:
                logger.info(f"等待 {sleep_time} 秒...")
                time.sleep(sleep_time)
            
            # 步骤3: 测试用例转XMind
            logger.info(f"\n步骤3/3: 将测试用例JSON转换为XMind...")
            success = self._step3_testcase_to_xmind(
                testcase_json=testcase_json_output,
                output_xmind=testcase_xmind_output
            )
            if not success:
                logger.error("步骤3失败：测试用例转XMind失败")
                return False
            
            logger.info(f"\n{'='*60}")
            logger.info(f"✓ 转换完成！")
            logger.info(f"输入: {xmind_file}")
            logger.info(f"输出: {testcase_xmind_output}")
            logger.info(f"{'='*60}")
            print(f"\n✓ 测试用例XMind文件已成功生成: {testcase_xmind_output}")
            return True
            
        except (ValueError, FileNotFoundError) as e:
            logger.error(f"参数或文件错误: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"转换过程中发生错误: {str(e)}", exc_info=True)
            raise
    
    def _step1_xmind_to_json(
        self,
        xmind_file: str,
        output_json: str
    ) -> dict:
        """
        私有方法：步骤1 - 将XMind文件转换为JSON格式
        
        Args:
            xmind_file: XMind文件路径
            output_json: JSON输出路径
            
        Returns:
            dict: 转换后的JSON数据，失败返回空字典
        """
        try:
            # 验证XMind文件存在
            if not os.path.exists(xmind_file):
                logger.error(f"XMind文件不存在: {xmind_file}")
                return {}
            
            # 创建转换器并执行转换
            converter = XmindPointJson(xmind_file=xmind_file)
            result = converter.process_and_save(output_file=output_json)
            
            if not result:
                logger.error("XMind转JSON返回空结果")
                return {}
            
            # 验证输出文件是否生成
            if not os.path.exists(output_json):
                logger.error(f"JSON文件未生成: {output_json}")
                return {}
            
            logger.info(f"✓ XMind转JSON成功: {output_json}")
            logger.info(f"  提取到 {len(result)} 个产品的测试点数据")
            return result
            
        except Exception as e:
            logger.error(f"XMind转JSON失败: {str(e)}", exc_info=True)
            return {}
    
    def _step2_generate_testcases(
        self,
        input_file: str,
        output_path: str,
        extract: bool,
        storage_file_path: str
    ) -> bool:
        """
        私有方法：步骤2 - 调用AI生成测试用例
        
        Args:
            input_file: 输入文件路径（测试点JSON）
            output_path: 输出路径
            extract: 是否提取为AI友好格式
            storage_file_path: 存储文件路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证输入文件存在
            if not os.path.exists(input_file):
                logger.error(f"输入文件不存在: {input_file}")
                return False
            
            success = self.testcase_interface.get_ai_testcase_write_json(
                user_input=input_file,
                output_path=output_path,
                extract=extract,
                storage_file_path=storage_file_path
            )
            
            if not success:
                logger.error("AI生成测试用例返回失败")
                return False
            
            # 验证输出文件是否生成
            if not os.path.exists(storage_file_path):
                logger.error(f"测试用例JSON文件未生成: {storage_file_path}")
                return False
            
            logger.info(f"✓ 测试用例JSON已生成: {storage_file_path}")
            
            # 读取并统计用例数量
            testcase_data = self.file_processor.find_and_read_file(storage_file_path, type="json")
            if testcase_data and isinstance(testcase_data, dict):
                test_cases = testcase_data.get('测试用例', [])
                logger.info(f"  共生成 {len(test_cases)} 条测试用例")
            
            return True
            
        except Exception as e:
            logger.error(f"生成测试用例失败: {str(e)}", exc_info=True)
            return False
    
    def _step3_testcase_to_xmind(
        self,
        testcase_json: str,
        output_xmind: str
    ) -> bool:
        """
        私有方法：步骤3 - 将测试用例JSON转换为XMind
        
        Args:
            testcase_json: 测试用例JSON文件路径
            output_xmind: XMind输出路径
            
        Returns:
            bool: 是否成功
        """
        try:
            # 验证JSON文件存在
            if not os.path.exists(testcase_json):
                logger.error(f"测试用例JSON文件不存在: {testcase_json}")
                return False
            
            # 读取JSON数据
            testcase_data = self.file_processor.find_and_read_file(testcase_json, type="json")
            if not testcase_data:
                logger.error("读取测试用例JSON数据失败")
                return False
            
            # 转换并导出
            success = self.testcase_interface.converter.convert_and_export_to_xmind(
                input_data=testcase_data,
                output_xmind_file=output_xmind,
                root_title="测试用例",
                sheet_title="功能测试用例"
            )
            
            if not success:
                logger.error("转换XMind失败")
                return False
            
            # 验证XMind文件是否生成
            if not os.path.exists(output_xmind):
                logger.error(f"测试用例XMind文件未生成: {output_xmind}")
                return False
            
            logger.info(f"✓ 测试用例XMind已生成: {output_xmind}")
            
            # 显示文件大小
            file_size = os.path.getsize(output_xmind)
            logger.info(f"  文件大小: {file_size / 1024:.2f} KB")
            
            return True
            
        except Exception as e:
            logger.error(f"测试用例转XMind失败: {str(e)}", exc_info=True)
            return False


if __name__ == '__main__':

    converter = interfaceTestPointToAITestCaseXmind()

    # 只需提供XMind文件路径，其他全部使用默认值
    success = converter.convert_testpoint_to_testcase_xmind(
        xmind_file=r"D:\AIGeneration\testcase\output.xmind"
    )

    if success:
        print("✓ 转换成功！")
    # 生成测试点xmind和json
    # interfaceAITestPoint().get_test_point(user_input="电商下单界面功能",
    #                                       output_path=r"D:\AIGeneration\testcase\output.xmind",
    #                                       storage_json=r"D:\AIGeneration\testcase\测试点.json")

    # converter = XmindPointJson(xmind_file=r"D:/AIGeneration/testcase/output.xmind")
    # result = converter.process_and_save(output_file=r"D:/AIGeneration/testcase/output.json")

    #  #测试用例
    #  interfaceAITestCaseXmind().get_ai_testcase_write_json(user_input=r'D:\AIGeneration\testcase\output.json',
    #                                     output_path=r'D:\AIGeneration\testcase\测试转化数据.json',
    #                                     extract=True,
    #                                     storage_file_path=r'D:\AIGeneration\testcase\测试用例_output.json'
    #                                     )
    #  time.sleep(5)
    #  interfaceAITestCaseXmind().get_testcase_xmind()




    # converter = TestPointXmindToTestcaseXlsx()
    #
    # success = converter.convert_xmind_to_testcase_xlsx(
    #     xmind_file=r"D:\AIGeneration\testcase\output.xmind",
    #     output_xlsx_file=r"D:\AIGeneration\testcase\测试用例.xlsx",
    #     temp_json_dir=r"D:\AIGeneration\testcase"
    # )

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



    # converter = interfaceAIAnyFlieToXlsx()
    # # 高级用法 - 自定义所有路径
    # success = converter.generate_testcase_xlsx_from_text(
    #     user_input="用户登录注册功能",
    #     output_dir=r"D:\MyProject",
    #     test_point_file=r"D:\MyProject\testpoints.json",
    #     testcase_file=r"D:\MyProject\testcases.json",
    #     xmind_file=r"D:\MyProject\testcases.xmind",
    #     xlsx_file=r"D:\MyProject\testcases.xlsx"
    # )