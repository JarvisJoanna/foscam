"""Redis数据类型:
1. <set key value>
    类型	:   String(字符串)
    简介:   二进制安全
    特性	:   可以包含任何数据,比如jpg图片或者序列化的对象,一个键最大能存储512M
    场景:   /

2. <hset major_key key value>
    类型	:   Hash(字典)
    简介:   键值对集合,即编程语言中的Map类型
    特性	:   适合存储对象,并且可以像数据库中update一个属性一样只修改某一项属性值(Memcached中需要取出整个字符串反序列化成对象修改完再序列化存回去)
    场景:   存储、读取、修改用户属性

3. <头部：lpush key value1 value2 ... 末尾：rpush key value1 value2 ...> 可添加一个或多个值
    类型	:   List(列表)
    简介:   链表(双向链表)
    特性	:   增删快,提供了操作某一段元素的API
    场景:   1.最新消息排行等功能(比如朋友圈的时间线) 2.消息队列

4. <sadd key member1 member2 ...> 可添加一个或多个值
    类型	:   Set(集合)
    简介:   哈希表实现,元素不重复
    特性	:   1.添加、删除,查找的复杂度都是O(1) 2.为集合提供了求交集、并集、差集等操作
    场景:   1.共同好友 2.利用唯一性,统计访问网站的所有独立ip 3,好用推荐时,根据tag求交集,大于某个阈值就可以推荐

5. <zadd key score1 member1 score2 member2 ...> 可添加一个或多个值
    类型	:   Sorted Set(有序集合)
    简介:   将Set中的元素增加一个权重参数score,元素按score有序排列
    特性	:   数据插入集合时,已经进行天然排序
    场景:   	1.排行榜 2.带权重的消息队列

键值相关命令:
1.  keys *                   查看当前所有的key
2.  exists name              查看数据库是否有name这个key
3.  del name                 删除key name
4.  expire confirm 100       设置confirm这个key100秒过期
5.  ttl confirm              获取confirm 这个key的有效时长
6.  select 0                 选择到0数据库 redis默认的数据库是0~15一共16个数据库
7.  move confirm 1           将当前数据库中的key移动到其他的数据库中，这里就是把confire这个key从当前数据库中移动到1中
8.  persist confirm          移除confirm这个key的过期时间
9.  randomkey                随机返回数据库里面的一个key
10. rename key2 key3         重命名key2 为key3
11. type key2                返回key的数据类型

服务器相关命令:
1.  ping                     PING返回响应是否连接成功
2.  echo                     在命令行打印一些内容
3.  select                   0~15 编号的数据库
4.  quit                     退出客户端
5.  dbsize                   返回当前数据库中所有key的数量
6.  info                     返回redis的相关信息
7.  config get dir/*         实时传储收到的请求
8.  flushdb                  删除当前选择数据库中的所有key
9.  flushall                 删除所有数据库中的数据库

Tips：
打开cmd输入 redis-cli.exe 即可进入redis命令行
"""
# -*- coding:utf-8 -*-
import redis
import pickle
import datetime


