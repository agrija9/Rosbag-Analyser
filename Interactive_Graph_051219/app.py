from flask import Flask, render_template
from flask import request, redirect
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
import rosbag
import time
import glob
import rospy
import pandas as pd
import numpy
import random
import os

app = Flask(__name__)

@app.route('/convert_time')
def convert_time(tm, nsec):
    return time.strftime("%d %m %Y %H:%M:%S ", time.localtime(tm)) + str(nsec)

@app.route('/read_message')
def read_message(msg):
    headers = msg.__slots__
    for i in headers:
        print(i + ' : ' + str(getattr(msg, i)))

@app.route('/bag_content')
def bag_content(bag, df):
    df1 = pd.DataFrame(columns = ['Time', 'Topic', 'Message', 'Color'])
    for Topic, Msg, T in bag.read_messages(topics = bag.get_type_and_topic_info()[1].keys()):
        Time = convert_time(T.secs, T.nsecs)
        # if Topic ==  '/cmd_vel':
        try:
            data = Msg.data
            if type(data) == str and data != "" and len(data) < 50:
                df1 = df1.append({'Time' : Time, 'Topic' : Topic, 'Message' : Msg.data, 'Color' : df.loc[Topic].Color} , ignore_index=True)
        except:
            None
    
    df1 = df1.append({'Time' : '17 10 2019 19:37:19 190000000 17 10 2019 19:37:30 340000000', 'Topic' : '/cmd_vel', 'Message' : 'Something', 'Color' : 'color_(100,225,18)'} , ignore_index=True)

    jsonfile =  df1.to_json(orient='records')
    df1.to_csv('Rosbag_Content.csv', index=True)
    return jsonfile

@app.route('/bag_info')
def bag_info(bag):
    Start_Time = convert_time(bag.get_start_time(), (bag.get_start_time() - int(bag.get_start_time()))*10**9)
    End_Time = convert_time(bag.get_end_time(), (bag.get_end_time() - int(bag.get_end_time()))*10**9)
    Messages = bag.get_type_and_topic_info()[0].keys()
    Topics = bag.get_type_and_topic_info()[1].keys()
    msgs = [bag.get_type_and_topic_info()[1].get(i) for i in bag.get_type_and_topic_info()[1].keys()]
    df1 = pd.DataFrame(columns = ['Topic', 'Color', 'Message', 'Count', 'Connections', 'Frequency'])

    colors = color_gen(len(Topics))
    random.shuffle(colors)
    random.shuffle(colors)
    random.shuffle(colors)
    for idx, j in enumerate(Topics):
        df1 = df1.append({'Topic' : j, 'Color': colors[idx],'Message' : msgs[idx].msg_type, 'Count' : msgs[idx].message_count, 'Connections' : msgs[idx].connections, 'Frequency' : msgs[idx].frequency}, ignore_index=True)

    df1 = df1.set_index('Topic')
    df1.to_csv('Rosbag_Info.csv', index=True)
    return df1

@app.route('/color_gen')
def color_gen(n):
    ret = []
    r = int(random.uniform(0,1) * 256)
    g = int(random.uniform(0,1) * 256)
    b = int(random.uniform(0,1) * 256)
    step = 256 / n
    while len(ret) < n:
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        ret.append('color_' + str((r,g,b)))
        ret = list(dict.fromkeys(ret))
    return ret

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        bag = rosbag.Bag(f.filename)
        df = bag_info(bag)
        jsonfile = bag_content(bag, df)
        os.remove(f.filename)
        return render_template('SDP_visualize.html',  jsonfile=jsonfile)

if __name__ == '__main__':
    app.run(debug=True)