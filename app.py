from flask import Flask, render_template
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

# # setup mongo connection
 conn = "mongodb://localhost:27017"
 client = pymongo.MongoClient(conn)

# # connect to mongo db and collection
# db = client.store_inventory
# produce = db.produce


@app.route("/scrape")
def scrape():
    results = scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({},results, upsert=True)

    # Redirect back to home page
    return redirect("/")

    # TO DO: Save to Mongo DB
    return {}


@app.route("/")
def index():
    return {}
    # # write a statement that finds all the items in the db and sets it to a variable
    # inventory = list(produce.find())
    # print(inventory)

    # # render an index.html template and pass it the data you retrieved from the database
    # return render_template("index.html", inventory=inventory)


if __name__ == "__main__":
    app.run(debug=True)


