import subprocess
import os
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

"""
获取udp ，tcp,mqtt,http，websocket,rtc数据

"""
def  get_path(type):
    current_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_path)
    parent_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(parent_dir,"data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    udp_path = os.path.join(data_dir,"udp")
    tcp_path = os.path.join(data_dir,"tcp")
    websocket_path = os.path.join(data_dir,"websocket")
    rtcp_path = os.path.join(data_dir,"rtcp")

    path_list = [udp_path, tcp_path, websocket_path, rtcp_path]
    for path in path_list:
        if not os.path.exists(path):
            os.makedirs(path)
    if type == "udp":
       return path_list[0]
    if type == "tcp":
        return path_list[1]
    if type == "websocket":
        return path_list[2]
    if type == "rtcp":
        return path_list[3]









def getPrinterData(ip,type):
    if type in ["udp", "tcp", "mqtt", "http", "websocket", "rtcp"]:
        path = get_path(type)
        pcapfile = os.path.join(path, f"{ip}.pcap")
        print(pcapfile)
    if pcapfile is not None:
        interface = "wlan"  # 可配置接口
        LAN_interface = "eth0"  # 网络接口
        target_ip = ip  # 目标 IP
        output_file = pcapfile  # 输出文件名
        duration = 120  # 捕获持续时间（秒）
        if type in ["udp", "tcp"]:
            filter_expression = f"{type} and host {target_ip}"
        elif type in ["websocket", "rtcp", "http", "mqtt"]:
            display_expression = f"{type} and ip.addr == {target_ip}"
        else:
            logging.error(f"Unsupported data type: {type}")
            raise ValueError(f"Unsupported data type: {type}")

        # 构建 tshark 命令
        if type in ["tcp","udp"]:
            command = [
                "tshark",
                "-i", interface,
                "-f", filter_expression,
                "-a", f"duration:{duration}",
                "-w", output_file
            ]
        elif type in ["websocket","rtcp","http"]:
            command = [
                "tshark",
                "-i", LAN_interface,
                "-Y", display_expression,
                "-a", f"duration:{duration}",
                "-w", output_file
            ]
        else:
            logging.error(f"Unsupported data type: {type}")
            raise ValueError(f"Unsupported data type: {type}")
        subprocess.run(command, text=True)
        print("等待中")
        return pcapfile
    else:
        raise Exception(f"获取{type}数据失败")


if __name__ == '__main__':
    getPrinterData("172.16.1.234 ","tcp")
