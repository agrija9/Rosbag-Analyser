
import rosbag
import time

def convert_time(tm):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(tm))

bag = rosbag.Bag('bagfiles/2019-10-24-13-52-05.bag')

print bag

for topic, msg, t in bag.read_messages(topics=['/turtle1/pose']):
    print topic
    print convert_time(t.secs)
    print msg

bag.close()