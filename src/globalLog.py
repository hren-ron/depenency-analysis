
import yaml
import logging.config

# 加载日志
with open('logging.yml', 'r') as f_conf:
    dict_conf = yaml.load(f_conf, Loader=yaml.FullLoader)
logging.config.dictConfig(dict_conf)
logger = logging.getLogger('simpleExample')