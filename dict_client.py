from socket import *
import sys
import getpass


def do_register(s):
    while True:
        name = input("请输入您的名字")
        password = getpass.getpass("请输入密码")
        password1 = getpass.getpass("请再次输入密码")
        if (' ' in name) or (' ' in password):
            print("用户名和密码不能有空格")
            continue
        if password != password1:
            print("两次密码输入不一致")
            continue
        msg = 'R {} {}'.format(name, password)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1
        else:
            return 2


def do_login(s):
    name = input("User")
    passwd = getpass.getpass("Password:")
    msg = 'L {} {}'.format(name, passwd)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        return name
    else:
        return


def do_query(s, name):
    while True:
        word = input("请输入单词")
        if word == '##':
            break
        msg = 'Q {} {}'.format(name, word)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print("没有查到该单词")

def do_hist(s, name):
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            print(data)
            if data == '##':
                break
    else:
        print("没有历史记录")


def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            ========welcome======
            1.注册  2.登录  3.退出
            =====================
            ''')
        try:
            cmd = int(input("请输入请求"))
        except Exception as e:
            print("命令错误")
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项")
            sys.stdin.flush()
            continue
        elif cmd == 1:
            r = do_register(s)
            if r == 0:
                print("注册成功")
            elif r == 1:
                print("用户已存在")
            elif r == 2:
                print("注册失败")
        elif cmd == 2:
            name = do_login(s)
            if name:
                print("登陆成功")
                login(s, name)
            else:
                print("用户名或密码不正确")
        elif cmd == 3:
            s.send(b'E')
            sys.exit("谢谢使用")


def login(s, name):
    while True:
        print('''
            ==========查询界面==========
            1.查询   2.历史记录   3.退出
            ===========================
            ''')
        try:
            cmd = int(input("请输入请求"))
        except Exception:
            print("命令错误")
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项")
            sys.stdin.flush()
            continue
        elif cmd == 1:
            do_query(s, name)
        elif cmd == 2:
            do_hist(s, name)
        elif cmd == 3:
            return


if __name__ == "__main__":
    main()
