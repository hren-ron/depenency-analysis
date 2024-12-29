
import yaml
import logging.config

# 加载日志
with open('config/logging.yml', 'r') as f_conf:
    dict_conf = yaml.load(f_conf, Loader=yaml.FullLoader)
logging.config.dictConfig(dict_conf)
logger = logging.getLogger('simpleLogger')