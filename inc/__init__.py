# 添加模块包的相对路径
import sys
import os
from pprint import pprint

# pprint(sys.path)
work_path=os.path.dirname(os.path.abspath(__file__))
# print(work_path)
sys.path.append(work_path)
# pprint(sys.path)