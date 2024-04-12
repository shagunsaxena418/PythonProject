from pymongo import MongoClient

def seed_database():
    client = MongoClient('localhost', 27017)  # Connect to MongoDB server
    db = client.calculatorDB  # Create a database named 'calculatorDB'
    db.calculations.drop()  # Drop the collection if it already exists
    db.create_collection('calculations')  # Create a new collection named 'calculations'
    print("Database and collection created successfully.")

if __name__ == '__main__':
    seed_database()