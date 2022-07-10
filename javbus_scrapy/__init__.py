import os

from .settings import log_dir

# 提前生成log文件目录
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
