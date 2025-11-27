#调用deepseekAPI接口
import os
from openai import OpenAI

class DeepSeekAPI:

    def __init__(self, question):
        self.DEEPSEEK_API_KEY = r"sk-5822942360b0414eae1134f5b5aaa69a"
        self.MODEL_NAME = "deepseek-chat"
        self.userName = "user"
        self.language = "Chinese"
        self.requestQuestion = promoptchars + question

    def get_answer(self):
        client = OpenAI(
            api_key = DEEPSEEK_API_KEY,
            base_url = "https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model = MODEL_NAME
            , messages = [
                {"role": "system", "content": f"You are a helpful assistant. Please respond in {self.language}"},
                {"role": self.userName, "content": self.requestQuestion}
            ]
            , stream = False
        )
        result = response.choices[0].message.content
        return result

