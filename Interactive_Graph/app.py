from flask import Flask, render_template
from flask import request, redirect
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
import rosbag
import os
import sys
from utils import bag_content, bag_info, color_gen, convert_time
import rospy
import numpy as np
import pandas as pd
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import threading
import time
import rosgraph
import socket
from flask_socketio import SocketIO, send
from datetime import datetime
import random

myapp = Flask(__name__)
socketio = SocketIO(myapp)

count = 1
check = False
df1 = pd.DataFrame(columns = ['Time', 'Topic', 'Message', 'Color'])
df2 = pd.DataFrame(columns = ['Topic', 'Color'])

def resets():
    time.sleep(0.5)
    python = sys.executable
    os.execl(python, python, * sys.argv)

@myapp.route("/", methods=["GET", "POST"])
def index():
    z = threading.Thread(target=resets, args=())
    z.start()
    return render_template('index.html')

@myapp.route("/team", methods=["GET", "POST"])
def team():
    return render_template('team.html')

@myapp.route("/live", methods=["GET", "POST"])
def live():
    x = threading.Thread(target=check_master, args=())
    x.start()
    return render_template('live_visualize.html')

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

def roslaunch():
    # os.system("rosrun turtlesim turtlesim_node")
    os.system("rosbag play move_base_WS02_to_WS03.bag")

@socketio.on('message')
def handleMessage(msg):
    global count
    global df2
    if check == False:
        if count == 1:
            s = threading.Thread(target=roslaunch, args=())
            s.start()
            time.sleep(0.5)
            count = 2
            lists = rospy.get_published_topics()
            strlist = []
            for i in lists:
                if i[1] == 'std_msgs/String':
                    strlist.append(i[0])
            
            colors = color_gen(len(strlist))
            random.shuffle(colors)
            for idx, j in enumerate(strlist):
                df2 = df2.append({'Topic' : j, 'Color': colors[idx]}, ignore_index=True)

            df2 = df2.set_index('Topic')
            y = threading.Thread(target=listener, args=(strlist,))
            y.start()
    else:
        print("Roscore is not running. Start roscore and try again")   
    jsonfile =  df1.to_json(orient='records')
    send(jsonfile, broadcast=True)

def callback(data, args):
    global df1
    T = rospy.Time.from_sec(time.time()).to_sec()
    Tn = int(str(T - int(T))[2:9])
    df1 = df1.append({'Time' : convert_time(T,Tn), 'Topic' : args[0], 'Message' : data.data, 'Color' : df2.loc[args[0]].Color} , ignore_index=True)

def listener(strlist):
    rospy.init_node('listener', anonymous=True, disable_signals=True)
    for i in strlist:
        rospy.Subscriber(i, String, callback, (i, datetime.now().strftime("%d %m %Y %H:%M:%S %f")))
    rospy.spin()

def check_master():
    global check
    while check == False:
        try:
            rosgraph.Master('/rostopic').getPid()
        except socket.error:
            check = True
            rospy.signal_shutdown('exit')

if __name__ == '__main__':
    # myapp.run(debug=True)
    socketio.run(myapp)