import os
import shutil

def  clearLog(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"{path}目录已删除")
    else:
        print(f"{path}目录不存在")






def  clearCache(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"{path}目录已删除")
    else:
        print(f"{path}目录不存在")
