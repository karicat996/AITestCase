# mxind数据转换器
import xmind
from utils.logs import LogManager
from loguru import logger
import pandas
import openpyxl


class MxindDataProcessor:
    def __init__(self):
        self.xmind_file = r"C:\Users\admin\Desktop\test.xmind"
        self.logging = LogManager()
        self.case_dict = {}
    def xmind_to_json(self):
        workbook = xmind.load(self.xmind_file)
        sheet = workbook.getData()
        logger.debug("调试信息")
        if sheet:
            logger.debug("调试信息")
            return sheet[0]


class AdvancedTestCaseExtractor:

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


class DicToXlsx:
    """
    将字典数据转换为XLSX文件
    """

    def __init__(self, dic, xlsx_file):
        self.dic = dic
        self.xlsx_file = xlsx_file

    def convert(self):
        """
        将字典数据转换为XLSX文件
        """
        workbook = xlsxwriter.Workbook(self.xlsx_file)
        worksheet = workbook


if __name__ == '__main__':
    json_data = MxindDataProcessor().xmind_to_json()
    extractor = AdvancedTestCaseExtractor(max_depth=10)
    results = extractor.extract(json_data)
    total = extractor.get_statistics()
    print(results)