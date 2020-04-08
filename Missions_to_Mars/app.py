from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

mars_table = db.mars_table

# connect to mongo db and collection


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    inventory = list(mars_table.find())
    print(inventory)

    # Find one record of data from the mongo database
    # mars = mars_table.find_one()

    mars = list(mars_table.find())

    # Return template and data
    return render_template("index.html", record=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    data = scrape_mars.scrape_info()
    
    db.mars_table.drop()
    # Update the Mongo database using update and upsert=True
    db.mars_table.insert(data)



    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
