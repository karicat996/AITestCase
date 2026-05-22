import paddleocr
from collections import Counter
import cv2
import numpy as np
from PIL import ImageGrab, Image
from paddleocr import PaddleOCR
import time
import os

def ocr_get_text_from_img(
    image_path: str
):
    """
    从屏幕截取图片，并使用ocr获取text
    :return:
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"{image_path}文件不存在")
    ocr =  paddleocr.PaddleOCR(lang='ch',use_angle_cls=True,precision='fp16')
    img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)  # 智能降噪

    # 执行OCR识别
    result = ocr.ocr(img, cls=True)

    # 结构化输出
    texts = [line[1][0] for line in result[0]] if result else []
    details = [
        {
            "position": np.array(line[0]).astype(int).tolist(),
            "content": line[1][0],
            # "confidence": float(line[1][1])
        } for line in result[0]
    ] if result else []

    return {
        "text": texts,
        "details": details,
        "image_shape": img.shape
    }


if __name__ == '__main__':
    # result = ocr_get_text_from_img(image_path=r"D:\AIGeneration\config\de.png")
    res = ['chitumanager重构', '1.历史记录自动化', '2.重构登录00，01d的用例今日目标', '3.外部打开chitumanager', '4.chitumanger与设备端的校验', '重构用例后-', '5.封装chitumanager为软件执行', '6.增加chitumanager打包程序', '7.将报告发送到邮件中']

    # 方法1: 使用join直接拼接所有元素
    des = ''.join(res)
    print("拼接结果:", des)


