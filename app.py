import os
import sys
import click
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
print(WIN)
if WIN:  # 如果是Windows系统，使用三个斜线
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 初始化扩展，传入程序实例 app
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev'

@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
# Initialize the database
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
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
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done')

@app.route('/user/<name>')
def user_page(name):
    return "你是输入的User时{}：".format(name)

# 模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是post请求
        # 获取表单数据
        title = request.form.get('title')   # 传入表单对应输入字段的name的值
        year = request.form.get('year')
        #验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  #显示错误提示

            return redirect(url_for('index'))   # 重定向回主页
        # 保存表单数据到数据库
        print("保存表单到数据库")
        movie = Movie(title=title,year=year) # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        return redirect(url_for('index'))
    user = User.query.first()
    movies = Movie.query.all()  # 读取所有电影记录
    print("显示所有电影")
    return render_template('index.html', user=user, movies=movies)
    # return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
    # return 'Hello'
    # return '<h1>Hello Totoro!</h1><img src="https://img.soogif.com/NQy8FNhHUebORPnFRkJogMVARjCvkpRv.gif">'


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': #处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title
        movie.year = year
        db.session.commit()
        flash("Item updated.")
        return redirect(url_for('index'))
    # 传入被编辑的电影记录
    return render_template('edit.html', movie=movie)



# 删除电影条目
@app.route('/movies/delete/<int:movie_id>', methods=['POST'])
# 限定只接受POST请求
def delete(movie_id):
    movie = Movie.query.get(movie_id) # 获取电影记录
    db.session.delete(movie) # delete对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted')
    return redirect(url_for('index'))


@app.errorhandler(404)   #传入要处理的错误代码
def page_not_found(e):   # 接受异常对象作为参数
    return render_template('404.html'),404  # 返回模板和状态码



@app.route('/test')
def test_url_for():
    # 下面时一些调用示例（请在命令行窗口查看输出的URL）
    print(url_for('hello'))
    print(url_for('user_page', name='小明'))
    print(url_for('user_page', name='小红'))
    print(url_for('test_url_for', nm=2))
    return "Test Page"


# if __name__ == '__main__':
#     app.run()