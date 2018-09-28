from pymysql import *


class mysqlhelp:
    def __init__(self, database, host='localhost', user='root', password='123456', charset='utf8', port=3306):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port

    # 链接数据库创建
    def open(self):
        self.conn = connect(host=self.host, user=self.user, password=self.password,
                            database=self.database, charset=self.charset, port=self.port)
        self.cur = self.conn.cursor()

    # 关闭方法
    def close(self):
        self.cur.close()
        self.conn.close()
    # 执行SQL语句

    def work(self, sql, L=[]):
        self.open()
        try:
            self.cur.execute(sql, L)
            self.conn.commit()
            # print("ok")
        except Exception as e:
            self.conn.rollback()
            print("Failed", e)

        self.close()

    # 执行查询方法

    def getall(self, sql, L=[]):
        self.open()
        self.cur.execute(sql, L)
        # print("ok")
        result = self.cur.fetchall()
        self.close()
        return result


# if __name__ == "__main__":
    # 测试
    # mysql = mysqlhelp("MOSHOU")
    # insert = 'insert into hero(id) values(89);'
    # mysql.work(insert)
    # select = 'select name from hero'
    # print(mysql.getall(select))
