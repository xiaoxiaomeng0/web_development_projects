from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return "<Book %r>" % self.title

db.create_all()
# book2 = Book(title="Harry Potter6", author="J.K. Rowling6", rating=9.3) #The primary key is optional.
# db.session.add(book2)
# db.session.commit()

@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return render_template("index.html")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    update_book = Book.query.get(id)
    if request.method == "POST":
        update_book.rating = request.form["new_rating"]
        db.session.commit()
        return redirect("/", code=302)

    return render_template("edit.html", book=update_book)

if __name__ == "__main__":
    app.run(debug=True)

