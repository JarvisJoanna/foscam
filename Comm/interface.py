def dns_environment(api_type):
    environment_type = 1  # 请求环境：1为测试国外
    if environment_type == 1:
        if api_type == 0:
            api_interface = 'https://test-api.myfoscam.com'
            return api_interface

        elif api_type == 1:
            api_interface = 'https://test-api.myfoscam.com/oauth'
            return api_interface

        elif api_type == 2:
            api_interface = 'https://test-api.myfoscam.com/gateway'
            return api_interface
    else:
        if api_type == 0:
            api_interface = 'https://test-api.myfoscam.cn'
            return api_interface

        elif api_type == 1:
            api_interface = 'https://test-api.myfoscam.cn/oauth'
            return api_interface

        elif api_type == 2:
            api_interface = 'https://test-api.myfoscam.cn/gateway'
            return api_interface

