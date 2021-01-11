import pymysql.cursors
import pyodbc

test_id = 0


def get_connection_mysql():
    connection = pymysql.connect(host='***',
                                 user='***',
                                 password='***',
                                 db='arenda',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


def get_connection_mssql():
    connection = pyodbc.connect('Driver={SQL Server};'
                                'Server=***;'
                                'Database=GCP;'
                                'UID=***;'
                                'PWD=***')
    return connection
