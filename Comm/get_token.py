import os
import requests
import json
import yaml
from Comm.interface import dns_environment
import urllib3
from Comm.USERINFO import *
from Comm.error_log import Logger

file_path = os.path.basename(__file__)
logger = Logger(logger_name=file_path)


def get_userinfo(URL, username=USERNAME, password=PASSWORD, oemCode=OEMCODE):
    # 获取openId和accesstoken
    try:
        url = URL + '/oauth'
        d = {'service': 'authorize', 'version': '',
             'username': username, 'password': password,
             'grantType': 'password', 'clientId': 'foscloud',
             'clientSecret': '180886A8A45AA905E3182A99D24A874B',
             'consideringTheReusability': 'true', 'accessType': '2', 'oemCode': oemCode}
        r = requests.post(url, data=d, verify=False)
        jsonContent = json.loads(r.text)
    except Exception as e:
        msg = '登录账号获取用户认证信息数据失败 get_userinfo' + "    " + str(e)
        logger.war(msg)
        return 0
    # 获取usertag、alexatag和subtoken、rekognitionTag
    try:
        url2 = URL + '/gateway'
        da = {'service': 'center.getServerInfo', 'version': '',
              'accessToken': jsonContent['data']['accessToken'], 'openId': jsonContent['data']['openId'],
              'area': '', 'clientId': 'foscloud',
              'oemCode': oemCode}
        re = requests.get(url2, da, verify=False)
        user_data = jsonContent['data']
        # print(user_data)
        jsonContent2 = json.loads(re.text)
        user_data['subtoken'] = jsonContent2['data']['subtoken']
        user_data['tag'] = jsonContent2['data']['tag']
        user_data['storeTag'] = jsonContent2['data']['storeTag']
        user_data['alexaTag'] = jsonContent2['data']['alexaTag']
        user_data['rekognitionTag'] = jsonContent2['data']['rekognitionTag']
        logger.info('获取用户认证信息成功,返回数据为：' + str(user_data))
        return user_data
    except Exception as e:
        msg = '根据表格请求所需信息插入用户信息失败' + "    " + str(e)
        logger.war(msg)
        return 0


test_data = r'D:\Python_test\web\test_0506\config\api_data.yaml'
urllib3.disable_warnings()
with open(test_data, 'r', encoding='utf-8') as file:
    data = yaml.load(stream=file, Loader=yaml.FullLoader)


# 2--从user_ipc_setting_v2_0.getByMac接口中得到ipc id
def user_ipc_setting_v2_0_getByMac_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[2]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['data']['id'])
    except Exception as e:
        msg = '设备模块   查询设备根据MAC   user_ipc_setting_v2_0.getByMac  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 3--从fcmall.queryOrderDetail接口中得到tradeOrderNo
def fcmall_queryOrderDetail_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[3]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['detailList'][0]['tradeOrderNo'])
    except Exception as e:
        msg = '支付   查询订单详情   fcmall.queryOrderDetail  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 4--从user_bpi.list_all接口中得到bpi的id
def user_bpi_list_all_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[4]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['data']['bpiBaseList'][0]['id'])
    except Exception as e:
        msg = '设备模块   查询用户IPC和BPI基站信息   user_bpi_list_all  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 5--从center.getServerInfo接口中得到Tag
def center_getServerInfo_tag_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[5]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['data']['tag'])
    except Exception as e:
        msg = '设备模块   基础子服务信息查询  center.getServerInfo  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 从center.getServerInfo接口中得到storeTag
def center_getServerInfo_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[5]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return jsonContent['data']['storeTag']
    except Exception as e:
        msg = '设备模块   基础子服务信息查询  center.getServerInfo  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 6--从user_nvr.list接口中得到NVR的id
def user_nvr_list_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[6]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        nvrid = jsonContent['data'][0]['id']
        return str(nvrid)
    except Exception as e:
        msg = '设备模块   查询用户的NVR   user_nvr.list  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 7--从coupon.getByCouponCode接口中得到couponId
def coupon_getByCouponCode_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[7]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.post(url, data=data, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['id'])
        # return jsonContent
    except Exception as e:
        msg = 'portal   APP获取优惠券信息   oupon.getByCouponCode  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 8--从ddns-info.getDdnsByType接口中得到ddns的id
def ddns_info_getDdnsByType_parameter(openid, accesstoken):
    try:
        url = dns_environment(2)
        d = data[8]
        d['openId'] = openid
        d['accessToken'] = accesstoken
        r = requests.get(url, params=d, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['data']['id'])
    except Exception as e:
        msg = 'portal   查询DDNS信息   ddns-info.getDdnsByType  作为参数接口连接失败' + "    " + str(e)
        logger.war(msg)
        return 0


# 9--从queryDevicesLatest接口中得到最后一个离线消息id
def message_queryDevicesLatest_parameter(tag):
    try:
        url = dns_environment(0) + r'/push-msg/queryDevicesLatest?tag={}'.format(tag)
        r = requests.get(url, verify=False)
        jsonContent = json.loads(r.text)
        return str(jsonContent['data']['msgList'][0]['msgId'])
    except Exception as e:
        msg = 'queryDevicesLatest   查询离线消息id信息   /push-msg/queryDevicesLatest  作为参数接口连接失败' + "    " + str(
            e)
        logger.war(msg)
        return 0


if __name__ == '__main__':
    url = 'https://test-api.myfoscam.com'
    a = get_userinfo(url)
    print(a)
