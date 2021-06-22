from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content")
    submit = SubmitField("Submit Post")

def time_formatted():
    now = datetime.datetime.now()
    year = now.year
    month = now.strftime("%B")
    day = now.strftime("%-d")
    return f"{month} {day}, {year}"

@app.route('/')
def get_all_posts():
    posts = BlogPost.query.filter_by().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    # posts = db.session.query(BlogPost).all()
    requested_post = BlogPost.query.filter_by(id=index).first()
    return render_template("post.html", post=requested_post)


@app.route("/new", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    print(form.title)
    if form.validate_on_submit():
        add_new_post = BlogPost(title=form.title.data,
                                subtitle=form.subtitle.data,
                                body=form.body.data, # or request.form.get("body")
                                author=form.author.data,
                                date=time_formatted(),
                                img_url=form.img_url.data)
        db.session.add(add_new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    if post:
        edit_form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            img_url=post.img_url,
            author=post.author,
            body=post.body
        )
        if edit_form.validate_on_submit():
            post.title = edit_form.title.data
            post.subtitle = edit_form.subtitle.data
            post.img_url = edit_form.img_url.data
            post.author = edit_form.author.data
            post.body = edit_form.body.data
            # post.date = time_formatted()
            db.session.commit()
            return redirect(url_for("show_post", index=post.id))
        return render_template("make-post.html", form=edit_form)
    return jsonify(error="Post Not Found")


@app.route("/delete/<int:post_id>")
def delete(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return jsonify(error="Post Not Found")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)