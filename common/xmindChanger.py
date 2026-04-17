# mxind数据转换器
import xmind
import json
import uuid
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






def _build_xmind_topic(xmind_topic, data):
    """
    递归构建 XMind 主题

    Args:
        xmind_topic: XMind 主题对象
        data: 数据字典或字符串
    """
    if isinstance(data, str):
        xmind_topic.setTitle(data)
    elif isinstance(data, dict):
        # 设置当前主题标题
        title = data.get('title', data.get('name', ''))
        if title:
            xmind_topic.setTitle(title)

        # 处理子主题
        topics = data.get('topics', data.get('children', []))
        if topics and isinstance(topics, list):
            for child_data in topics:
                child_topic = xmind_topic.addSubTopic()
                _build_xmind_topic(child_topic, child_data)

        # 处理备注信息（如果有）
        notes = data.get('notes', data.get('comment', ''))
        if notes:
            xmind_topic.setNote(notes)

        # 处理测试用例的特殊字段
        if 'steps' in data or 'result' in data:
            note_content = ""
            if 'steps' in data and data['steps']:
                note_content += f"步骤：{data['steps']}\n"
            if 'result' in data and data['result']:
                note_content += f"预期结果：{data['result']}\n"
            if note_content:
                existing_note = xmind_topic.getNote()
                if existing_note:
                    xmind_topic.setNote(f"{existing_note}\n{note_content}")
                else:
                    xmind_topic.setNote(note_content)
    elif isinstance(data, list):
        # 如果是列表，第一个元素作为标题，其余作为子主题
        if len(data) > 0:
            xmind_topic.setTitle(str(data[0]))
            for item in data[1:]:
                child_topic = xmind_topic.addSubTopic()
                _build_xmind_topic(child_topic, item)


# 测试点的xmind 转化 json
class XmindPointJson:

    def __init__(self):
        self.xmind_file = r"C:\Users\admin\Desktop\test.xmind"

    def readXmindData(self):
        workbook = xmind.load(self.xmind_file)
        sheet = workbook.getData()
        if not sheet:
            print("模板文件中没有工作表")
            return None
        else:
            JsonData = sheet[0]
            print(JsonData)
        return JsonData

    def extract_test_points_data(self):
        """
        从给定的数据中提取测试点和其子项，生成新的JSON格式

        Args:
            data: 包含原始数据的字典

        Returns:
            dict: 新的JSON格式数据，格式为 {"测试点1": ["功能可靠", "性能安全", "使用方便"], "测试点2": [...]}
        """
        # 创建新的结果字典
        result = {}
        data = self.readXmindData()
        # 遍历主题下的topics获取测试点
        topics = data.get('topic', {}).get('topics', [])

        for topic in topics:
            test_point_title = topic.get('title')  # 测试点标题，如"测试点1"

            # 获取该测试点下的所有子主题
            sub_topics = topic.get('topics', [])
            sub_titles = [sub_topic.get('title') for sub_topic in sub_topics]

            # 将测试点作为键，子项列表作为值添加到结果中
            result[test_point_title] = sub_titles

        print(result)


