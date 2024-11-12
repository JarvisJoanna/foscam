import pymssql
import time
import pandas as pd


class MSSQL:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        # 查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行非查询语句

        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


def main():
    # host默认为127.0.0.1，如果打开了TCP动态端口的需要加上端口号，如'127.0.0.1:1433'
    # user默认为sa
    # pwd为自己设置的密码
    # db为数据库名字
    ms = MSSQL(host='172.16.8.199', user="sa", pwd="foscam.com_123", db="MESTESTDB01")
    # resList = ms.ExecQuery("SELECT * FROM UIDTA;")
    # print(resList)
    return ms


def formantuid(ipcuid):
    """输入uid格式：uid（24位）@uid密码（8位）"""
    date = time.strftime('%Y%m%d')
    uidlist = ipcuid.split("@")[0]
    uid1 = uidlist[0:20]
    uid2 = uidlist[20:]
    sql1 = "INSERT INTO UIDTA(TA001,TA002,TA005,TA006,TA007,TA009,TA011,TA012,TA013) VALUES('AIOAF{}01','','{}','u={};e={}','5300-{}01','DB4','3',GETDATE(),'CON_IN');".format(
        date, ipcuid, uid1, uid2, date
    )
    sql2 = "INSERT INTO UIDTD(TD001,TD002,TD003,TD004,TD006,TD007,TD008) VALUES('AIOAF{}01','DB4','','C2222','0',GETDATE(),'5300-{}01'); ".format(
        date, date
    )
    return sql1, sql2


if __name__ == '__main__':
    # uid = '3YOM3Z4AB2DJ5Q26DTZZZCJB@8syV5l4h'
    mysql = main()
    aa = mysql.ExecQuery("SELECT * FROM UIDTA;")
    print(aa)
    # sqls = formantuid(uid)
    # for i in sqls:
    #     mysql.ExecNonQuery(i)
    file = r'D:\Python_test\foscam_delete_server\foscam\Thor-UID和密码-10-ZZZCJB--20240507065649.csv'
