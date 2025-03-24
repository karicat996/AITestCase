

#处理 json数据
from typing import Any,List,Optional
import  json
from common.bindPrinter import TsharkCapture

class DataProcess:
    def __init__(self):
        self.data = []





#查询嵌套json数据

    def get_printer_data(self):
        res = TsharkCapture()
        results = res.data_analysis("192.168.0.110", "tcp")
        printerInfo = res.json_deduplication(results)
        print(printerInfo[0])


#处理大量json数据，查询某个字典键的值,封装成列表

    def extract_nested_values(
            self,
            data_list: List[dict],
            target_key: str,
            default: Any = None,
            max_depth: int = 10,
            parse_json_str: bool = True
    )-> List[Optional[Any]]:

        def _deep_search(obj,current_depth=0)->Any:
            if current_depth > max_depth:
                return default

            if parse_json_str and isinstance(obj,str):
                try:
                    parsed =  json.loads(obj)
                    return _deep_search(parsed,current_depth+1)
                except json.JSONDecodeError:
                    return default



            if  isinstance(obj,dict):
                if target_key in obj:
                    return obj[target_key]
                for v in obj.values():
                    result = _deep_search(v,current_depth+1)
                    if result is not None:
                        return result
            elif isinstance(obj,list):
                for item in obj:
                    result = _deep_search(item,current_depth+1)
                    if result is not default:
                        return result
            return default

        return [_deep_search(item) for item in data_list]








#获取打印机Attributes



#获取chitumanager的请求命令

#获取chitumanager发送的cmd0

#获取chitumanager发送的cmd1

#获取chitumanager发送的cmd320

#获取chitumanager发送的cmd321


#获取打印机Status

#获取打印机cmd320

#获取打印机cmd321

#获取打印机cmd386

#获取打印机cmnd0

#获取打印机cmd1


if __name__=="__main__":
    data = DataProcess()
    data.get_printer_data()