class JsonToXmind:
    #获取测试点转化为xmind格式文件
    def primaryJsonToTrueJson(self,json_data):
        pass

    def json_to_xmind(self,json_data, output_file,template_file=None):
        try:
            # 创建新的 XMind 工作簿
            if template_file is None:
                template_file = os.path.join(os.path.dirname(__file__), 'template.xmind')
                # 若默认模板不存在，则回退到项目 config 目录的 template.json 对应的空 xmind（需要你提前准备）
                if not os.path.exists(template_file):
                    template_file = r"C:\Users\admin\Desktop\test.xmind"  # 你需要在本地准备这个空白模板

                # 加载模板工作簿
            workbook = xmind.load(template_file)
            # sheets = workbook.getData()
            sheet = workbook.getPrimarySheet()
            if not sheet:
                print("模板文件中没有工作表")
                return False


            # 设置工作表标题
            if isinstance(json_data, dict) and 'title' in json_data:
                sheet.setTitle(json_data['title'])
            else:
                sheet.setTitle('测试用例')

            # 获取根主题
            root_topic = sheet.getRootTopic()

            # 如果 json_data 是字典且包含 topic 键
            if isinstance(json_data, dict) and 'topic' in json_data:
                _build_xmind_topic(root_topic, json_data['topic'])
            elif isinstance(json_data, dict):
                # 直接作为根主题处理
                _build_xmind_topic(root_topic, json_data)
            elif isinstance(json_data, list):
                # 如果是列表，每个元素作为一个子主题
                for item in json_data:
                    if isinstance(item, dict):
                        child_topic = root_topic.addSubTopic()
                        _build_xmind_topic(child_topic, item)

            # 保存 XMind文件
            file_dir = os.path.dirname(output_file)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            xmind.save(workbook, output_file)
            print(f"XMind文件已成功生成：{output_file}")
            return True

        except Exception as e:
            print(f"转换 XMind文件时发生错误：{str(e)}")
            return False

    def convert_test_points_to_xmind_format(self,input_data, root_title="逻辑图", sheet_title="测试用例"):
        def generate_id():
            return str(uuid.uuid4())

        test_point_topics = []
        test_point_counter = 1

        for category, subcategories in input_data.items():
            if isinstance(subcategories, dict):
                sub_topics = []
                for sub_key, sub_values in subcategories.items():
                    sub_topic = {
                        'id': generate_id(),
                        'link': None,
                        'title': sub_key,  # 如"等价类划分"
                        'note': None,
                        'label': None,
                        'comment': None,
                        'markers': []
                    }
                    sub_topics.append(sub_topic)

                    # 构建测试点主题
                    test_point_topic = {
                        'id': generate_id(),
                        'link': None,
                        'title': f"测试点{test_point_counter}",  # 如"测试点1"
                        'note': None,
                        'label': None,
                        'comment': None,
                        'markers': [],
                        'topics': sub_topics
                    }
                    test_point_topics.append(test_point_topic)
                    test_point_counter += 1

            elif isinstance(subcategories, list): # 如果直接是列表，每个元素作为子主题
                sub_topics = []
                for item in subcategories:
                    sub_topic = {
                        'id': generate_id(),
                        'link': None,
                        'title': str(item),
                        'note': None,
                        'label': None,
                        'comment': None,
                        'markers': []
                    }
                    sub_topics.append(sub_topic)

                test_point_topic = {
                    'id': generate_id(),
                    'link': None,
                    'title': f"测试点{test_point_counter}",
                    'note': None,
                    'label': None,
                    'comment': None,
                    'markers': [],
                    'topics': sub_topics
                }
                test_point_topics.append(test_point_topic)
                test_point_counter += 1

                # 构建完整的XMind JSON结构
        xmind_json = {
            'id': generate_id(),
            'title': root_title,
            'topic': {
                'id': generate_id(),
                'link': None,
                'title': sheet_title,
                'note': None,
                'label': None,
                'comment': None,
                'markers': [],
                'topics': test_point_topics
            }
        }

        return xmind_json

    def save_xmind_json(self,data, output_file):
        """
        将XMind格式的JSON数据保存到文件
        """
        try:
            # 确保目录存在
            file_dir = os.path.dirname(output_file)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            # 写入JSON文件（单行格式，与测试点2.json保持一致）
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)

            print(f"XMind格式JSON已成功保存到: {output_file}")
            return True
        except Exception as e:
            print(f"保存JSON文件时发生错误: {str(e)}")
            return False

    def convert_and_export_to_xmind(self,input_data, output_xmind_file, root_title="逻辑图", sheet_title="测试用例",
                                    template_file=None):
        """
        一键转换并导出为XMind文件

        Args:
            input_data: 原始测试点数据
            output_xmind_file: 输出的XMind文件路径
            root_title: 根节点标题
            sheet_title: 工作表标题
            template_file: XMind模板文件路径（可选）

        Returns:
            bool: 是否成功
        """
        # 步骤1: 转换为XMind标准JSON格式
        xmind_json = convert_test_points_to_xmind_format(input_data, root_title, sheet_title)

        # 步骤2: 使用JsonToXmind类导出为XMind文件
        converter = JsonToXmind()
        success = converter.json_to_xmind(xmind_json, output_xmind_file, template_file)

        if success:
            print(f"XMind文件已成功生成: {output_xmind_file}")

        return success


#AI给出json，转化为xmind格式文件


#获取测试用例转化为xmind格式文件

#测试用例的xmind格式文件转为json

#AI给出json，转化为execl格式文件

#AI给出json，转化为xmind格式文件




if __name__ == '__main__':
    # dic_to_xlsx = DicToXlsx()
    # dic_to_xlsx.table_data_processing()
    # dc = MxindDataProcessor()
    # res = dc.xmind_to_json()
    # DD = WriteInfo()
    # DD.write_json_to_file(data=res, file=r"D:\AIGeneration\testcase\demo.json")
    #
    # with open(r"D:\AIGeneration\testcase\demo.json", 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    # #
    # # # 转换为 XMind并导出
    # output_xmind = r"C:\Users\admin\Desktop\demo_output.xmind"
    # json_to_xmind(json_data, output_xmind)
    res = XmindPointJson()
    res.extract_test_points_data()