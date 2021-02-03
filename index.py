# 導入相對應的套件
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder


# 創建了一個flask的實例
app = Flask(__name__)


# 導入DB相關設置
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)


'''定義Message模型 (DB)'''


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'id=%r, title=%r,content=%r' % (self.id, self.title, self.content)

    # def __repr__(self):
    #     return 'id: %r' % self.id

    # def __init__(self, user_id, title, content):

    #     self.user_id = user_id
    #     self.title = title
    #     self.content = content


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    name = db.Column(db.String(100), nullable=False)
    # relationship
    messages = db.relationship('Message', backref='user')

    def __repr__(self):
        return 'id=%r, User_name=%r' % (self.id, self.name)

    # def __init__(self, name, messages, city_id):

    #     self.name = name
    #     self.messages = messages
    #     self.city_id = city_id


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # relationship
    users = db.relationship('User', backref='city')

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return 'id=%r, city_name=%r' % (self.id, self.name)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # 抓取並回傳整個form資料 (測試用看是否有正確抓到)
        # return request.form
        # 抓取並回傳整個form資料中的城市id
        # return request.form['city_select']
        user_name = request.form['user_name']
        # 抓取form中的城市id
        city_id = request.form['city_select']

        # select_city = City.query.filter_by(name="Taipei")
        creater_user = User(city_id=city_id, name=user_name)
        db.session.add(creater_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/add', methods=["POST", "GET"])
def add():
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        user_name = request.form['user_name']
        select_user = User.query.filter_by(
            name=user_name)  # 先取得在user當中naem='Eric'的User_id
        # 在Message()這張表單新增資料
        create_Eric_Messags = Message(
            user_id=select_user[0].id, title=title, content=content)
        db.session.add(create_Eric_Messags)  # 建立資料暫存
        db.session.commit()  # 傳送至資料庫
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<message_id>', methods=['GET', 'POST'])
def delete(message_id):
    # if request.method == "POST":
    select_message = Message.query.filter_by(id=int(message_id)).first()
    # 利用 delete 的方法即可刪除單筆資料
    db.session.delete(select_message)
    # 將之前的操作變更至資料庫中
    db.session.commit()
    return redirect(url_for('index'))
    # return render_template('delete.html')


@app.route('/update/<message_id>', methods=["POST", "GET"])  # 小心同名子不行
def update(message_id):
    if request.method == "POST":
        content = request.form['content']
        title = request.form['title']
        # update_title = request.form['update_title']
        select_message = Message.query.filter_by(id=int(message_id)).first()
        select_message.title = title
        select_message.content = content
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html')


@app.route('/', methods=["POST", "GET"])  # 小心同名子不行
def index():
    all_data = Message.query.all()

    if request.method == "POST":
        id_data = request.form['id']
        content = request.form['content']
        title = request.form['title']
        select_message = Message.query.filter_by(id=int(id_data)).first()
        select_message.title = title
        select_message.content = content
        db.session.commit()
        # return redirect(url_for('index'))
    return render_template('new_crud_index.html', Messages=all_data)


@app.route('/editdb')
def editdb():

    # 刪除資料庫
    # db.drop_all()
    # return "資料庫刪除成功"

    # 創建資料庫
    # db.create_all()
    # return "資料庫創建成功"

    # 增加資料
    # city_taipei = City(name='Taipei')

    # city, user 要跟上面的backref變數名稱一樣
    # user_eric = User(name='Eric', city=city_taipei)
    # user_deemo = User(name='Deemo', city=city_taipei)
    # user_grace = User(name='Grace', city=city_taipei)

    # db.session.add_all([user_eric, user_deemo, user_grace])
    # message_test = MessageNew(title='welcome words',
    #                           content='Hello yoyo', user=user_eric)

    # db.session.add_all([city_taipei, user_eric, message_test])
    # db.session().delete(city_taipei.id[0])

    # db.session.commit()
    # return "添加資料成功"

    return render_template('index2.html', message=all_data)


if __name__ == '__main__':
    app.run(debug=True)
