import os
import pathlib
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














