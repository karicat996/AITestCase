import os
from pathlib import Path
import json
import yaml
from loguru import logger
from utils.logs import LogManager

# 初始化日志配置（指定日志输出到文件夹）
LogManager(log_dir=r"D:\AIGeneration\utils\logs")
class fileProcessor:
    def __init__(self):
        pass


    def deal_json_data(self, json_data, json_file=None, join_data=False):
        if os.path.exists(json_file) is True:
            if join_data is False:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                return json_data
            else :
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"{json_file}文件写入")
        else:
            os.makedirs(os.path.dirname(json_file), exist_ok=True)
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f"{json_file}文件创建并写入")



    def write_file(self, file_path, data, file_type=None):
        """
        通用文件写入方法，支持多种格式
        
        Args:
            file_path: 文件路径
            data: 要写入的数据
            file_type: 文件类型 (json, yaml, txt)，如果不指定则根据文件扩展名自动判断
            
        Returns:
            bool: 写入是否成功
        """
        try:
            # 确保目录存在
            file_dir = os.path.dirname(file_path)
            if file_dir:
                os.makedirs(file_dir, exist_ok=True)
            
            # 自动判断文件类型
            if file_type is None:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.json':
                    file_type = 'json'
                elif ext in ['.yaml', '.yml']:
                    file_type = 'yaml'
                else:
                    file_type = 'txt'
            
            # 根据类型写入文件
            if file_type == 'json':
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                logger.info(f"JSON 文件已成功写入: {file_path}")
                
            elif file_type == 'yaml':
                with open(file_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
                logger.info(f"YAML 文件已成功写入: {file_path}")
                
            elif file_type == 'txt':
                with open(file_path, 'w', encoding='utf-8') as f:
                    if isinstance(data, str):
                        f.write(data)
                    else:
                        f.write(str(data))
                logger.info(f"TXT 文件已成功写入: {file_path}")
                
            else:
                logger.error(f"不支持的文件类型: {file_type}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"写入文件失败 [{file_path}]: {str(e)}", exc_info=True)
            return False

    # 获取文件信息
    def find_and_read_file(self,relative_path, start_dir = None, type = None):

        try:
            if start_dir is None:
                start_dir = Path(__file__).parent.parent
            target_path = Path(start_dir) / relative_path

            if not target_path.exists():
                raise FileNotFoundError(f"{target_path}文件不存在")
            if not target_path.is_file():
                raise IsADirectoryError(f"{target_path}不是文件")

            if type == "json":
                with open(target_path, 'r', encoding='utf-8')  as f:
                    content = json.load(f)
                return content

            if type == "yaml":
                with open(target_path, 'r', encoding='utf-8') as f:
                    content = yaml.load(f, Loader=yaml.FullLoader)
                return content

            if type == "txt":
                with open(target_path, 'r', encoding='utf-8') as f:
                    return f.read()
                return content

        except UnicodeDecodeError:
            with open(target_path, 'w', encoding='gbk') as f:
                return f.read()

        except Exception as e:
            print(f"读取失败：{e}")
            return  None




if __name__ == '__main__':
    f = fileProcessor()
    # f.find_and_read_file("config/promptWord.yaml", type="yaml")
    res = f.find_and_read_file("config/template.json", type="json")
    print(res)











