import config
import traceback
from datetime import timedelta, datetime

today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')


def get_checks():
    conn_mssql = config.get_connection_mssql()
    sql_query = 'SELECT * FROM Prod_CheckInfo WHERE Day_id LIKE \'%s%%\';' % yesterday
    cursor = conn_mssql.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn_mssql.close()
    return result


def get_bp():
    conn_mysql = config.get_connection_mysql()
    sql_query = 'SELECT * FROM boarding_passes WHERE date LIKE \'%s%%\';' % yesterday
    cursor = conn_mysql.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn_mysql.close()
    return result


def get_checks_shop(shop):
    conn_mssql = config.get_connection_mssql()
    sql_query = 'SELECT * FROM Prod_CheckInfo WHERE Day_id LIKE \'%s%%\' AND Shop_Name = \'%s\';' % (yesterday, shop)
    cursor = conn_mssql.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn_mssql.close()
    return result


def add_main(check_list):
    conn_mysql = config.get_connection_mysql()
    mysql_cursor = conn_mysql.cursor()
    conn_mssql = config.get_connection_mssql()
    mssql_cursor = conn_mssql.cursor()
    for key, value in check_list.items():
        checks_query = 'SELECT * FROM Prod_CheckInfo WHERE fiscalsign = \'%s\';' % value
        mssql_cursor.execute(checks_query)
        checks = mssql_cursor.fetchall()
        bp_query = 'SELECT * FROM boarding_passes WHERE id = \'%s\';' % key
        mysql_cursor.execute(bp_query)
        bp = mysql_cursor.fetchone()
        for check in checks:
            n_cat = ''
            if check.category is None:
                n_cat = 'None'
            else:
                n_cat = check.category
            print(n_cat)
            sql_query = 'INSERT INTO main (route, airline, flight, airport, article_name, category, arendator_name, ' \
                        'shop_name, user_inn, day_id, check_date, revenue, fiscal_sign, qnty) VALUES ' \
                        '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', ' \
                        '\'%s\', \'%s\', \'%s\', \'%s\');' \
                        % (bp['route'], bp['airline'], bp['flight'], check.Airport, check.article_name, n_cat,
                           check.arendator_name, check.Shop_Name, check.userInn, check.Day_id, check.check_date,
                           check.Revenue, check.fiscalsign, check.Qnty)
            mysql_cursor.execute(sql_query)
            conn_mysql.commit()
    conn_mssql.close()
    conn_mysql.close()
