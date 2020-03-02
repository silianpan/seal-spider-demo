
from mysql_util import MysqlUtil

if __name__ == '__main__':
    sql = MysqlUtil()
    sql.insert('law_test', {'title': 'test', 'url': 'test', 'content': 'test'})
