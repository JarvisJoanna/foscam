# 封装测试数据读取方法
import pandas as pd


def read_excel(file, **kwargs):
    data_dict = []
    try:
        data = pd.read_excel(file, keep_default_na=False, **kwargs)
        data_dict = data.to_dict('records')
    except Exception as e:
        print(e)
    finally:
        return data_dict


if __name__ == '__main__':
    datas = read_excel(r'D:\pythonProject\Testcase\Testdata\Foscam_API_TEST_Case.xls')
    print(datas)
    for i in datas:
        print(i)
