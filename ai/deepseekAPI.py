#调用deepseekAPI接口
import os
import json
from openai import OpenAI
from utils.logs import LogManager
from loguru import logger
from common.promptProcessing import get_prompt,get_testcase,get_point
from common.fileProcessor import fileProcessor
LogManager(log_dir=r"D:\AIGeneration\utils\logs")
class DeepSeekAPI:

    def __init__(self):
        fp = fileProcessor()
        # 延迟导入，避免循环依赖
        self.DEEPSEEK_API_KEY = fp.find_and_read_file("config/systemConfig.yaml", type="yaml").get("DEEPSEEK_API_KEY")
        self.MODEL_NAME = "deepseek-chat"
        self.userName = "user"
        self.language = "Chinese"

    def get_test_point_answer(self,user_input):
        self.requestQuestion = get_prompt(user_input)
        client = OpenAI(
            api_key =self.DEEPSEEK_API_KEY,
            base_url = "https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model = self.MODEL_NAME
            , messages = [
                {"role": "system", "content": f"You are a helpful assistant. Please respond in {self.language}"},
                {"role": self.userName, "content": self.requestQuestion}
            ]
            , stream = False
        )
        result = response.choices[0].message.content
        print(f"获取到答案:{result}")
        return result

    def get_testcase_answer(self,prompt_input):
        self.testcaseQuestion = get_testcase(prompt_input)
        print("已发送测试用例生成请求，等待生成....")
        client = OpenAI(
            api_key =self.DEEPSEEK_API_KEY,
            base_url = "https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model = self.MODEL_NAME
            , messages = [
                {"role": "system", "content": f"You are a helpful assistant. Please respond in {self.language}"},
                {"role": self.userName, "content": self.testcaseQuestion}
            ]
            , stream = False
        )
        result = response.choices[0].message.content
        print(type(result))
        print(f"获取到答案:{result}")
        return result

    def get_ai_point(self,image_path):
        """
        从图像中提取文本并生成测试关键词（第一步：图片→关键词）
        :param image_path: 图像文件路径
        :return: AI生成的测试关键词结果
        """
        self.requestQuestion = get_point(image_path)
        if self.requestQuestion is None:
            logger.error("获取图像测试点提示词失败")
            return None
        
        print("已发送关键词提取请求，等待生成....")
        client = OpenAI(
            api_key =self.DEEPSEEK_API_KEY,
            base_url = "https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model = self.MODEL_NAME
            , messages = [
                {"role": "system", "content": f"You are a helpful assistant. Please respond in {self.language}"},
                {"role": self.userName, "content": self.requestQuestion}
            ]
            , stream = False
        )
        result = response.choices[0].message.content
        print(f"获取到关键词:{result}")
        return result
    def point_to_list(self, data= None):
        """
        将测试点数据转换为列表
        """
        test_points = []
        if isinstance(data, dict):
            for item in data.values():
                if isinstance(item, dict):
                    # 接收递归调用的返回值
                    test_points.extend(self.testpoint_to_list(item))
                elif isinstance(item, list):
                    for point in item:
                        test_points.append(point)
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    test_points.extend(self.testpoint_to_list(item))
                elif isinstance(item, list):
                    for point in item:
                        test_points.append(point)
        else:
            # 处理基本数据类型
            pass
        return test_points

if __name__ == '__main__':
    api = DeepSeekAPI()

