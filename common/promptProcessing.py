# 拼接提示词
import yaml
from common.fileProcessor import fileProcessor

def get_prompt():
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
    template_prompt = origin_data.get("text") + origin_data.get("promptTemplate") + origin_data.get("format")
    user_input = "新年红包"
    prompt = " ".join([user_input, template_prompt ])
    return prompt

