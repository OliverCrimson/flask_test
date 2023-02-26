from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
database_ = SQLAlchemy(app)







@app.route('/')
def index():  # put application's code here
    return render_template('index.html', title='home')


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            database_.session.add(article)
            database_.session.commit()
            return redirect('/posts')
        except:
            return f'Error while adding an article'

    else:
        return render_template('create_article.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id_article>')
def posts_details(id_article):
    article = Article.query.get(id_article)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id_article>/delete')
def post_delete(id_article):
    article = Article.query.get_or_404(id_article)
    try:
        database_.session.delete(article)
        database_.session.commit()
        return redirect('/posts')
    except:
        return 'Error while deleting post'


@app.route('/posts/<int:id_article>/update', methods=['POST', 'GET'])
def post_update(id_article):
    article = Article.query.get(id_article)
    if request.method == 'POST':
        article.tile = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            database_.session.commit()
            return redirect('/posts')
        except:
            return 'Error while editing an article'
    else:
        return render_template('post_update.html', article=article)


@app.route('/about')
def about():
    return render_template('/about.html', title='about')


class Article(database_.Model):
    id_article = database_.Column(database_.Integer, primary_key=True)
    title = database_.Column(database_.String(100), nullable=False)
    intro = database_.Column(database_.String(300), nullable=False)
    text = database_.Column(database_.Text, nullable=False)
    date = database_.Column(database_.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id_article

if __name__ == '__main__':
    app.run(debug=True)
