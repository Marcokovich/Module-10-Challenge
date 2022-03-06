import scraping
from flask import Flask, redirect, render_template, url_for
from flask_pymongo import PyMongo
print("imports imported")
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
inde_x = "index.html"
#print("mars")
#print(mongo.db.mars.find_one())
#print("mars")
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   print('printing mars')
   print(type(mars))
   print('mars printed')
   print(index)
   return render_template(inde_x, mars=mars)

print('post 1')
@app.route("/scrape")
def scrape():
   print('post 2')
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   print('testing')
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()