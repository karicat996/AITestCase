#调用deepseekAPI接口
import os
from openai import OpenAI
from common.promptProcessing import get_prompt
from common.fileProcessor import fileProcessor
class DeepSeekAPI:

    def __init__(self, question):
        fp = fileProcessor()
        self.DEEPSEEK_API_KEY = fp.find_and_read_file("config/userInfo.yaml", type="yaml").get("DEEPSEEK_API_KEY")
        self.MODEL_NAME = "deepseek-chat"
        self.userName = "user"
        self.language = "Chinese"
        self.requestQuestion = get_prompt()

    def get_answer(self):
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
        print(result)
        # return result


if __name__ == '__main__':
    print(DeepSeekAPI("").get_answer())

