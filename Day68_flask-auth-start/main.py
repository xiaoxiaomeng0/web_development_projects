from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'randomsecreteformyuse'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template("index.html", user=current_user)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"), salt_length=8)
        check_if_exist = User.query.filter_by(email=email).first()
        if not check_if_exist:
            new_user = User(email=email, password=password, name=name)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("secrets"))
        flash("Username or email exists! Try again!")
    return render_template("register.html", user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()
        if not user:
            flash("Username does not exist, please try again!")
        else:
            if check_password_hash(user.password, request.form.get("password")):
                login_user(user)
                flash("logged in Successfully.")
                return redirect(url_for("secrets"))
            flash("username and password does not match! Please try again.")
    return render_template("login.html", user=current_user)


@app.route('/secrets')
@login_required
def secrets():
    if current_user.is_authenticated:
        return render_template("secrets.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/download')
@login_required
def download():
    return send_from_directory("static", "files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
