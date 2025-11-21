#调用deepseekAPI接口
import os
from openai import OpenAI

DEEPSEEK_API_KEY = r"sk-5822942360b0414eae1134f5b5aaa69a"
MODEL_NAME = "deepseek-chat"
userName = "user"
language = "Chinese"
requestQuestion = promoptchars + question

client = OpenAI(
    api_key = DEEPSEEK_API_KEY,
    base_url = "https://api.deepseek.com"
)
response = client.chat.completions.create(
    model = MODEL_NAME
    , messages = [
        {"role": "system", "content": f"You are a helpful assistant. Please respond in {language}"},
        {"role": userName, "content": requestQuestion}
    ]
    , stream = False
)


print(response.choices[0].message.content)