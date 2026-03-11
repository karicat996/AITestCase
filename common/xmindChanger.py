# mxind数据转换器
import xmind
from utils.logs import LogManager
from loguru import logger
import pandas as pd
from openpyxl import Workbook, load_workbook
import os
from common.dataProcessor import WriteInfo

class MxindDataProcessor:#  xmind数据整理
    def __init__(self):
        self.xmind_file = r"C:\Users\admin\Desktop\demo.xmind"
        self.logging = LogManager()
        self.case_dict = {}
    def xmind_to_json(self):
        workbook = xmind.load(self.xmind_file)
        sheet = workbook.getData()
        logger.debug("调试信息")
        if sheet:
            logger.debug("调试信息")
            return sheet[0]


class AdvancedTestCaseExtractor: #测试用例数据提取

    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.results = []

    def extract(self, json_obj):
        """
        提取测试用例数据
        """
        self.results = []
        root_topic = json_obj.get('topic', {})

        if root_topic:
            # 从根节点开始遍历，传递路径信息
            self._traverse_with_path(root_topic, [], 1)

        return self.results

    def _traverse_with_path(self, node, path, level):
        """
        带路径信息的遍历方法 - 基于层级位置判断
        """
        if self.max_depth is not None and level > self.max_depth:
            return

        # 更新路径
        current_path = path + [node]

        # 基于层级位置判断节点类型
        # 假设结构：第1层为产品名，第2层为模块名，第3层为测试用例
        if level == 4:  # 测试用例节点位于第3层
            # 创建基础测试用例信息
            test_case_info = self._create_test_case_dict_by_position(node, current_path, level)

            # 获取按步骤拆分后的结果
            split_entries = self._extract_steps_and_results_by_position(node, test_case_info)

            if split_entries:
                # 添加拆分后的条目
                self.results.extend(split_entries)
            else:
                # 如果没有子节点，添加原始条目
                self.results.append(test_case_info)

        # 递归处理子节点
        for child in node.get('topics', []):
            self._traverse_with_path(child, current_path, level + 1)

    def _create_test_case_dict_by_position(self, test_case_node, path, level):
        """
        根据节点在树中的位置创建测试用例字典
        """
        subject = ''
        model = ''

        #  这里处理节点的属性，例如主题、模型等
        if len(path) >= 1:
            subject = path[0].get('title', '')
        if len(path) >= 2:
            model = path[1].get('title', '')
        if len(path) >= 3:
            title = path[2].get('title', '')
        if len(path) >= 4:
            header = path[3].get('title', '')
        return {
            'Subject': subject,
            'model': model,
            'title': title,
            'header': header,
            'steps': '',
            'result': ''
        }

    def _extract_steps_and_results_by_position(self, test_case_node, test_case_info):
        """
        基于位置提取测试步骤和预期结果
        假设第一层子节点是步骤，第二层子节点是对应的结果
        """
        new_entries = []

        # 获取子节点（假设为测试步骤）
        child_nodes = test_case_node.get('topics', [])

        for step_node in child_nodes:
            # 获取步骤节点的子节点（假设为预期结果）
            result_nodes = step_node.get('topics', [])

            if result_nodes:
                # 对每个结果节点创建一个条目
                for result_node in result_nodes:
                    new_entry = {
                        'Subject': test_case_info['Subject'],
                        'model': test_case_info['model'],
                        'title': test_case_info['title'],
                        'header': test_case_info['header'],
                        'steps': step_node.get('title', ''),
                        'result': result_node.get('title', '')
                    }
                    new_entries.append(new_entry)
            else:
                # 如果步骤节点没有结果子节点
                new_entry = {
                    'Subject': test_case_info['Subject'],
                    'model': test_case_info['model'],
                    'title': test_case_info['title'],
                    'header': test_case_info['header'],
                    'steps': step_node.get('title', ''),
                    'result': ''
                }
                new_entries.append(new_entry)

        return new_entries

    def get_statistics(self):
        """
        获取提取结果的统计信息

        Returns:
            dict: 统计信息
        """
        if not self.results:
            return {'total_cases': 0}

        total_steps = len(self.results)  # 每个条目代表一个步骤-结果对
        total_results = len(self.results)

        data = {
            'total_cases': len(self.results),
            'total_steps': total_steps,
            'total_results': total_results
        }

        print(data)

class DicToXlsx: # 字典转换成用例
    def __init__(self):
        self.xlsx_file = r'C:\Users\admin\Desktop\demo.xlsx'
        file_dir = os.path.dirname(self.xlsx_file)
        if file_dir and not os.path.exists(file_dir):  # 只有当目录不存在时才创建
            os.makedirs(file_dir, exist_ok=True)
        json_data = MxindDataProcessor().xmind_to_json()
        extractor = AdvancedTestCaseExtractor(max_depth=10)
        self.data = extractor.extract(json_data)
        statistics = extractor.get_statistics()
        print(f"提取到的数据: {len(self.data)} 条")

    def table_data_processing(self):
        try:
            # 如果文件不存在，则创建新的工作簿并设置表头
            if not os.path.exists(self.xlsx_file):
                wb = Workbook()
                sheet = wb.active
                # 定义中文表头
                headers_chinese = ['主题', '模块', '标题', '前置条件', '步骤', '预期结果']
                for col_num, header in enumerate(headers_chinese, 1):
                    sheet.cell(row=1, column=col_num, value=header)
                # 设置表头行高
                sheet.row_dimensions[1].height = 25
                wb.save(self.xlsx_file)
                print(f"已创建新文件并写入表头: {self.xlsx_file}")

            # 加载现有的工作簿
            wb = load_workbook(self.xlsx_file)
            sheet = wb.active

            # 检查表头是否已经存在，如果不存在则添加
            first_cell = sheet.cell(row=1, column=1).value
            headers_chinese = ['主题', '模块', '标题', '前置条件', '步骤', '预期结果']

            # 检查第一列是否包含期望的表头值之一
            if not first_cell or first_cell not in headers_chinese:
                # 重新写入表头
                for col_num, header in enumerate(headers_chinese, 1):
                    sheet.cell(row=1, column=col_num, value=header)
                print("已写入表头到第一行")

            # 获取现有数据的最后一行
            last_row = sheet.max_row
            # 定义英文键名用于从数据字典中获取值
            headers_english = ['Subject', 'model', 'title', 'header', 'steps', 'result']

            # 遍历数据数组，逐行写入
            for row_idx, data_dict in enumerate(self.data, start=last_row + 1):
                for col_idx, header in enumerate(headers_english, start=1):
                    # 从字典中获取对应键的值，如果键不存在则写入空字符串
                    value = data_dict.get(header, '')
                    sheet.cell(row=row_idx, column=col_idx, value=value)

            # 保存工作簿
            wb.save(self.xlsx_file)
            print(f"数据已成功写入: {self.xlsx_file}")

        except PermissionError:
            print(f"权限错误：无法访问文件 {self.xlsx_file}，请确保文件未被其他程序打开")
        except Exception as e:
            print(f"写入Excel文件时发生错误: {str(e)}")



#xmind测试点转化json



#xmind测试用例转换成

if __name__ == '__main__':
    # dic_to_xlsx = DicToXlsx()
    # dic_to_xlsx.table_data_processing()
    dc = MxindDataProcessor()
    res = dc.xmind_to_json()
    DD = WriteInfo()
    DD.write_json_to_file(data=res, file=r"D:\AIGeneration\testcase\demo.json")
