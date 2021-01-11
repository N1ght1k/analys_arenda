import config
import sql_queries
import traceback
from datetime import timedelta, datetime

today = datetime.today()
yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
check_list = {}
checks = sql_queries.get_checks()
boarding_passes = sql_queries.get_bp()

if config.test_id == 0:
    for bp in boarding_passes:
        checks_shop = sql_queries.get_checks_shop(bp['shop'])
        for check in checks_shop:
            check_date = check.check_date[:-1]
            check_date = datetime.strptime(check_date, '%Y-%m-%d %H:%M:%S.%f')
            print(check_date)
            print(bp['date'])
            print(check_date - bp['date'])
            if check_date - bp['date'] < timedelta(minutes=2) and (check_date - bp['date']).total_seconds() > 0:
                check_list[bp['id']] = check.fiscalsign
                break
    sql_queries.add_main(check_list)
    print(check_list)
else:
    for bp in boarding_passes:
        check_list[bp['id']] = bp['fiscal_sign']
    sql_queries.add_main(check_list)
