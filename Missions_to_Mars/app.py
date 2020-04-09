from flask import Flask, render_template, redirect
import pymongo
import scrape_mars
import pandas as pd

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client["mars_db"]
mars_table = db["mars_table"]

db.mars_table.drop()

data = scrape_mars.scrape_info()
db.mars_table.insert_one(data)
print ("Hi")
print (type(data))


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars = list(mars_table.find())

    print ("Hi")
    print(mars)


    # Return template and data
    return render_template("index.html", record=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    data = scrape_mars.scrape_info()
    
    db.mars_table.drop()
    # Update the Mongo database using update and upsert=True
    db.mars_table.insert_one(data)



    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


