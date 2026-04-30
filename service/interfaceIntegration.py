from service.xmindChanger import *
from ai.deepseekAPI import *
from common.promptProcessing import fileProcessor
import os
import json
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
    def get_ai_testcase_write_json(self, user_input, output_path,extract, storage_file_path):
        user_input = self.ai_test_input.get_test_case_template(user_input, output_path, extract)
        if not user_input:
            print("没有获取到测试用例模板数据")
            return False
        ds_res = self.DS.get_testcase_answer(user_input)
        if ds_res:
            #数据存在写入文件中
            self.get_json.write_file(storage_file_path, ds_res, "json")
        print("执行完毕")

    def get_testcase_xmind(self):
        print("\n=== 测试用例JSON转化成xmind")
        # 读取测试用例JSON文件
        testcase_json_path = r"D:\AIGeneration\testcase\测试用例.json"
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





"""
ai生成测试用例接口
支持手动输入测试点列表
导出为测试用例xmind

默认模板
要支持自定义模板

"""


"""
ai生成测试用例接口
支持手动输入测试点列表
导出为测试用例xlsx

默认模板
要支持自定义模板

"""


"""
测试用例xmind导出为xlsx
支持手动上传xmind文件
导出为测试用例xlsx

默认模板
要支持自定义模板

"""



"""
管理日志接口
"""



"""
管理配置接口
"""



"""
管理提示词配置接口
"""

if __name__ == '__main__':
     interfaceAITestCaseXmind().get_ai_testcase_write_json(user_input=r'D:\AIGeneration\testcase\测试点.json',
                                        output_path=r'D:\AIGeneration\testcase\测试转化数据.json',
                                        extract=False,
                                        storage_file_path=r'D:\AIGeneration\testcase\测试用例_output.json'
                                        )

    # interfaceAITestPoint().get_test_point(user_input="LCD光固化3D打印机，带Z轴，功能有加热功能，曝光时间，延时打印，中断打印续打，支持多种树脂打印,支持连接app", output_path=r"D:\AIGeneration\testcase\output.xmind", storage_json=r"D:\AIGeneration\testcase\测试点.json")