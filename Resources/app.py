import scraping
from flask import Flask, redirect, render_template, url_for
from flask_pymongo import PyMongo
print("imports imported")
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
inde_x = "index.html"
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template(inde_x, mars=mars)
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()
