# 拼接提示词
import yaml
from common.fileProcessor import fileProcessor

def get_prompt(user_input):
    if user_input is None:
        logger.error("输入内容为空")
    else:
        fp = fileProcessor()
        origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
        template_prompt = origin_data.get("text") + origin_data.get("promptTemplate") + origin_data.get("format")
        prompt = " ".join([user_input, template_prompt])
        return prompt


def get_testcase(prompt_input):
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
    template_prompt = origin_data.get("testcasePrompt")
    prompt_input = "{'测试模块1': ['功能可靠', '性能安全', '使用方便'], '测试模块2': ['优化好', '便利好用', '经典红']}"
    prompt = " ".join([prompt_input, template_prompt])
    return prompt



if __name__ == '__main__':
    print(get_testcase(prompt_input))