# 拼接提示词
import yaml
from os import path
from common.fileProcessor import fileProcessor
from loguru import logger
from utils.logs import LogManager
from common.textRecognition import *
# 初始化日志配置（指定日志输出到文件夹）
LogManager(log_dir=r"D:\AIGeneration\utils\logs")

def get_prompt(user_input):
    if user_input is None:
        logger.error("输入内容为空")
        return None
    
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")
    
    if origin_data is None:
        logger.error("读取 promptWord.yaml 失败，请检查文件路径或格式")
        return None
        
    try:
        template_prompt = str(origin_data.get("text", "")) + str(origin_data.get("promptTemplate", "")) + str(origin_data.get("format", ""))
        prompt = " ".join([user_input, template_prompt])
        return prompt
    except Exception as e:
        logger.error(f"拼接提示词出错: {str(e)}")
        return None


def get_testcase(prompt_input):
    if prompt_input is None:
        logger.error("输入内容为空")
        return None
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")

    if origin_data is None:
        logger.error("读取 promptWord.yaml 失败，请检查文件路径或格式")
        return None
    try:
        template_prompt = str(origin_data.get("testcasePrompt", ""))
        # prompt_input = "{'测试模块1': ['功能可靠', '性能安全', '使用方便'], '测试模块2': ['优化好', '便利好用', '经典红']}"
        prompt = " ".join([template_prompt,prompt_input])
        return prompt
    except Exception as e:
        logger.error(f"拼接测试用例提示词出错: {str(e)}")
        return None


def get_point(image_path):
    if image_path is None or not path.exists(image_path):
        logger.error("输入地址为空或文件不存在")
        return None
    fp = fileProcessor()
    origin_data = fp.find_and_read_file("config/promptWord.yaml", type="yaml")

    if origin_data is None:
        logger.error("读取 promptWord.yaml 失败，请检查文件路径或格式")
        return None
    try:
        result = ocr_get_text_from_img(image_path)
        res = result.get("text")
        str_input = ''.join(res)
        template_prompt = str(origin_data.get("testpointPrompt", ""))
        prompt = " ".join([template_prompt,str_input])
        return prompt
    except Exception as e:
        logger.error(f"拼接测试用例提示词出错: {str(e)}")
        return None





if __name__ == '__main__':
    print(get_point(image_path=r"D:\AIGeneration\config\de.png"))