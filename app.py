#Import Mongo & python scraping file
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

#Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Set up homepage & link our visual representation of our work, our web app, to the code that powers it
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#Set up scrape page - scrape new data with scraping.py, update database & return success message
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()