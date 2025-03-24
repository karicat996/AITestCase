import subprocess
import os
from scapy.all import *
import json
from common.getData import getPrinterData
"""
  tshark命令筛选过滤抓取数据
  开始捕捉，设置时间，停止捕捉

  输出数据包

  将抓取的数据保存到临时文件里

  进行数据解析，分析json
  根据json里的字段断言
  测试用例通过
  第一步：捕捉数据--->放到临时文件中---->过滤数据---->展示json数据---->上报具体的字段 

  第二步： 大量过滤分析  ok

  第三步： 数据封装  

  第四步： 数据视图化


 最终 输出demo脚步


"""

class TsharkCapture:


    def data_analysis(self,ip,type):
        results = []
        # src_path = getPrinterData(ip,type)# 文件数据解析json
        src_path = r"D:/ChituManagerProject/data/tcp/192.168.0.110.pcap"
        if src_path is not None:
            packets = rdpcap(src_path)


        for packet in packets:
            # 检查是否为 UDP 数据包
            if packet.haslayer('UDP'):
                payload = bytes(packet['UDP'].payload)
                json_data = self._try_parse_json(payload)
                if json_data:
                    return json_data

            if packet.haslayer('TCP'):
                payload = bytes(packet['TCP'].payload)
                json_data = self._try_parse_json(payload)
                if json_data:
                    results.append(json_data)

            if packet.haslayer('HTTP'):
                payload = bytes(packet['HTTP'].payload)
                json_data = self._try_parse_json(payload)
                if json_data:
                    return json_data

            if packet.haslayer('Websocket'):
                payload = bytes(packet['Websocket'].payload)
                json_data = self._try_parse_json(payload)
                if json_data:
                    return json_data

        return  results

    def _try_parse_json(self, payload):
        try:
            # 打印 payload 内容以便调试
            # print(f"Payload: {payload}")

            # 尝试将字节数据解码为 UTF-8 字符串
            payload_str = payload.decode('utf-8')
            json_data = self._extract_json(payload_str)
            return json_data
        except (UnicodeDecodeError, json.JSONDecodeError):
            # 尝试使用 latin1 编码
            try:
                payload_str = payload.decode('latin1')
                json_data = self._extract_json(payload_str)
                return json_data
            except (UnicodeDecodeError, json.JSONDecodeError):
                # 如果解码或解析失败，打印错误信息并返回 None
                print("无法解码或解析 JSON 数据")
                return None

    def _extract_json(self, payload_str):
        try:
            # 尝试从字符串中提取 JSON 数据
            # 这里假设 JSON 数据是字符串的一部分，且以 '{' 开头，以 '}' 结尾
            start = payload_str.find('{')
            end = payload_str.rfind('}')
            if start != -1 and end != -1 and end > start:
                json_str = payload_str[start:end + 1]
                json_data = json.loads(json_str)
                return json_data
        except json.JSONDecodeError:
            raise "无法解析提取的 JSON 数据"
            return None

    #json数据去重
    def json_deduplication(self,json_data):
        if not isinstance(json_data, list):
            json_data = [json_data]
        seen = set()
        deduplicated_list = []
        for item in json_data:
            # 将JSON对象转换为一个不可变的元组，以便于比较
            item_tuple = self._convert_to_immutable(item)
            if item_tuple not in seen:
                seen.add(item_tuple)
                deduplicated_list.append(item)
        return deduplicated_list


    def _convert_to_immutable(self, obj):#将嵌套字典和列表转化为不可变的元组

        if isinstance(obj, dict):
            return tuple(sorted((k, self._convert_to_immutable(v)) for k, v in obj.items()))
        elif isinstance(obj, list):
            return tuple(self._convert_to_immutable(item) for item in obj)
        else:
            return obj



if __name__ == "__main__":
    res = TsharkCapture()
    results = res.data_analysis("192.168.0.110","tcp")
    result = res.json_deduplication(results)
    print(result)
