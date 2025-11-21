# 将json格式转化成xmind格式
import json
import os



class DataProcess:

    def __init__(self):
        json_path = r""
        markdown_path = r""

    # 读取json文件数据
    def read_json(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            demo_data = json.load(f)
            return demo_data


    # 递归将JSON数据转换为Markdown格式
    def json_to_markdown(data, level=0):
        """
        递归地将JSON数据转换为Markdown格式
        """
        # 定义缩进配置
        INDENT_UNIT = "    "  # 4个空格作为一个缩进单位
        markdown_content = ""
        current_indent = INDENT_UNIT * level

        # 首先判断是否是字典，列表，字符串，数字，None
        if isinstance(data, dict):
            # 遍历字典的键值对
            # 特殊处理测试用例对象
            if 'title' in data:
                # 按照目标格式逐级缩进
                markdown_content += f"{current_indent}- {data.get('id', '')}\n"
                markdown_content += f"{current_indent}{INDENT_UNIT}- {data.get('title', '')}\n"
                markdown_content += f"{current_indent}{INDENT_UNIT * 2}- {data.get('description', '')}\n"

                # 处理步骤数组
                steps = data.get('steps', [])
                if steps:
                    steps_text = " ".join([f"{i + 1}.{step}" for i, step in enumerate(steps)])
                    markdown_content += f"{current_indent}{INDENT_UNIT * 3}- {steps_text}\n"

                # 处理预期结果
                expected = data.get('expected_result', '')
                if expected:
                    markdown_content += f"{current_indent}{INDENT_UNIT * 4}- {expected}\n"
            else:
                # 普通字典处理
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        markdown_content += f"{current_indent}- **{key}**:\n"
                        markdown_content += json_to_markdown(value, level + 1)
                    else:
                        markdown_content += f"{current_indent}- **{key}**: {value}\n"
        elif isinstance(data, list):
            for index, item in enumerate(data):
                markdown_content += f"{current_indent}{index + 1}.\n"
                markdown_content += json_to_markdown(item, level + 1)
        elif isinstance(data, str):
            markdown_content += f"{current_indent}{data}\n"
        elif isinstance(data, int):
            markdown_content += f"{current_indent}{data}\n"
        else:
            markdown_content += f"{current_indent}{data}\n"

        return markdown_content


     # 将JSON转换为Markdown文件
    def json_to_markdown_file(json_data, output_file):
        # 创建Markdown内容
        markdown_content = "# JSON数据转换结果\n\n"
        markdown_content += "## 测试用例\n\n"
        markdown_content += json_to_markdown(json_data)

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # 写入文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"Markdown文件已生成: {output_file}")


# if __name__ == "__main__":
#     # 读取JSON数据
#     demo_data = read_json(json_path)
#
#     # 转换为Markdown
#     json_to_markdown_file(demo_data, markdown_path)
#
#     # 打开文件
#     os.system(f"start {markdown_path}")