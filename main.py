# pip install flask-sqlalchemy
from crypt import methods
from datetime import datetime
from pyexpat.errors import messages
from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 1. Налаштування
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key='aaieLF0AKDtpzQzpJ93oMAx-rxF1R_w2KPdb_uHrSjw'

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


# Інший варіант

#    def __init__(self, title,text):
#        self.post_name = title
#        self.post_text =  text + 'New tesxt'
#        ...

#    row = Posts(title=post_text,
#               ...)


    def __repr__(self):
        return f'<User {self.username}>'

#with app.app_context():
#    db.create_all()

@app.route('/')
def index():
    x = session.get('username')
    return render_template('index.html', username=x)

@app.route('/login', methods=['GET'])
def login():
    message = 'Enter you login and password'
    return render_template('login.html', message=message)

@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        message = 'Enter correct email'
        return render_template('login.html', message=message)
    else:
        if user.password != password:
            message = 'Enter correct password'
            return render_template('login.html', message=message)
        else:
            session['username'] = user.username

            return redirect('/')
            #return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/articles')
def articles():
    articles = Posts.query.all()
    return render_template('articles.html',
                           articles=articles)

@app.route('/add_post', methods=['GET'])
def add_post():
    if not session.get('username'):
        return redirect('/login')

    return render_template('add_post.html')

@app.route('/add_post',  methods=['POST'])
def add_post_form():
    if not session.get('username'):
        return redirect('/login')

    post_name = request.form['text']
    post_text = request.form['text']
    post_image = request.form['URL']
    continent = request.form['continent']

    row = Posts(post_name=post_name,
                post_text=post_text,
                post_image=post_image,
                continent=continent)
    db.session.add(row)
    db.session.commit()

    return render_template('add_post.html')

@app.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    if not session.get('username'):
        return redirect('/login')

    if request.method == 'POST':
        id_list = request.form.getlist('id')
        for id in id_list:
            row = Posts.query.filter_by(id=id).first()
            db.session.delete()

        db.session.commit()

    articles = Posts.query.all()
    return render_template('delete_post.html', articles=articles)

@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if not session.get('username'):
        return redirect('/login')

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


@app.route('/logout')
def logout():
    if not session.get('username'):
        return redirect('/login')

    session.clear()
    return redirect('/')

# Лише для локаотного сервера (закоментувати)
if __name__ == '__main__':
    app.run(debug=True)

