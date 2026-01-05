# 将json格式转化成xmind格式
import json
import os



class DataProcess:

    def __init__(self):
            json_path = r""
            markdown_path = r""
            self.data = {
      "功能角度测试点": {
        "等价类划分": [
          "红包金额在有效范围内（如0.01-200元）",
          "红包金额为边界值（如0.01元、200元）",
          "红包金额为无效值（如负数、0元、超过200元）"
        ],
        "边界值分析": [
          "红包最小金额0.01元",
          "红包最大金额200元",
          "红包金额为0元（无效）",
          "红包金额为200.01元（无效）"
        ],
        "错误推测": [
          "输入非数字字符作为红包金额",
          "在发送红包时网络中断",
          "红包余额不足时仍尝试发送",
          "重复点击发送按钮导致多次扣款"
        ],
        "场景法": [
          "单人发送红包给单人",
          "群聊中发送拼手气红包",
          "群聊中发送普通等额红包",
          "红包过期未领取的退款流程"
        ],
        "判定表": [
          "用户是否实名认证与发送红包权限的关系",
          "红包类型（普通/拼手气）与金额分配规则",
          "领取红包是否需为好友或群成员"
        ],
        "正交实验": [
          "不同红包类型（普通、拼手气）与不同金额组合",
          "不同支付方式（余额、银行卡）与红包发送场景组合"
        ],
        "状态迁移": [
          "红包状态从创建、发送、领取到过期/退款的完整流程",
          "用户从打开红包到领取成功或失败的状态变化"
        ],
        "流程分析": [
          "发送红包流程：选择类型->输入金额->支付->发送",
          "领取红包流程：点击红包->开红包->领取成功",
          "退款流程：红包过期->系统自动退款到账户"
        ]
      },
      "用户使用角度测试点": {
        "新用户场景": [
          "首次发送红包的引导提示",
          "新用户领取红包的权限验证",
          "红包功能入口的易发现性"
        ],
        "日常使用场景": [
          "在聊天界面快速发送红包",
          "查看已发送红包的记录和状态",
          "查看已领取红包的记录和金额"
        ],
        "群聊场景": [
          "在群聊中发送拼手气红包的公平性",
          "群红包被快速领取时的通知提示",
          "群红包领取列表的可见性"
        ],
        "支付相关场景": [
          "发送红包时多种支付方式的选择",
          "红包发送失败时的退款及时性",
          "领取红包后余额更新的实时性"
        ],
        "异常场景": [
          "弱网环境下发送/领取红包的稳定性",
          "红包被恶意刷领的防护机制",
          "设备切换后红包记录的同步"
        ],
        "节日特殊场景": [
          "春节等节日红包封面的特殊显示",
          "节日期间红包金额上限的临时调整",
          "拜年红包等特殊红包类型的适配"
        ]
      }
    }



    # 递归将JSON数据转换为Markdown格式
    def json_to_markdown(self, data, level=0):
        """
        递归地将JSON数据转换为Markdown格式
        """
        # 定义缩进配置
        INDENT_UNIT = "    "  # 4个空格作为一个缩进单位
        markdown_content = ""
        current_indent = INDENT_UNIT * level

        # 首先判断是否是字典，列表，字符串，数字，None
        if isinstance(data, dict):
            # 遍历字典的键值对
            # 特殊处理测试用例对象
            if 'title' in data:
                # 按照目标格式逐级缩进
                markdown_content += f"{current_indent}- {data.get('id', '')}\n"
                markdown_content += f"{current_indent}{INDENT_UNIT}- {data.get('title', '')}\n"
                markdown_content += f"{current_indent}{INDENT_UNIT * 2}- {data.get('description', '')}\n"

                # 处理步骤数组
                steps = data.get('steps', [])
                if steps:
                    steps_text = " ".join([f"{i + 1}.{step}" for i, step in enumerate(steps)])
                    markdown_content += f"{current_indent}{INDENT_UNIT * 3}- {steps_text}\n"

                # 处理预期结果
                expected = data.get('expected_result', '')
                if expected:
                    markdown_content += f"{current_indent}{INDENT_UNIT * 4}- {expected}\n"
            else:
                # 普通字典处理
                for key, value in data.items():
                    if isinstance(value, (dict, list)):
                        markdown_content += f"{current_indent}- **{key}**:\n"
                        markdown_content += json_to_markdown(value, level + 1)
                    else:
                        markdown_content += f"{current_indent}- **{key}**: {value}\n"
        elif isinstance(data, list):
            for index, item in enumerate(data):
                markdown_content += f"{current_indent}{index + 1}.\n"
                markdown_content += json_to_markdown(item, level + 1)
        elif isinstance(data, str):
            markdown_content += f"{current_indent}{data}\n"
        elif isinstance(data, int):
            markdown_content += f"{current_indent}{data}\n"
        else:
            markdown_content += f"{current_indent}{data}\n"

        return markdown_content


     #数据写入md文件
    def json_to_markdown_file(self, output_file):

        if output_file.exists():
            print(f"{output_file}已存在，请勿重复生成")
            return output_file
        else:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        # 确保输出目录存在
        # 写入文件
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(self.data)

        return output_file






if __name__ == "__main__":
    # 转换为Markdown
    dc = DataProcess()
    # 转换为Markdown
    dc.json_to_markdown_file(output_file=r"D:\AIGeneration\config\answer.md")

    # 打开文件
    os.system(f"start {markdown_path}")