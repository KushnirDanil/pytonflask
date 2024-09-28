# pip install flask-sqlalchemy
from datetime import datetime

from flask import Flask, render_template
from flask import  request
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# 1. Налаштування
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Запуск бази даних
# database = SQLAlchemy
db = SQLAlchemy(app)


# 3 Створення таблиці
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    role = db.Column(db.Integer(), default=0, nullable=False)

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_name = db.Column(db.String(255), nullable=False)
    post_text = db.Column(db.Text(), nullable=False)
    post_image = db.Column(db.String(255), nullable=False)
    continent = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.Date(), default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

#with app.app_context():
#    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/articles')
def articles():
    new_articles = ['How to avoid expensive travel mistakes', 'Top 5 places to experience supernatural forces',
                    'Three wonderfully bizarre Mexican festivals', 'The 20 greenest destinations on Earth',
                    'How to survive on a desert island']
    return render_template('articles.html', articles=new_articles)

@app.route('/add_post')
def add_post():
    return render_template('add_post.html')


@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User( username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('index.html')
    else:
        return render_template('add_user.html')

# Лише для локаотного сервера (закоментувати)
if __name__ == '__main__':
    app.run(debug=True)
