import configparser
import os

# 解析配置生成config对象
config_file_name = "config.ini"
config_abs_path = os.path.join((os.path.dirname(os.path.dirname(__file__))), config_file_name)
config_parser = configparser.ConfigParser()
config_parser.read(config_abs_path, encoding="utf-8")
spider_config = config_parser['spider_config']
global_config = config_parser

# 提前生成log文件目录
setting_dir = os.path.dirname(__file__)
log_dir = os.path.dirname(setting_dir)
log_dir = os.path.join(log_dir, spider_config['log_dir_name'])
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
