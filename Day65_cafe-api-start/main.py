from flask import Flask, jsonify, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

API_KEY = "TopSecretAPIKey"

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random_choice():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(all_cafes)
    # cafe = jsonify(
    # jsonify the dictionary
    #     cafe=jsonify(
    #         # jsonify the cafe data
    #         id=random_cafe.id,
    #         name=random_cafe.name,
    #         map_url=random_cafe.map_url,
    #         img_url=random_cafe.img_url,
    #         location=random_cafe.location,
    #         seats=random_cafe.seats,
    #         has_toilet=random_cafe.has_toilet,
    #         has_wifi=random_cafe.has_wifi,
    #         has_sockets=random_cafe.has_sockets,
    #         can_take_calls=random_cafe.can_take_calls,
    #         coffee_price=random_cafe.coffee_price,
    #     ).json  # convert the Response object to a dictionary
    # )
    # return cafe

    return jsonify(cafe=random_cafe.to_dict())


## HTTP GET - Read Record
@app.route("/all")
def get_all():
    all_cafes = Cafe.query.filter_by().all()
    new_all_cafes = [cafe.to_dict() for cafe in all_cafes]
    return jsonify(cafes=new_all_cafes)


@app.route("/search")
def search():
    location = request.args.get("loc")
    find_cafes = Cafe.query.filter_by(location=location).all()
    if not find_cafes:
        return jsonify(error={"not Found": "Sorry, we don't have a cafe at that location."})
    new_find_cafes = [cafe.to_dict() for cafe in find_cafes]
    return jsonify(cafes=new_find_cafes)


## HTTP POST - Create Record
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("loc"),
            has_sockets=bool(request.form.get("sockets")),
            has_toilet=bool(request.form.get("toilet")),
            has_wifi=bool(request.form.get("wifi")),
            can_take_calls=bool(request.form.get("calls")),
            seats=request.form.get("seats"),
            coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        if new_cafe:
            return jsonify(response={"success": "Successfully added the new cafe."})
        return jsonify(response="None")
    return render_template("add.html")


## HTTP PUT/PATCH - Update Record
@app.route("/update-price/<cafe_id>", methods=["POST"])
def update(cafe_id):
    update_cafe = Cafe.query.filter_by(id=cafe_id).first()
    if update_cafe:
        update_cafe.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(success="Successfully updated the price.")
    return jsonify(error={"not Found": "Sorry, we don't have a cafe at that location."})


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.args.get("api-key")
    deleted_cafe = Cafe.query.filter_by(id=cafe_id).first()
    if api_key == API_KEY:
        db.session.delete(deleted_cafe)
        db.session.commit()
        return jsonify(response=f"Successfully deleted {deleted_cafe.name}")
    return jsonify(error={"not Found": "Sorry, we don't have a cafe at that location."})

if __name__ == '__main__':
    app.run(debug=True)
