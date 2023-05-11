from flask import Flask,url_for

app = Flask(__name__)
@app.route('/user/<name>')
def user_page(name):
    return "你是输入的User时{}：".format(name)

@app.route('/')
def hello():
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    return 'Hello'
    # return '<h1>Hello Totoro!</h1><img src="https://img.soogif.com/NQy8FNhHUebORPnFRkJogMVARjCvkpRv.gif">'

@app.route('/test')
def test_url_for():
    # 下面时一些调用示例（请在命令行窗口查看输出的URL）
    print(url_for('hello'))
    print(url_for('user_page', name='小明'))
    print(url_for('user_page', name='小红'))
    print(url_for('test_url_for', nm=2))
    return "Test Page"