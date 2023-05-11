from flask import Flask, url_for, render_template

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

a = 'dd'
app = Flask(__name__)


@app.route('/user/<name>')
def user_page(name):
    return "你是输入的User时{}：".format(name)


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies, a=a)
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    # return 'Hello'
    # return '<h1>Hello Totoro!</h1><img src="https://img.soogif.com/NQy8FNhHUebORPnFRkJogMVARjCvkpRv.gif">'


@app.route('/test')
def test_url_for():
    # 下面时一些调用示例（请在命令行窗口查看输出的URL）
    print(url_for('hello'))
    print(url_for('user_page', name='小明'))
    print(url_for('user_page', name='小红'))
    print(url_for('test_url_for', nm=2))
    return "Test Page"
