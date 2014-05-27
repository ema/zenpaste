from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paste.db'
db = SQLAlchemy(app)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contents = db.Column(db.Text)

@app.route("/newpost", methods=['PUT'])
def newpost():
    post = Post(contents=request.data)
    db.session.add(post)
    db.session.commit()
    return str(post.post_id)

@app.route("/p/<int:post_id>", methods=['GET'])
def show_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    return render_template('post.html', post_id=post_id,
        contents=post.contents)

@app.route("/", methods=['GET'])
def index():
    """The homepage"""
    return render_template('pastebin.html')

if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
