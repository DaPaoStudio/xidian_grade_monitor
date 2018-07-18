import sqlite3
DB = 'db.sqlite'


def create_tables_users(all_users):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS users')
    cur.execute(
        'CREATE TABLE users ('
        'account TEXT PRIMARY KEY,'
        'passwd TEXT,'
        'name TEXT,'
        'email TEXT'
        ')'
    )
    conn.commit()
    for user in all_users:
        cur.execute('INSERT INTO users VALUES (?, ?, ?, ?)', user)
    conn.commit()
    conn.close()


def create_table_grades():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS grades')
    cur.execute(
        'CREATE TABLE grades ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'account TEXT,'  # foreign key references user(account).
        'course_id TEXT,'
        'class_id TEXT,'
        'course_name TEXT,'
        'course_name_en TEXT,'
        'credit TEXT,'
        'type TEXT,'
        'grade TEXT'
        ')'
    )
    conn.commit()


def select_all_grades(account):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    res = cur.execute('SELECT course_id, class_id, course_name, course_name_en, credit, type, grade '
                      'FROM grades WHERE account = ?', (account, )).fetchall()
    conn.close()
    return res


def insert_into_grades(grades):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    for grade in grades:
        cur.execute('INSERT INTO grades VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?)', grade)
    conn.commit()
    conn.close()
