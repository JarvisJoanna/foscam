import os
import time
import unittest
from Comm import myddt
from Comm.error_log import Logger
from Comm.get_token import get_userinfo
from Comm.request_datas import request_model,  xiaobei_request_data
from Comm.data import read_excel
from main import TestCasePath, URL

# 获取测试数据
file = os.path.join(TestCasePath,
                    r'Testdata\Foscam_API_test_case_20210222.xls')  # Foscam_API_TEST_Case1.xls&Foscam_API_test_case_20210222.xls
test_data = read_excel(file, sheet_name='XY-xiaobei')


@myddt.ddt
class TestIOT_XIAOBEI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        file_path = os.path.basename(__file__)
        cls.logger = Logger(logger_name=file_path)
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        cls.time1 = time.time()
        cls.logger.info('开始执行测试用例，时间：{}'.format(now))
        cls.user_info = get_userinfo(URL)

    @classmethod
    def tearDownClass(cls):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        cls.time2 = time.time()
        cls.logger.info('测试用例执行完成，时间：{},共用时{}秒'.format(now, round(cls.time2 - cls.time1, 2)))

    @myddt.data(*test_data)
    def test_iot_xiaobei(self, datas):
        """{}""".format(datas['接口测试描述'])
        print(datas['接口测试描述'])
        request_datas = xiaobei_request_data(URL, datas, self.user_info)
        r = request_model(datas['提交方式'], request_datas[0], request_datas[1])
        # print('请求信息:{},\n响应数据:{}'.format(request_data,r))
        self.logger.info('用例执行完成，执行用例：{},\n用例请求信息:{},\n响应数据:{}'.format(datas['接口测试描述'],request_datas, r))
        self.assertIn(datas['errorCode'], r['errorCode'])


if __name__ == '__main__':
    unittest.main()
