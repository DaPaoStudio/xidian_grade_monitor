import db_options
from get_my_grades import get_grades
from send_email import send
import time

USERS = [  # 用户列表
    # [学号, 教务处密码, 用户名（发邮件用）, 收件邮箱],
    ['16130120xxx', '000000', 'hhh', 'someone@example.com'],
    # 可以设置多用户，如果你会写Python的列表的话
]
SLEEP_TIME = 300  # 每个人之后休息几秒？一般不要小于10秒。

db_options.create_tables_users(USERS)  # 重置用户列表
db_options.create_table_grades()  # 重置成绩列表

while True:
    for user in USERS:
        for i in range(3):
            try:
                now_grades = list(get_grades(user[0], user[1]))
            except:
                continue
            break
        new_grades = now_grades.copy()
        old_grades = db_options.select_all_grades(user[0])
        for i in old_grades:
            try:
                new_grades.remove(i)
            except:
                pass

        if new_grades:
            print('%s，检查%d个成绩，%d个成绩改变' % (user[2], len(now_grades), len(new_grades)))
            insert_data = []
            for i in new_grades:
                temp = list(i)
                temp.insert(0, user[0])
                insert_data.append(temp)
            db_options.insert_into_grades(insert_data)

            try_times = 3
            while not send(
                    user[3],
                    [[i[0], i[2], i[5], i[6]] for i in new_grades],
                    [[i[0], i[2], i[5], i[6]] for i in now_grades],
                    user[2]
            ):
                try_times -=1
                print('邮件发送失败')
                if not try_times:
                    break
            else:
                print('邮件已发送')
            continue
        print('%s，检查%d个成绩，成绩未改变' % (user[2], len(now_grades)))
        time.sleep(SLEEP_TIME)
