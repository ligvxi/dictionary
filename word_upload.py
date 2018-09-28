from mysqlpy import mysqlhelp
import re

mysql = mysqlhelp('dict')
try:
    f = open('dict.txt', 'r')
    for i in f:
        # print(i)
        word = re.match('\S*', i).group()
        print(word)

        disception = re.sub('^\S*', '', i).strip(' ')
        print(disception)
        ins = 'insert into word values(%s,%s)'
        mysql.work(ins, L=[word, disception])
    f.close()
except OSError:
    print('打开失败')
except Exception as e:
    print(e)
