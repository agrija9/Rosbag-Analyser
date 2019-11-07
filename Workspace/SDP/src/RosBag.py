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
    Start_Time = convert_time(bag.get_start_time(), (bag.get_start_time() - int(bag.get_start_time()))*10**9)
    End_Time = convert_time(bag.get_end_time(), (bag.get_end_time() - int(bag.get_end_time()))*10**9)
    Messages = bag.get_type_and_topic_info()[0].keys()
    Topics = bag.get_type_and_topic_info()[1].keys()
    msgs = [bag.get_type_and_topic_info()[1].get(i) for i in bag.get_type_and_topic_info()[1].keys()]
    print('Start Time : ' + str(Start_Time))
    print('End Time : ' + str(End_Time))
    print('Messages : ' + str(Messages))
    print('Topics : ' + str(Topics))
    print('--------------------------------------------------------------------')
    print('Topics and Messages :')
    df1 = pd.DataFrame(columns = ['Topic', 'Message', 'Count', 'Connections', 'Frequency'])


    for idx, j in enumerate(Topics):
        print('\n')
        print('Topic : ' + str(j))
        print('Message : ' + str(msgs[idx].msg_type))
        print('Count : ' + str(msgs[idx].message_count))
        print('Connections : ' + str(msgs[idx].connections))
        print('Frequency : ' + str(msgs[idx].frequency) + ' Hz')
        df1 = df1.append({'Topic' : j, 'Message' : msgs[idx].msg_type, 'Count' : msgs[idx].message_count, 'Connections' : msgs[idx].connections, 'Frequency' : msgs[idx].frequency}, ignore_index=True)

    df1 = df1.set_index('Topic')
    df1.to_csv('Rosbag_Info.csv', index=True)

def bag_content(bag):
    df1 = pd.DataFrame(columns = ['Time', 'Topic', 'Message'])

    for Topic, Msg, T in bag.read_messages(topics = bag.get_type_and_topic_info()[1].keys()):
        Time = convert_time(T.secs, T.nsecs)
        # print(Msg)
        try:
            df1 = df1.append({'Topic' : Topic , 'Time' : Time, 'Message' : Msg.msg} , ignore_index=True)
        except:
            df1 = df1.append({'Topic' : Topic , 'Time' : Time, 'Message' : None} , ignore_index=True)

    df1 = df1.set_index('Time')
    df1.to_csv('Rosbag_Content.csv', index=True)


bag = rosbag.Bag(bag_names[2])
print('--------------------------------------------------------------------')
# bag_info(bag)
bag_content(bag)
print('--------------------------------------------------------------------')

bag.close()