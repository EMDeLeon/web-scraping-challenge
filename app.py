from flask import Flask, render_template
import pymongo
from scrape_mars import scrape_all

app = Flask(__name__)

# # setup mongo connection
conn="mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# # connect to mongo db and collection
db = client.missiontomars
mars = db.mars


@app.route("/scrape")
def scrape_all():
    results = scrape_mars.scrape_all()

    # Update the Mongo database using update and upsert=True
    client.db.collection.update({},results, upsert=True)

    # Redirect back to home page
    return redirect("/")

    # TO DO: Save to Mongo DB
    return {}


@app.route("/")
def index():
        ##render an index.html template and pass it the data you retrieved from the database
    mars=client.db.missiontomars.find_one()  #takes the last item in the table to return
    return render_template("index.html", mars=mars)


if __name__ == "__main__":
    app.run(debug=True)


