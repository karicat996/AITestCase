import os
from pathlib import Path
import json
import yaml

class fileProcessor:
    def __init__(self):
        pass


    def deal_json_data(self, json_data, json_file=None, join_data=False):
        if os.exists(json_file) is True:
            if join_data is False:
                json_data = json.load(json_file)
                return json_data
            else :
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"{json_file}文件写入")
        else:
            os.mikedirs(pathlib.Path(json_file).parent, exist_ok=True)



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











