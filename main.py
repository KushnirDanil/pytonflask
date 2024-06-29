from flask import Flask, render_template

app = Flask(__name__)




@app.route('/')
@app.route('/name')
def index(name=''):
    return render_template('index.html', name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/details')
def details():
    return render_template('details.html')

# Лише для локального сервера  (за коментувати)
if __name__ == '__main__':
    app.run(debug=True)

