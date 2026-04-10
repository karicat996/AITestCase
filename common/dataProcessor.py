import json
import os
import re
from ai.deepseek3 import DeepSeekAPI
from common.fileProcessor import fileProcessor


#将json数据转化为markdown,再转化为
class DataProcess:

    def __init__(self):
        self.ds = DeepSeekAPI().get_test_point_answer()
        self.ts = fileProcessor().find_and_read_file("config/template.json", type="json")

    def extract_json_from_ai_response(self,text):
        pattern = r"```json\s*({[\s\S]*?})\s*```"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            json_str = match.group(1)
            # 修复双大括号问题
            valid_json = json_str.replace("{{", "{").replace("}}", "}")
            return valid_json  # 获得可解析的标准JSON
        else:
            raise ValueError("未匹配到JSON")

    def testpoint_to_list(self, data):
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


    def json_to_markdown(self, data=None, output_file=None, level=0):
      """
      递归地将JSON数据转换为Markdown格式并写入文件
      """
      if data is None:
        data = self.ds
        extracted_json = self.extract_json_from_ai_response(data)
        if extracted_json:
          data = json.loads(extracted_json) # 解析提取的JSON
        else:
          print("无法从数据中提取JSON内容")
      with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 测试点\n\n") # 添加标题
        self._write_markdown_recursive(data, f, level) # 递归处理数据
        print("数据已写入文件：", output_file)

    def _write_markdown_recursive(self, data, file_handle, level=0):
      """
      递归写入Markdown格式数据
      """
      indent = "#" * (level + 2)  # 使用标题层级
      if isinstance(data, dict):
        for key, value in data.items():
          if isinstance(value, (dict, list)):
            # 写入标题
            file_handle.write(f"{indent} {key}\n\n")
            # 递归处理子元素
            self._write_markdown_recursive(value, file_handle, level + 1)
          else:
            # 简单键值对
            file_handle.write(f"{indent} {key}: {value}\n\n")
      elif isinstance(data, list):
        for item in data:
          if isinstance(item, (dict, list)):
            file_handle.write(f"\n")
            self._write_markdown_recursive(item, file_handle, level + 1)
          else:
            # 列表项使用Markdown列表格式
            file_handle.write(f"{indent} {item}\n")
        file_handle.write("\n")

    # 针对测试用例
    def json_to_testcase(self, data=None, output_file=None, level=0):
      """
      将JSON数据转换为测试用例格式并写入文件
      """
      if data is None:
        data = self.ts

      with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 测试用例\n\n")  # 添加标题
        self._write_testcase_recursive(data, f, level)

    def _write_testcase_recursive(self, data=None, file_handle=None, level=0):

      # 定义标题级别映射
      title_levels = {
        "测试模块": 2,  # ## 级别
        "标题": 3,  # ### 级别
        "前置条件": 4,  # #### 级别
        "操作步骤": 5,  # ##### 级别
        "预期结果": 6  # ###### 级别
      }

      if isinstance(data, dict):
        for key, value in data.items():
          if key in title_levels:
            level_num = title_levels[key]
            indent = "#" * level_num

            if key == "前置条件" or key == "操作步骤" or key == "预期结果":
              # 对于列表类型的值，将其连接为一行
              if isinstance(value, list):
                formatted_items = " ".join([f"{i + 1}.{item}" for i, item in enumerate(value)])
                file_handle.write(f"{indent} {formatted_items}\n\n")
            else:
              # 对于非列表类型的值，直接输出
              file_handle.write(f"{indent} {value}\n\n")
          elif isinstance(value, (dict, list)):
            # 递归处理其他嵌套结构
            self._write_testcase_recursive(value, file_handle, level)
      elif isinstance(data, list):
        for item in data:
          if isinstance(item, dict):
            self._write_testcase_recursive(item, file_handle, level)
          elif isinstance(item, list):
            # 处理嵌套列表
            for sub_item in item:
              file_handle.write(f"{sub_item}\n")
          else:
            # 列表项处理
            file_handle.write(f"{item}\n")


class WriteInfo:
    def write_json_to_file(self, data, file):#将数据写入json文件中
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"数据已成功写入文件：{file}")
        except Exception as e:
            print(f"写入文件时发生错误：{e}")
            raise



if __name__ == "__main__":
    # 转换为Markdown
    dc = DataProcess()
    # 转换为Markdown
    # dc.json_to_markdown(output_file=r"D:\AIGeneration\config\answer.md")
    dc.testpoint_to_list(fp)
    # dc.json_to_testcase(output_file=r"D:\AIGeneration\testcase\testcase.md")

