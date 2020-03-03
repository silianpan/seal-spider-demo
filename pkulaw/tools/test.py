
from mysql_util import MysqlUtil

if __name__ == '__main__':
    sql = MysqlUtil()
    ret = {'title': '123', 'url': '123', 'content': '123'}
    sql.insert('law_test', **ret)
