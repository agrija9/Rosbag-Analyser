import rospy
import numpy as np
from std_msgs.msg import String
import threading
import time
import rosgraph
import socket
from datetime import datetime
from flask import Flask, render_template
from flask import request, redirect
from gevent.pywsgi import WSGIServer
from werkzeug import secure_filename
import os

def callback(data, args):
    print('Time : ' + args[1] + ', Topic : ' + args[0] + ', Data : ' + data.data)
    return ('Time : ' + args[1] + ', Topic : ' + args[0] + ', Data : ' + data.data)

def listener(strlist):
    rospy.init_node('listener', anonymous=True)

    for i in strlist:
        rospy.Subscriber(i, String, callback, (i, datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")))

    rospy.spin()

def check_master(check):
    while check == False:
        try:
            rosgraph.Master('/rostopic').getPid()
        except socket.error:
            check = True
            rospy.signal_shutdown('exit')

if __name__ == '__main__':

    x = threading.Thread(target=check_master, args=(False,))
    x.start()

    lists = rospy.get_published_topics()

    strlist = []
    for i in lists:
        if i[1] == 'std_msgs/String':
            strlist.append(i[0])
    
    listener(strlist)