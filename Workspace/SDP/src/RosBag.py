import rosbag
import time
import glob
import rospy

bag_names = glob.glob("bagfiles/*.bag")

def convert_time(tm):
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(tm))

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
    for idx, j in enumerate(Topics):
        print('\n')
        print('Topic : ' + str(j))
        print('Message : ' + str(msgs[idx].msg_type))
        print('Count : ' + str(msgs[idx].message_count))
        print('Connections : ' + str(msgs[idx].connections))
        print('Frequency : ' + str(round(msgs[idx].frequency, 1)) + ' Hz')

bag = rosbag.Bag(bag_names[0])

# print(bag)

print('--------------------------------------------------------------------')
bag_info(bag)
print('--------------------------------------------------------------------')

# for topic, msg, t in bag.read_messages(topics = []):
#     print(topic)
#     print(convert_time(t.secs))
#     read_message(msg)
#     break

bag.close()