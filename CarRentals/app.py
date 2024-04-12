# import necessary modules
import random
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient

# define the mongodb client
client = MongoClient(port=27017)
# define the database to use
db = client.car_rental_data
collection = db['carRentalData']

# define the flask app
app = Flask(__name__)


# define the home page route
@app.route('/')
def Home():
    return render_template("index.html")

# define the home page route
@app.route('/cars')
def Cars():
    cars_data = []
    cars = list(collection.find())
    for car in cars:
        cars_data.append({
            "Brand": car["Brand"],
            "Model": car["Model"],
            "Year": car["Year"],
            "Color": car["Color"],
            "Type": car["Type"],
            "Fuel": car["Fuel"],
            "Transmission": car["Transmission"],
            "Price": car["Price"]
        })
        
    return render_template("cars.html", cars=cars_data)

# define the registration page route
@app.route('/home')
def Registration():
    return render_template("home.html")

# define the registration page route
@app.route('/booking')
def Bookings():
    return render_template("booking.html")

# route to get data from html form and insert data into database
@app.route('/data', methods=["GET", "POST"])
def data():
    data = {}
    if request.method == "POST":
        data['Brand'] = request.form['brand']
        data['Model'] = request.form['model']
        data['Year'] = request.form['year']
        data['Color'] = request.form['color']
        data['Type'] = request.form['type']
        data['Fuel'] = request.form['fuel']
        data['Transmission'] = request.form['transmission']
        data['Price'] = request.form['price']
        db.carRentalData.insert_one(data)

    return render_template("home.html")

@app.route('/cars_data', methods=["GET"])
def cars_data():
    cars = list(collection.find())
    car_data = []
    for car in cars:
        car_data.append({
            "Brand": car["Brand"],
            "Model": car["Model"],
            "Year": car["Year"],
            "Color": car["Color"],
            "Type": car["Type"],
            "Fuel": car["Fuel"],
            "Transmission": car["Transmission"],
            "Price": car["Price"]
        })
    return jsonify(car_data)

def generate_reference_number():
    reference_number = ''
    for i in range(8):
        reference_number += str(random.randint(0, 9))
    return reference_number

@app.route('/bookings', methods=["GET","POST"])
def booking_dat():
    data = {}
    if request.method == "POST":
        data['reference_number'] = generate_reference_number()
        data['firstName'] = request.form['firstName']
        data['lastName'] = request.form['lastName']
        data['mobileNumber'] = request.form['mobileNumber']
        data['pickupLocation'] = request.form['pickupLocation']
        data['dropLocation'] = request.form['dropLocation']
        db.bookings.insert_one(data)

if __name__ == '__main__':
    app.run(debug=False)



