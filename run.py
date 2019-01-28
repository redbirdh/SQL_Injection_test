from flask import Flask, render_template, request, redirect, url_for
import sqlite3
#from flask_bootstrap import Bootstrap

app = Flask(__name__)
#bootstrap = Bootstrap(app)

@app.route('/')
def hello():
    return 'ネットワーク委員会勉強会用SQLインジェクションのデモページです．/loginへアクセスしてください．'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message = "ISDL SECURE LOGIN")
    elif request.method == 'POST':
        name = request.form['name']
        passwd = request.form['passwd']
        submessage = ""
        authenticated = False

        # ユーザーをDBから探してパスワードが一致するか調べる（脆弱ポイント）
        sql_string = "SELECT * FROM users WHERE name='" + name + "' AND password='" + passwd + "'"
        #print(sql_string)
        c = sqlite3.connect('user.sqlite3').cursor()
        c.execute(sql_string)
        result = c.fetchall()
        submessage = sql_string
        if len(result) != 0:
            authenticated = True

        if authenticated:
            return render_template('login.html', name=name, submessage=submessage)
        else:
            submessage = "これ（' or 5=5 --）いれてみて..."
            return render_template('login.html', message="ISDL SECURE LOGIN", error="INVALID USER. TRY AGAIN.", submessage=submessage)

#=======================================
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('user.sqlite3')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("DROP TABLE IF EXISTS users")
            self.cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT PRIMARY KEY, password TEXT)")
            self.cur.execute("INSERT INTO users VALUES ('hyoneda', 'hyoneda')")
            self.conn.commit()
        except sqlite3.Error as e:
            print('######')
            print('sqlite3.Error occurred: ', e.args[0])
            print('######')
    def __del__(self):
        self.conn.close()
#=======================================

if __name__ == '__main__':
    db = DB()
    app.debug = True
    app.run(host='0.0.0.0')
