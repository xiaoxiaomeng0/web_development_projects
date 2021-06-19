from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired

class UpdateRatingMovieForm(FlaskForm):
    new_rating = DecimalField("Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    new_review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")

class AddNewMovieForm(FlaskForm):
    new_movie_title = StringField("Movie Title", validators=[DataRequired()])
    add_button = SubmitField("Add Movie")