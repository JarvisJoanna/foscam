# 读取config.ini
import os
from configparser import ConfigParser

# 使用相对目录确定文件位置
_conf_dir = os.path.dirname(__file__)
_conf_file = os.path.join(_conf_dir, 'config.ini')


# 继承ConfigParser，写一个将结果转为dict的方法
class MyParser(ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d


# 读取所有配置，以字典方式输出结果
def _get_all_conf():
    _config = MyParser()
    result = {}
    if os.path.isfile(_conf_file):
        try:
            _config.read(_conf_file, encoding='UTF-8')
            result = _config.as_dict()
        except OSError:
            raise ValueError("Read config file failed: %s" % OSError)
    return result


config = _get_all_conf()
sys_cfg = config['sys']
test_sys_cfg = config['test_sys']
smtp_cfg = config['smtp']
email_cfg = config['email']
log_cfg = config['log']
env_cfg = config['env']

# 将各配置读取出来，放在变量中，后续其它文件直接引用这个这些变量
if __name__ == '__main__':
    print(sys_cfg['com'])
