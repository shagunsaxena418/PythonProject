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

value=0
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
    if value==0:
        suc=""
    else:
        suc="data inserted"
    return render_template("home.html",message=suc)

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
        value=1
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

@app.route('/book', methods=["GET","POST"])
def booking_dat():
    data = {}
    if request.method == "POST":
               
        data['reference_number'] =  generate_reference_number()
        data['firstName'] = request.form['firstname']
        data['lastName'] = request.form['lastname']
        data['email'] = request.form['email']
        data['mobileNumber'] = request.form['mobile']
        data['pickupLocation'] = request.form['Pickup']
        data['dropLocation'] = request.form['dropLocation']
        data['pickupDate']=request.form['pickupdate']
        data['dropOffDate']=request.form['returndate']
        db.bookings.insert_one(data)
        return "good "
        return render_template("home.html")
    
@app.route('/save-data', methods=['POST'])
def save_data():
    try:
        # Retrieve form data from the request
        data = request.form.to_dict()

        # Here you can process and save the form data as needed
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
            value =1

        # Assuming the data was successfully saved, return a success response
        return jsonify({"success": True}), 200
    except Exception as e:
        # If an error occurred during data saving, return an error response
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)



