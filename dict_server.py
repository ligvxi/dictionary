from socket import *
import sys
import os
import time
import signal
import pymysql

# 定义全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST, PORT)

# 流程控制


def main():
    # 创建数据库链接
    db = pymysql.connect('localhost', 'root', '123456', 'dict')
    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)
    # 忽略子进程信号
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
            print("Connect from ", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            do_child(c, db)
        else:
            c.close()
            continue


def do_child(c, db):
    while True:
        data = c.recv(1024).decode()
        if (not data) or (data[0] == 'E'):
            c.close()
            sys.exit(0)
        elif data[0] == 'R':
            do_register(c, db, data)
        elif data[0] == 'L':
            do_login(c, data, db)
        elif data[0] == 'Q':
            do_query(c, db, data)
        elif data[0] == 'H':
            do_hist(c, db, data)


def do_login(c, data, db):
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cur = db.cursor()
    sql = 'select * from user where username = %s and password = %s'
    cur.execute(sql, [name, passwd])
    r = cur.fetchone()
    if r == None:
        c.send(b'FALL')
    else:
        c.send(b'OK')


def do_register(c, db, data):
    print("注册操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cur = db.cursor()
    sql = "select * from user where username = '%s'" % name
    cur.execute(sql)
    r = cur.fetchone()
    if r != None:
        c.send(b"EXISTS")
        return
    sql = 'insert into user (username,password) values(%s,%s)'
    try:
        cur.execute(sql, [name, passwd])
        db.commit()
        c.send(b"OK")
    except:
        db.rollback()
        c.send(b'fall')
    else:
        print('%s注册成功' % name)


def do_query(c, db, data):
    l = data.split(' ')
    name = l[1]
    word = l[2]
    cur = db.cursor()

    def insert_history():
        sql = 'insert into history(username,word)\
        values(%s,%s)'
        try:
            cur.execute(sql, [name, word])
            db.commit()
        except Exception as e:
            print("失败", e)
            db.rollback()
    # 文本查询
    try:
        f = open(DICT_TEXT)
    except:
        c.send(b'FALL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FALL')
            f.close()
            return
        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()


def do_hist(c, db, data):
    l = data.split(' ')
    name = l[1]
    cur = db.cursor()
    sql = 'select * from history where username =%s'
    cur.execute(sql, [name])
    r = cur.fetchall()
    if not r:
        c.send(b'FALL')
    else:
        c.send(b'OK')
    for i in r:
        time.sleep(0.1)
        msg = '%s %s %s' % (i[0], i[1], i[2])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ == "__main__":
    main()
