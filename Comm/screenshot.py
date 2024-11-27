# 截图
import os
import time
from Conf.Config import log_cfg
from PIL import ImageGrab

# 先定义截图文件的存放路径，这里在Log目录下建个Screen目录，按天存放截图
_BaseHome = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
_log_path = log_cfg['log_path']
_today = time.strftime("%Y%m%d")
_screen_path = os.path.join(_BaseHome, _log_path, 'Screen', _today)
print(_screen_path)


# 再使用PIL的ImageGrab实现截图
def screen(name):
    t = time.time()
    png = ImageGrab.grab()
    if not os.path.exists(_screen_path):
        os.makedirs(_screen_path)
    image_name = os.path.join(_screen_path, name)
    png.save('%s_%s.png' % (image_name, str(round(t * 1000))))  # 文件名后面加了个时间戳，避免重名


if __name__ == '__main__':
    screen('test')
