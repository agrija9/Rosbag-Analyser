from flask import Flask, render_template
from flask import request, redirect
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
import rosbag
import os
from utils import bag_content, bag_info


myapp = Flask(__name__)

@myapp.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

@myapp.route("/team", methods=["GET", "POST"])
def team():
    return render_template('team.html')

@myapp.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        bag = rosbag.Bag(f.filename)
        df = bag_info(bag)
        jsonfile = bag_content(bag, df)
        os.remove(f.filename)
        return render_template("SDP_visualize.html",  jsonfile=jsonfile)
    
    elif request.method == "GET":
        return render_template("index.html")

@myapp.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "POST":
        return render_template("about.html")
    
    elif request.method == "GET":
        return render_template("index.html")
    

if __name__ == '__main__':
    myapp.run(debug=True)