class Redis(object):

    def __init__(self, host='host', port=6379, db=0, password=''):
        """
        初始化Redis连接池
        :param host: 主机名
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        """
        pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=None  # 连接池最大值，默认2**31
        )
        self.redis = redis.Redis(connection_pool=pool)

    def __del__(self):
        """程序结束后，自动关闭连接，释放资源"""
        self.redis.connection_pool.disconnect()

    def exists(self, name):
        """
        检查name是否存在
        :param name:
        :return:
        """
        return self.redis.exists(name)

    def delete(self, name):
        """
        删除指定的name
        :param name:
        :return:
        """
        # 先查询存在多少匹配的KEY，然后轮巡进行删除
        keys = self.redis.keys(name)
        print('匹配的值是{}'.format(keys))
        num = 0
        for key in keys:
            num += 1
            print('查询次数：{}，值是：{}'.format(num, key))
            self.redis.delete(key)
        return

    def delete_valu(self, name):  # 删除指定hash类型的KEY中的参数name
        """
        设置name的值
        :param name:
        :param value:
        :return:
        """
        llm = 'rekognition:service:detect:llm'
        try:
            print('删除的值是{}'.format(llm + ':' + name))
            return self.redis.hdel(llm, name)
        except Exception as e:
            print('delete failed')
            print(e)

    def rename(self, old, new):
        """
        重命名
        :param old:
        :param new:
        :return:
        """
        if self.exists(old):
            return self.redis.rename(old, new)

    def set_expire_by_second(self, name, second=60 * 60 * 24 * 7):
        """
        以秒为单位设置过期时间
        :param name:
        :param second: 默认7天
        :return:
        """
        return self.redis.expire(name, time=second)

    def remove_expire(self, name):
        """
        移除name的过期时间，name将持久保持
        :param name:
        :return:
        """
        return self.redis.persist(name)

    def get_expire_by_second(self, name):
        """
        以秒为单位返回name的剩余过期时间
        :param name:
        :return:
        """
        return self.redis.ttl(name)

    def get_name_type(self, name):
        """
        获取name的数据类型
        :param name:
        :return:
        """
        return self.redis.type(name).decode()

    def check_name_type(self, name, expect_type='string'):
        """
        检查name的数据类型
        数据类型对照表：
            set   ->  'string'
            hset  ->  'hash'
            lpush ->  'list'
            sadd  ->  'set'
            zadd  ->  'zset'
        :param name:
        :param expect_type: string / hash / list / set / zset
        :return:
        """
        name_type = self.get_name_type(name)
        if name_type == expect_type:
            return True
        else:
            return False

    def set(self, name, value, do_pickle=True, expire=60 * 60 * 24 * 7):
        """
        添加set类型，使用pickle进行持久化存储
        :param name:
        :param value:
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :param expire: 单位second，默认7天
        :return:
        """
        if do_pickle:
            self.redis.set(name=name, value=pickle.dumps(value), ex=expire)
        else:
            self.redis.set(name=name, value=value, ex=expire)

    def get_set_all(self, do_pickle=True):
        """
        获取所有的set value
        :param do_pickle: 是否使用pickle进行二进制反序列化，默认True
        :return: [{}, {}, {}]
        """
        all_data = []
        if self.redis.keys():
            for key in self.redis.keys():  # 获取所有的key
                flag = self.check_name_type(name=key, expect_type='string')  # 判断是否为set类型
                if not flag:
                    continue
                value = self.get_set_value(name=key, do_pickle=do_pickle)
                all_data.append({key.decode(): value})
        return all_data

    def zadd(self, name, value=None, do_pickle=True, expire=60 * 60 * 24 * 7):
        """
        添加有序集合类型，默认score为当前时间戳，使用pickle进行持久化存储
        :param name:
        :param value: [{}, {}, {}]
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :param expire: 单位second，默认7天
        :return:
        """
        if value is None:
            value = []
        assert value, 'value不能为空'
        value_dict = {}
        for each in value:
            score = each.get('timestamp') or datetime.datetime.now().timestamp()  # 如果没有timestamp，取当前时间戳为score
            if do_pickle:
                value_dict.setdefault(pickle.dumps(each), score)
            else:
                value_dict.setdefault(str(each), score)  # 如果不进行序列化，需要将字典转化为字符串作为Key，否则会报错

        self.redis.zadd(name=name, mapping=value_dict)
        self.set_expire_by_second(name, expire)  # 设置expire

    def get_zadd_data_by_score(self, name, start_score=None, end_score=None, do_pickle=True):
        """
        根据score范围，返回对应的数据，只用于有序集合
        :param name:
        :param start_score: timestamp时间戳
        :param end_score: timestamp时间戳
        :param do_pickle: 是否使用pickle进行二进制序列化，默认True
        :return:
        """
        # 如果start_score为空，默认为前一天的时间戳
        start_score = start_score or (datetime.datetime.now() - datetime.timedelta(days=1)).timestamp()
        # 如果end_score为空，默认为当前时间的时间戳
        end_score = end_score or datetime.datetime.now().timestamp()

        data = self.redis.zrangebyscore(name, start_score, end_score)
        if do_pickle:
            return [pickle.loads(i) for i in data]
        else:
            return [i for i in data]

    def delete_zadd_data_by_score(self, name, start_score, end_score):
        """
        根据score范围，删除对应的数据，只用于有序集合
        :param name:
        :param start_score: timestamp时间戳
        :param end_score: timestamp时间戳
        :return:
        """
        return self.redis.zremrangebyscore(name, start_score, end_score)

    def get_zadd_timestamp_range(self, name):
        """
        获取指定name对应集合中的score最小值和最大值，只用于有序集合
        :param name:
        :return: [start_datetime, end_datetime]
        """
        status = self.exists(name)
        if status != 0:
            # 转换为datetime类型
            start_datetime = datetime.datetime.fromtimestamp(self.redis.zrange(name,
                                                                               start=0,
                                                                               end=0,
                                                                               desc=False,
                                                                               withscores=True)[0][1])
            end_datetime = datetime.datetime.fromtimestamp(self.redis.zrange(name,
                                                                             start=0,
                                                                             end=0,
                                                                             desc=True,
                                                                             withscores=True)[0][1])
            return [start_datetime, end_datetime]
        else:
            return []


if __name__ == '__main__':
    REDIS = Redis(host='172.16.40.34')
    ipcmac = 'B00000000032'
    # ipc = r'push:grant:dev:{}:*'.format(ipcmac)
    # print(ipc)
    # REDIS.delete(ipc)

    REDIS.delete_valu(ipcmac)
    # for i in a:
    #     REDIS.delete(i)
    # a = REDIS.redis.keys(ipc)
    # print(a)
    # REDIS.delete(ipc)
    # 测试set
    # REDIS.set(name='name', value='Evan', do_pickle=True, expire=60)
    # REDIS.set(name='id', value=6, do_pickle=True, expire=60)
    # print(REDIS.get_set_value('name', do_pickle=True))
    # print(REDIS.get_set_all())
    # # 测试有序集合
    # REDIS.zadd(name='demo', value=[{'name': 'Evan'}, {'id': 6}], do_pickle=True, expire=60)
    # print(REDIS.get_zadd_data_by_score(name='demo', do_pickle=True))
    # print(REDIS.get_zadd_timestamp_range(name='demo'))
