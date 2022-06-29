from ctypes.wintypes import DWORD
from datetime import datetime
from this import d
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

# app.config["MONGO_URI"] = "mongodb://mongo:27017/customer"
# mongo = PyMongo(app)
# feedback_coll = mongo.db.customer

# app.config['MONGO_URI'] = 'mongodb://admin:admin@mongo-mongodb-0.mongo-mongodb-headless.default.svc.cluster.local:27017'
# mongo = PyMongo(app)
# feedback_coll = mongo.customer.customer

client = MongoClient('mongo', 27017, username='admin', password='admin', connect=False)
data = client["customer"]
feedback_coll = data["customer"]


@app.route("/")
def form():
   return render_template('form.html')


@app.route("/read")
def read_data():
    customer = (feedback_coll.find({}))
    return render_template('index.html', customer=customer)


@app.route("/data", methods=['GET'])
def show_data():
    if request.method == 'GET':
        name = request.args.get("x")
        phone = request.args.get("y")
        feed = request.args.get("z")
    if name != "" and phone != "" and feed != "":
        var = {"name": name, "phone": phone, "feedback": feed}
        feedback_coll.insert_one(var)
        return render_template('retind.html')
    else:
        return ("Kindly fill the form")


@app.route("/delete")
def delete():
    return render_template('delone.html')


@app.route("/delete_one")
def del_one():
    destroy = request.args.get("d")
    to = "'"
    to_destroy = str(to+destroy+to)
    feedback_coll.delete_one({"name": str(to_destroy)})
    return ("Deleted")


@app.route("/delete_all")
def delete_all():
    feedback_coll.delete_many({})
    return "All data deleted"


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8000)