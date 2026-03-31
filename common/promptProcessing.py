# 拼接提示词
import yaml
from common.fileProcessor import fileProcessor

def get_prompt():
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
    template_prompt = origin_data.get("text") + origin_data.get("promptTemplate") + origin_data.get("format")
    user_input = "杯子"
    prompt = " ".join([user_input, template_prompt ])
    return prompt


def get_testcase(prompt_input):
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
    template_prompt = origin_data.get("testcasePrompt")
    prompt = " ".join([prompt_input, template_prompt])
    return prompt



if __name__ == '__main__':
    prompt_input = "{'测试模块1': ['功能可靠', '性能安全', '使用方便'], '测试模块2': ['优化好', '便利好用', '经典红']}"
    print(get_testcase(prompt_input))