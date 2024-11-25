import json
import requests
from Comm.get_token import get_userinfo
from Comm.get_token import user_ipc_setting_v2_0_getByMac_parameter as getipcid
from Comm.get_token import fcmall_queryOrderDetail_parameter as getordeid
from Comm.get_token import user_nvr_list_parameter as getnvrid
from Comm.get_token import user_bpi_list_all_parameter as getbpiid
from Comm.get_token import ddns_info_getDdnsByType_parameter as getddnsid
from Comm.get_token import message_queryDevicesLatest_parameter as getmsgid
from Conf.Config import env_cfg, test_sys_cfg, sys_cfg
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_model(mod, URL, api_data):
    if mod == 'post':
        requests_data = requests.post(URL, api_data, verify=False)
        response_data = json.loads(requests_data.text)
    else:
        requests_data = requests.get(URL, api_data, verify=False)
        response_data = json.loads(requests_data.text)
    return response_data


def request_data(URL, datas, user_info=None):
    if user_info is None:
        userinfo = get_userinfo(URL)
    else:
        userinfo = user_info  # 获取用户openId和token
    if datas['接口地址'] == 1:
        URL = URL + env_cfg[str(datas['接口地址'])]
    elif datas['接口地址'] == 2:
        URL = URL + env_cfg[str(datas['接口地址'])]
    data = json.loads(datas['参数'])
    if datas['往字典插入键值'] is not None or datas['往字典插入键值'] != '':
        if 'openId' in str(datas['往字典插入键值']):
            data['openId'] = userinfo['openId']
        if 'accessToken' in str(datas['往字典插入键值']):
            data['accessToken'] = userinfo['accessToken']
        if 'refreshToken' in str(datas['往字典插入键值']):
            data['refreshToken'] = userinfo['refreshToken']
        if 'userTag' in str(datas['往字典插入键值']):
            data['userTag'] = userinfo['tag']
        if 'Tag' in str(datas['往字典插入键值']):
            data['tag'] = userinfo['tag']
        if 'ipcid' in str(datas['往字典插入键值']):
            data['id'] = getipcid(userinfo['openId'], userinfo['accessToken'])
        if 'bpiid' in str(datas['往字典插入键值']):
            data['id'] = getbpiid(userinfo['openId'], userinfo['accessToken'])
        if 'nvrid' in str(datas['往字典插入键值']):
            data['id'] = getnvrid(userinfo['openId'], userinfo['accessToken'])
        if 'tradeOrderNo' in str(datas['往字典插入键值']):
            data['tradeOrderNo'] = getordeid(userinfo['openId'], userinfo['accessToken'])
        if 'ddnsid' in str(datas['往字典插入键值']):
            data['id'] = getddnsid(userinfo['openId'], userinfo['accessToken'])
        if 'msgId' in str(datas['往字典插入键值']):
            data['msgId'] = getmsgid(userinfo['tag'])
    return URL, data


def xiaobei_request_data(URL, datas, user_info=None):
    if user_info is None:  # 获取用户openId和token
        userinfo = get_userinfo(URL)
    else:
        userinfo = user_info
    URL = URL + '/{}'.format(datas['接口名称'])
    data = json.loads(datas['参数'])
    if datas['往字典插入键值'] is not None or datas['往字典插入键值'] != '':
        if 'openId' in str(datas['往字典插入键值']):
            data['openId'] = userinfo['openId']
        if 'accessToken' in str(datas['往字典插入键值']):
            data['accessToken'] = userinfo['accessToken']
        if 'refreshToken' in str(datas['往字典插入键值']):
            data['refreshToken'] = userinfo['refreshToken']
        if 'userTag' in str(datas['往字典插入键值']):
            data['userTag'] = userinfo['tag']
    return URL, data


def env_url(env):
    if env == 0:
        URL = test_sys_cfg['com']
    elif env == 1:
        URL = test_sys_cfg['cn']
    elif env == 2:
        URL = sys_cfg['com']
    elif env == 3:
        URL = sys_cfg['cn']
    return URL


if __name__ == '__main__':
    # xiaobei_request_data
    print(env_url(0))
