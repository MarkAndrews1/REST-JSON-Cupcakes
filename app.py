"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'helloimasecret'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    return render_template('homepage.html')

# API ROUTES

@app.route('/api/cupcakes', methods=["GET"])
def list_cupcakes():
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]
    return jsonify(serialized)

@app.route('/api/cupcakes', methods=["POST"])
def add_cupcake():
    new_cupcake = Cupcake(
       flavor = request.json["flavor"],
       size = request.json["size"],
       rating = request.json["rating"],
       image = request.json["image"] or None
       )
    
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()
    return (jsonify(serialized), 201)

@app.route('/api/cupcakes/<int:id>')
def view_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    return jsonify(serialized)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    
    cupcake.flavor = request.json["flavor"],
    cupcake.size = request.json["size"],
    cupcake.rating = request.json["rating"],
    cupcake.image = request.json["image"]
    
    serialized = cupcake.serialize()
    return jsonify(serialized)

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def remove_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(msg="Deleted")