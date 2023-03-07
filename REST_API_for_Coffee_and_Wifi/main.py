#
# 
# 
# 
# We can use Postman to test our api. You need to download it. I skipped it.
#
#
#
import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
        
        # Method 1
        # dicti = {}
        # for column in self.__table__.columns:
        #     dicti[column.name] = getattr(self, column.name)
        #     return dicti

        # Method 2
        return {column.name:getattr(self, column.name) for column in self.__table__.columns}




@app.route("/")
def home():
    return render_template("index.html")
    


## HTTP GET - Read Record
@app.route('/random')
def get_random():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    # return jsonify(cafe = {
    #     'id' : random_cafe.id.data,
    #     'name' : random_cafe.name.data,
    #     'map_url' : random_cafe.map_url.data,
    #     'img_url' : random_cafe.img_url.data,
    #     'location' : random_cafe.location.data,
    #     'amenities':{
    #     'seats' : random_cafe.seats.data,
    #     'has_toilet' : random_cafe.has_toilet.data,
    #     'has_wifi' : random_cafe.has_wifi.data,
    #     'has_sockets' : random_cafe.has_sockets.data,
    #     'can_take_calls' : random_cafe.can_take_calls.data,
    #     'coffee_price' : random_cafe.coffee_price.data
    #     }
    # })
    return jsonify(cafe=random_cafe.to_dict())

@app.route('/all')
def get_all():
    cafes = db.session.query(Cafe).all()
    all_cafes = [cafe.to_dict() for cafe in cafes]
    return jsonify(all_cafes)


@app.route('/search')
def get_all_cafe_at_location():
    query_location = request.args.get('loc')
    cafe = Cafe.query.filter_by(location = query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={'Not Found':"Sorry we don't have a cafe at that location"})



## HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add():
    new_cafe = Cafe(
        name = request.form.get('name'),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get('loc'),
        seats = request.form.get('seats'),
        has_toilet = bool(request.form.get('toilets')),
        has_wifi = bool(request.form.get('wifi')),
        has_sockets = bool(request.form.get('sockets')),
        can_take_calls = bool(request.form.get('calls')),
        coffee_price = request.form.get('coffee_price')
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response = {"success":"Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafeid>', methods=['PATCH'])
def update_price(cafeid):
    new_price = request.args.get('new_price')
    cafe = Cafe.query.get(cafeid)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success":"Successfully updated the price."})
    else:
        return jsonify(error = {"Not Found":"Sorry a cafe with that id was not found in the database."})



## HTTP DELETE - Delete Record
@app.route('/report-closed/<int:cafeid>',methods = ["DELETE"])
def delete(cafeid):
    api_key = request.args.get('api-key')
    if api_key:     
        cafe = Cafe.query.get(cafeid)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response = {"success":"Successfully deleted cafe from the database."}), 200

        else:
            return jsonify(error = {"Not Found":"Sorry a cafe with that id was not found in the database."}), 404
    
    else:
        return jsonify(error = {'Forbidden':'Sorry that\'s not allowed.Make sure you have the correct api_key.'}), 403
        


if __name__ == '__main__':
    app.run(debug=True)



# If you use the Postman then you can perform and verify these actions there easily.
# Also you can easily generate the documentation for our api using Postman.