# 導入相對應的套件
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import pymysql
# pymysql.install_as_MySQLdb()

# 創建了一個flask的實例
app = Flask(__name__)

'''
在Flask項目中，我們會用到很多配置（Config） 像是以下的密鑰以及資料庫
Session, Cookies以及一些第三方擴展都會用到SECRET_KEY值
這是一個比較重要的配置值，如未使用，會出現以下錯誤
the session is unavailable because no secret key was set.
Set the secret_key on the application to something unique and secret
'''
# 導入DB相關設置
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''定義Message模型 (DB)'''


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)

    def __init__(self, name, title, content):

        self.name = name
        self.title = title
        self.content = content


@app.route('/')
def index():
    """
    在前端顯示message_crud表中的所有資料並依照id大小作排序
    """

    all_data = Message.query.all()
    # 透過 render_template() 這個函式輕鬆地呈現出 HTML 網頁的樣式
    # 將取得資料再傳入到html內 (將參數帶回頁面)
    return render_template('index2.html', message=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        # 取得表單中的資料 (html) 並準備傳送到資料庫(mysql)
        name = request.form['name']
        title = request.form['title']
        content = request.form['content']

        my_data = Message(name, title, content)
        # 利用 add 的方法即可新增單筆資料
        db.session.add(my_data)
        # 將之前的操作變更至資料庫中
        db.session.commit()
        # 利用flash將訊息由後端傳到前端
        flash("新增留言成功")
        # 找到function名稱為index指向的路由顯示出來並重新刷新
        return redirect(url_for('index'))


@ app.route('/update', methods=['GET', 'POST'])
def update():
    """
    更改留言版的留言，並在前端刷新及顯示message_crud表中的所有資料並依照id大小作排序
    """

    if request.method == 'POST':
        my_data = Message.query.get(request.form.get('id'))
        # 取得表單中的資料 (html) 並準備傳送到資料庫(mysql)
        my_data.name = request.form['name']
        my_data.title = request.form['title']
        my_data.content = request.form['content']
        # 將之前的操作變更至資料庫中
        db.session.commit()
        # 利用flash將訊息由後端傳到前端
        flash("更新此則留言成功")
        # 找到function名稱為index指向的路由顯示出來並重新刷新
        return redirect(url_for('index'))


@ app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    """
    刪除留言，並在前端刷新及顯示message_crud表中的所有資料並依照id大小作排序
    """

    my_data = Message.query.get(id)
    # 利用 delete 的方法即可刪除單筆資料
    db.session.delete(my_data)
    # 將之前的操作變更至資料庫中
    db.session.commit()
    # 利用flash將訊息由後端傳到前端
    flash("已成功刪除此則留言")
    # 找到function名稱為index指向的路由顯示出來並重新刷新
    return redirect(url_for('index'))


if __name__ == "__main__":
    # 由於在開發階段，將debug設為True
    app.run(debug=True)
