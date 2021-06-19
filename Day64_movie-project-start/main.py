from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from model import Movie, app, db
from form import UpdateRatingMovieForm, AddNewMovieForm

import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("MOVIE_API_KEY")

Bootstrap(app)

@app.route("/")
def home():
    all_movies = Movie.query.all()
    ordered_movie_list = Movie.query.order_by(Movie.rating.desc()).all()
    print(ordered_movie_list)
    movie_list_length = len(ordered_movie_list)
    for i in range(movie_list_length):
        ordered_movie_list[i].ranking = i + 1
        movie_list_length -= 1
    return render_template("index.html", all_movies=ordered_movie_list)

@app.route("/add", methods=["GET", "POST"])
def add():
    new_form = AddNewMovieForm()
    if new_form.validate_on_submit():
        title = new_form.new_movie_title.data
        url = "https://api.themoviedb.org/3/search/movie"
        paramters = {
            "api_key": api_key,
            "query": title,
        }
        response = requests.get(url=url, params=paramters)
        results = response.json()["results"]
        return render_template("select.html", all_movies=results)
    return render_template("add.html", form=new_form)

@app.route("/select")
def select():
    movie_id = request.args.get("tmdb_id")
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    paramters = {
        "api_key": api_key,
    }
    response = requests.get(url=url, params=paramters)
    result = response.json()
    new_movie = Movie(
        title=result["original_title"],
        year=result["release_date"].split("-")[0],
        description=result["overview"],
        rating=result["vote_average"],
        ranking=1,
        review="",
        img_url=f"https://image.tmdb.org/t/p/w500/{result['poster_path']}"
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_added = Movie.query.filter_by(title=new_movie.title).first()
    return redirect(url_for("edit", id=movie_added.id))

@app.route("/movie/<int:id>", methods=["GET", "POST"])
def edit(id):
    edit_movie = Movie.query.get(id)
    new_form = UpdateRatingMovieForm()
    if request.method == "POST":
        edit_movie.rating = new_form.new_rating.data
        edit_movie.review = new_form.new_review.data
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", form=new_form, movie=edit_movie)

@app.route("/delete")
def delete():
    delete_movie_id = request.args.get("id")
    delete_movie = Movie.query.get(delete_movie_id)
    db.session.delete(delete_movie)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
