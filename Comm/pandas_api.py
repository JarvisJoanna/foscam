import requests
import pandas as pd
import unittest


class TestAPI(unittest.TestCase):

    def setUp(self):
        # 加载测试数据
        self.data = pd.read_excel('test_data.xlsx')

    def test_api(self):
        # 遍历数据，对每一行数据进行测试
        for index, row in self.data.iterrows():
            # 构造请求参数
            params = {
                'param1': row['column1'],
                'param2': row['column2'],
            }

            # 发送请求
            response = requests.get(r'http://api.example.com', params=params)

            # 判断响应状态码是否为200
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
