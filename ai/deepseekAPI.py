#调用deepseekAPI接口
import os
from openai import OpenAI
from common.promptProcessing import get_prompt,get_testcase
from common.fileProcessor import fileProcessor

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


    def get_ai_point(self,user_input):
        self.requestQuestion = get_point(user_input)
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
    print(DeepSeekAPI().get_testcase_answer())

