import rosbag
import time
import glob
import rospy
import pandas as pd
import numpy

bag_names = glob.glob("bagfiles/*.bag")

def convert_time(tm, nsec):
    return time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime(tm)) + str(nsec)

def read_message(msg):
    headers = msg.__slots__
    for i in headers:
        print(i + ' : ' + str(getattr(msg, i)))

def bag_info(bag):
    Start_Time = convert_time(bag.get_start_time())
    End_Time = convert_time(bag.get_end_time())
    Messages = bag.get_type_and_topic_info()[0].keys()
    Topics = bag.get_type_and_topic_info()[1].keys()
    msgs = [bag.get_type_and_topic_info()[1].get(i) for i in bag.get_type_and_topic_info()[1].keys()]
    print('Start Time : ' + str(Start_Time))
    print('End Time : ' + str(End_Time))
    print('Messages : ' + str(Messages))
    print('Topics : ' + str(Topics))
    print('--------------------------------------------------------------------')
    print('Topics and Messages :')

    df = pd.DataFrame(columns=Topics)
    data = dict()
    data[' '] = ['Message', 'Count', 'Connections', 'Frequency']
    for idx, j in enumerate(Topics):
        print('\n')
        print('Topic : ' + str(j))
        print('Message : ' + str(msgs[idx].msg_type))
        print('Count : ' + str(msgs[idx].message_count))
        print('Connections : ' + str(msgs[idx].connections))
        print('Frequency : ' + str(round(msgs[idx].frequency, 1)) + ' Hz')
        data[j] = [msgs[idx].msg_type, msgs[idx].message_count, msgs[idx].connections, round(msgs[idx].frequency, 1)]
        
    df1 = pd.DataFrame(data)
    df = df.append(df1, ignore_index = True) 
    df.to_csv('Rosbag_info.csv', index=True)

def bag_content(bag):
    df1 = pd.DataFrame(columns = ['Time', 'Topic'])

    for Topic, Msg, T in bag.read_messages(topics = bag.get_type_and_topic_info()[1].keys()):
        Time = convert_time(T.secs, T.nsecs)
        df1 = df1.append({'Topic' : Topic , 'Time' : Time} , ignore_index=True)

    df1 = df1.set_index('Time')
    df1.to_csv('Rosbag_Content.csv', index=True)
    print(df1)


bag = rosbag.Bag(bag_names[0])

print('--------------------------------------------------------------------')
# bag_info(bag)
bag_content(bag)
print('--------------------------------------------------------------------')

bag.close()