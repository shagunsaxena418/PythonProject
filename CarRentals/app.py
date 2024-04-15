# import necessary modules
import random
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient


# define the mongodb client
client = MongoClient(port=27017)
# define the database to use
db = client.car_rental_data
collection = db['carRentalData']
usercollection=db['userRegistration']

# define the flask app
app = Flask(__name__)

# define the home page route
@app.route('/')
def Home():
    return render_template("index.html")

# define the About page route
@app.route('/about')
def About():
    return render_template("about.html")

# define the register page route
@app.route('/register')
def Register():
    return render_template("register.html")

# define the login page route
@app.route('/login')
def Login():
    return render_template("login.html")

# define the user register route
@app.route('/userregister', methods=["GET", "POST"])
def UserRegistration():
    data = {}
    users = list(usercollection.find())
    user_data = 1
    #Check whether the username already exists
    for user in users:
        if(user["email"] ==request.form['email'] ):
            user_data=0
            break
    
    if(user_data==1):
        if request.method == "POST":
            data['email'] = request.form['email']
            data['Passname'] = request.form['Passname']
            data['Active']=1
            db.userRegistration.insert_one(data)
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

# define the Booking page route
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
        data['Active']=1
        db.carRentalData.insert_one(data)
    return render_template("home.html")

# define the car data get page route
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

#function to create random numbers
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
        data['Sold']=1
        db.bookings.insert_one(data)
        return jsonify({"ref": data['reference_number']})
        

@app.route('/check_user_existence', methods=['GET','POST'])
def verify_user_existence():
    users = list(usercollection.find())
    user_data = 0
    for user in users:
        if(user["email"] == request.form['email']):
            user_data=1
            break
    if(user_data ==1):
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=False)
