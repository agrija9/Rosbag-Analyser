import time
import glob
import rospy
import pandas as pd
import numpy
import random

def convert_time(tm, nsec):
    return time.strftime("%d %m %Y %H:%M:%S ", time.localtime(tm)) + str(nsec)

def read_message(msg):
    headers = msg.__slots__
    for i in headers:
        print(i + ' : ' + str(getattr(msg, i)))

def bag_content(bag, df):
    df1 = pd.DataFrame(columns = ['Time', 'Topic', 'Message', 'Color'])
    for Topic, Msg, T in bag.read_messages(topics = bag.get_type_and_topic_info()[1].keys()):
        Time = convert_time(T.secs, T.nsecs)
        try:
            data = Msg.data
            if type(data) == str and (data == 'e_start' or data == 'e_stop' or data == 'e_stopped' or data == 'e_success'):
                df1 = df1.append({'Time' : Time, 'Topic' : Topic, 'Message' : Msg.data, 'Color' : df.loc[Topic].Color} , ignore_index=True)
        except:
            None

    jsonfile =  df1.to_json(orient='records')
    return jsonfile

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
    return df1

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