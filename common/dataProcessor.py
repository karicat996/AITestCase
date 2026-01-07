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
        self.data2 = {
  "功能角度测试模块": [
    {
      "测试模块": "等价类划分",
      "用例等级": "P0",
      "测试用例": [
        {
          "标题": "验证红包金额在有效范围内（0.01-200元）能够正常发送",
          "前置条件": [
            "用户已登录并完成实名认证",
            "账户余额充足",
            "网络连接正常"
          ],
          "操作步骤": [
            "进入聊天界面",
            "点击红包功能按钮",
            "选择红包类型（普通红包或拼手气红包）",
            "输入有效金额（如50元）",
            "确认发送红包"
          ],
          "预期结果": [
            "红包成功发送到聊天窗口",
            "扣款金额正确",
            "发送成功提示显示"
          ]
        },

      ]
    }
  ]
}

    # 针对测试点
    def json_to_markdown(self, data=None, output_file=None, level=0):
      """
      递归地将JSON数据转换为Markdown格式并写入文件
      """
      if data is None:
        data = self.data

      with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 测试点\n") # 添加标题
        self._write_markdown_recursive(data, f, level) # 递归处理数据

    def _write_markdown_recursive(self, data, file_handle, level=0):
      """
      递归写入Markdown格式数据
      """
      indent = "#" * (level + 2)  # 使用标题层级
      if isinstance(data, dict):
        for key, value in data.items():
          if isinstance(value, (dict, list)):
            # 写入标题
            file_handle.write(f"{indent} {key}\n\n")
            # 递归处理子元素
            self._write_markdown_recursive(value, file_handle, level + 1)
          else:
            # 简单键值对
            file_handle.write(f"{indent} {key}: {value}\n\n")
      elif isinstance(data, list):
        for item in data:
          if isinstance(item, (dict, list)):
            file_handle.write(f"\n")
            self._write_markdown_recursive(item, file_handle, level + 1)
          else:
            # 列表项使用Markdown列表格式
            file_handle.write(f"{'#' * level}{indent} {item}\n")
        file_handle.write("\n")

    # 针对测试用例
    def json_to_testcase(self, data=None, output_file=None, level=0):
      """
      将JSON数据转换为测试用例格式并写入文件
      """
      if data is None:
        data = self.data2

      with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 测试用例\n")  # 添加标题
        self._write_testcase_recursive(data, f, level)

    def _write_testcase_recursive(self, data=None, file_handle=None, level=0):
        """
        递归写入测试用例格式数据
        """
        indent = "#" * (level + 2)

        if isinstance(data, dict):
          for key, value in data.items():
            if isinstance(value, (dict, list)):
              # 写入标题
              file_handle.write(f"{indent} {key}\n\n")
              # 递归处理子元素
              self._write_testcase_recursive(value, file_handle, level + 1)
            else:
              # 键值对
              file_handle.write(f"{indent} {key}: {value}\n\n")
        elif isinstance(data, list):
          for item in data:
            if isinstance(item, (dict, list)):
              file_handle.write(f"\n")
              self._write_testcase_recursive(item, file_handle, level + 1)
            else:
              # 列表项
              file_handle.write(f"{'#' * level}{indent} {item}\n")



if __name__ == "__main__":
    # 转换为Markdown
    dc = DataProcess()
    # 转换为Markdown
    dc.json_to_testcase(output_file=r"D:\AIGeneration\testcase\testcase.md")

