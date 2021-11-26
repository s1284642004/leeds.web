# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import hashlib
import sqlite3
from flask import Flask, render_template, request,redirect,make_response

global account
global count
global con
global cur
global username
global password
global use
global situation
use = []
account = []
count = []
app = Flask(__name__)


def get_account():
    con = sqlite3.connect("DEMO.db")
    cur = con.cursor()
    cur.execute("select username,password from DEMO")
    con.commit()
    for i in range (0,len(account)):
        account.pop()
    # account.clear()
    account.append(cur.fetchall())
    return

def encrpt(s):
    a = hashlib.md5(s.encode('utf-8'))
    a = a.hexdigest()
    return a
def get_count(s):
    con = sqlite3.connect("DEMO.db")
    cur = con.cursor()
    k = "SELECT * FROM DEMO WHERE username = '"
    k += s
    k += "'"
    cur.execute(k)
    con.commit()
    for i in range(0, len(count)):
        count.pop()
    count.append(cur.fetchall())
    for i in range(0, len(use)):
        use.pop()

    for ak in range(0,len(count[0])):
        sb = ""
        sb += count[0][ak][2] + count[0][ak][3]+ count[0][ak][4]+ count[0][ak][5]
        if sb != "":
            use.append(count[0][ak])
    for i in range(0, len(count)):
        count.pop()
    count.append(use)
    con.close()

def login(a, b): # 0为登陆失败，1为登陆成功
    for i in range(0, len(account[0])):
        if a == account[0][i][0] and b == account[0][i][1]:
            return 1
    return 0


def search_username(s):  # 1为存在，0为不存在
    for i in range(0, len(account[0])):
        if s == account[0][i][0]:
            return 1
    return 0


@app.route('/', methods = ['GET', 'POST'])
def index():
    for i in range(0, len(count)):
        count.pop()
    if request.method == "POST":
        get_account()
        username = request.form.get('username_login')
        password = request.form.get('password_login')
        password = encrpt(password)
        if username == "" or password == "":
            return "<h1> Login failed. Please enter your username/password<h1> <a href = '/'>Back homepage</a>"
        elif search_username(username) == 0:
            return "<h1> The username is not registered <h1><a  display: block href = '/'>Back homepage</a> "
        elif login(username, password) == 0:
            return "<h1> Login failed. The username/password is incorrect <h1><a href = '/'>Back homepage</a>"
        elif login(username, password) == 1:
            return redirect('/user/' + username)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == "POST":
        get_account()
        username = request.form.get('username')
        password = request.form.get('password')
        password = encrpt(password)

        if username == "" or password == "":
            return "<h1> Fail to register <h1><a href = '/register'>Return to registration page</a>"
        elif search_username(username) == 1:
            return "<h1> The account has been registered <h1><a href = '/register'>Return to registration page</a>"
        else:
            account[0].append((username,password))
            cur.execute("INSERT INTO DEMO values(?,?,?,?,?,?,?)", (username, password, "welcome", "to", "use", "the system", 0))
            con.commit()
            return "<h1> Registered successfully <h1><a href = '/'>Back homepage</a>"
    return render_template('register.html')

@app.route('/add', methods=['GET', 'POST'])
def add_count():
    if request.method == "POST":
        ada = request.form.get('new_count')
        if ada == "确认添加":
            deadline = request.form.get('new_deadline')
            module_code = request.form.get('new_module_code')
            assessment_title = request.form.get('new_assessment_title')
            description = request.form.get('new_description')
            cur.execute("INSERT OR IGNORE INTO DEMO values(?,?,?,?,?,?,?)", (count[0][-1][0], count[0][-1][1], deadline, module_code,
                                                                   assessment_title, description, 0))
            con.commit()

        if ada == "确认":
            delete = int(request.form.get('delete'))
            delete = delete - 1
            if delete < 0 or delete >= len(count[0]):
                return"<h1> Please enter a correct ID <a href = '/'>log in again</a><h1>"
            sb = "UPDATE DEMO SET complete = 1 WHERE deadline = '"
            sb += str(count[0][delete][2])
            sb += "'AND module_code = '"
            sb += str(count[0][delete][3])
            sb +=  "'AND assessment_title = '"
            sb += str(count[0][delete][4])
            sb +=  "' AND description = '"
            sb += str(count[0][delete][5])
            sb += "'"
            cur.execute(sb)
            con.commit()
        return"<h1> Operation succeeded. Please log in again to view <a href = '/'>log in again</a><h1>"

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    choice = 2
    add = 0
    if request.method == "POST":  #判断展现哪些事件以及是否添加新事件
        st = request.form.get('choice')
        if st == "展示未完成事件":
            choice = 0
        elif st == "展示已完成事件":
            choice = 1
        elif st == "展示所有事件":
            choice = 2
        elif st == "添加新事件":
            add = 1
        '''elif st == "退出登录":
            return render_template('index.html')'''

        a = count[0]
        length = len(a)
        return render_template('user.html', choice=choice,name=name, count=a, length=length ,add = add)


    for i in range (0,len(count)):
        count.pop()
    get_count(name)
    a = count[0]
    length = len(a)
    return render_template('user.html', name=name, count=a, length=length, choice=choice)


if __name__ == '__main__':
    con = sqlite3.connect("DEMO.db",check_same_thread=False)
    cur = con.cursor()
    # sql = "CREATE TABLE IF NOT EXISTS DEMO(username TEXT ," \
    #        "password TEXT,deadline TEXT, modul" \
    #       "e_code TEXT, assessment_title TEXT,description TEXT, complete INTEGER)"
    #  cur.execute(sql)
    #  cur.execute("INSERT INTO DEMO values(?,?,?,?,?,?,?)", ("q3", "dwa", "dwa", "w", "sa", "d", 1))
    #  con.commit()
    app.run()