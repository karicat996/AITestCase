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


"""
ai生成测试点接口
支持手动输入内容
导出为测试点xmind

默认模板
要支持自定义模板

"""



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
    interfaceAITestPoint().get_test_point(user_input="LCD光固化3D打印机，带Z轴，功能有加热功能，曝光时间，延时打印，中断打印续打，支持多种树脂打印,支持连接app", output_path=r"D:\AIGeneration\testcase\output.xmind", storage_json=r"D:\AIGeneration\testcase\测试点.json")