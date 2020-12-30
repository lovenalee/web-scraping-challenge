from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

print('........')
print('mongo',mongo)
print('mongo.db',mongo.db)
print('mongo.db.mars', mongo.db.mars_app)

# Route to render index.html template using data from Mongo
@app.route("/")
def main():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)


@app.route("/scrape")
def scrape():
  
    mars_scrape = scrape_mars.scrape_info()
    print(mars_scrape)
    mongo.db.collection.update({}, mars_scrape, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
