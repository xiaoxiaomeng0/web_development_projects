from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "thisisasecrete"


class MyForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(),
                                             Email(),
                                             Length(min=6, max=120, message=(u'Too short for an email address?'))])
    password = PasswordField("password", validators=[DataRequired(),
                                                     Length(min=8, max=20, message=(u'The password needs to be at least 8 characters'))])
    submit = SubmitField(label="Log In")


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = MyForm()
    if form.validate_on_submit():
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            return render_template("success.html")
        return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
