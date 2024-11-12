import logging
import ctypes
import os
import time
from Conf.Config import log_cfg

FOREGROUND_WHITE = 0x0007
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_YELLOW = FOREGROUND_RED | FOREGROUND_GREEN

STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
file_path = os.path.basename(__file__)
_log_level = eval(log_cfg['log_level'])
_log_path = log_cfg['log_path']
_log_format = log_cfg['log_format']
_log_datefmt = log_cfg['log_datefmt']
path1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now_time = time.strftime('%Y-%m-%d_%H', time.localtime())

_log_file = os.path.join(path1, _log_path, '{}.log'.format(now_time))


def set_color(color, handle=std_out_handle):
    boolv = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return boolv


class Logger:
    """设置日志配置，path，日志存储路径，clevel：cmd展示异常日志的登记，Flevel：日志文件存储的日志等级"""

    def __init__(self, path=_log_file, logger_name=file_path, clevel=logging.INFO, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter(_log_format, _log_datefmt)
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path, encoding='utf-8')
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        set_color(FOREGROUND_BLUE)
        self.logger.debug(message)

    def info(self, message, color=FOREGROUND_BLUE):
        set_color(color)
        self.logger.info(message)

    def war(self, message, color=FOREGROUND_YELLOW):
        set_color(color)
        self.logger.warning(message)

    def error(self, message, color=FOREGROUND_RED):
        set_color(color)
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


if __name__ == '__main__':
    # logpath = path1 + r"\Log\{}.log".format(time.strftime('%Y-%m-%d-%H-%M-%S'))
    logpath = _log_file
    print(logpath)
    file_path = os.path.basename(__file__)
    print(file_path)
    # logyyx = Logger(logpath,'test', logging.INFO, logging.DEBUG)
    # logyyx.debug('一个debug信息')
    # logyyx.info('一个info信息')
    # logyyx.war('一个warning信息')
    # logyyx.error('一个error信息')
    # logyyx.cri('一个致命critical信息')
