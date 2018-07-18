import requests
import re
import time


def get_grades(username, password):
    if not username or not password:
        return None

    # Login
    s = requests.session()
    r1 = s.get('http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp')
    lt = re.search(r'name="lt" value="(.+?)"', r1.text).group()[17:-1]
    execution = re.search(r'name="execution" value="(.+?)"', r1.text).group()[24:-1]
    login_data = {
        'username': username,
        'password': password,
        'submit': u'',
        'lt': lt,
        'execution': execution,
        '_eventId': u'submit',
        'rmShown': u'1'
    }
    r2 = s.post('http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp', data=login_data)

    # Get grades
    reg = re.compile(
            r'<tr class="odd" onMouseOut="this.className=\'even\';" onMouseOver="this.className=\'evenfocus\';">\s+'
            r'<td align="center">\s+([\S\s]+?)\s+</td>\s+<td align="center">\s+([\S\s]+?)\s+</td>\s+'
            r'<td align="center">\s+([\S\s]+?)\s+</td>\s+<td align="center">\s+([\S\s]+?)\s+</td>\s+'
            r'<td align="center">\s+([\S\s]+?)\s+</td>\s+<td align="center">\s+([\S\s]+?)\s+</td>\s+'
            r'<td align="center">\s+<p align="center">([\S\s]+?)</P>'
        )
    grade_info = None
    for i in range(3):
        try:
            r1 = s.get('http://jwxt.xidian.edu.cn/gradeLnAllAction.do?type=ln&oper=sxinfo&lnsxdm=whatever').text  # 方案成绩
            grade_info = reg.search(r1)
        except:
            print('获取成绩信息失败，重试（%d）...' % (i + 1, ))
            time.sleep(2)
            continue
        if grade_info:
            print('获取成绩信息成功，正在解析...')
            break

    grades = []
    while grade_info:
        grade = list(grade_info.groups())
        grade[3] = grade[3] if grade[3] != '&nbsp;' else ''
        grade[6] = grade[6][:-6]
        r1 = r1[grade_info.end():]
        grades.append(tuple(grade))
        grade_info = reg.search(r1)

    # Logout
    r6 = s.post('http://jwxt.xidian.edu.cn/logout.do', data=login_data)
    return tuple(grades)
