import rosbag
import time
import glob
import rospy
import pandas as pd
import numpy
import random

colors = ['aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black','blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan','darkgoldenrod','darkgray','darkgrey','darkgreen','darkkhaki','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen','darkslateblue','darkslategray','darkslategrey','darkturquoise','darkviolet','deeppink','deepskyblue','dimgray','dimgrey','dodgerblue','firebrick','floralwhite','forestgreen','fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray','grey','green','greenyellow','honeydew','hotpink','indianred','indigo','ivory','khaki','lavender','lavenderblush','lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan','lightgoldenrodyellow','lightgray','lightgrey','lightgreen','lightpink','lightsalmon','lightseagreen','lightskyblue','lightslategray','lightslategrey','lightsteelblue','lightyellow','lime','limegreen','linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid','mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise','mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite','navy','oldlace','olive','olivedrab','orange','orangered','orchid','palegoldenrod','palegreen','paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum','powderblue','purple','rebeccapurple','red','rosybrown','royalblue','saddlebrown','salmon','sandybrown','seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','slategrey','snow','springgreen','steelblue','tan','teal','thistle','tomato','turquoise','violet','wheat','white','whitesmoke','yellow','yellowgreen'] 
random.shuffle(colors)
bag_names = glob.glob("bagfiles/*.bag")

def convert_time(tm, nsec):
    return time.strftime("%a, %d %b %Y %H:%M:%S ", time.localtime(tm)) + str(nsec)

def read_message(msg):
    headers = msg.__slots__
    for i in headers:
        print(i + ' : ' + str(getattr(msg, i)))

def bag_info(bag, colors):
    Start_Time = convert_time(bag.get_start_time(), (bag.get_start_time() - int(bag.get_start_time()))*10**9)
    End_Time = convert_time(bag.get_end_time(), (bag.get_end_time() - int(bag.get_end_time()))*10**9)
    Messages = bag.get_type_and_topic_info()[0].keys()
    Topics = bag.get_type_and_topic_info()[1].keys()
    msgs = [bag.get_type_and_topic_info()[1].get(i) for i in bag.get_type_and_topic_info()[1].keys()]
    
    print('Start Time : ' + str(Start_Time))
    print('End Time : ' + str(End_Time))
    print('Messages : ' + str(Messages))
    print('Topics : ' + str(Topics))
    # print('--------------------------------------------------------------------')
    # print('Topics and Messages :')
    df1 = pd.DataFrame(columns = ['Topic', 'Color', 'Message', 'Count', 'Connections', 'Frequency'])

    for idx, j in enumerate(Topics):
        # print('\n')
        # print('Topic : ' + str(j))
        # print('Message : ' + str(msgs[idx].msg_type))
        # print('Count : ' + str(msgs[idx].message_count))
        # print('Connections : ' + str(msgs[idx].connections))
        # print('Frequency : ' + str(msgs[idx].frequency) + ' Hz')
        df1 = df1.append({'Topic' : j, 'Color' : colors[idx], 'Message' : msgs[idx].msg_type, 'Count' : msgs[idx].message_count, 'Connections' : msgs[idx].connections, 'Frequency' : msgs[idx].frequency}, ignore_index=True)

    df1 = df1.set_index('Topic')
    df1.to_csv('Rosbag_Info.csv', index=True)
    return df1

def bag_content(bag, df):

    df1 = pd.DataFrame(columns = ['Time', 'Topic', 'Message', 'Color'])
    for Topic, Msg, T in bag.read_messages(topics = bag.get_type_and_topic_info()[1].keys()):
        Time = convert_time(T.secs, T.nsecs)
        try:
            data = Msg.data
            if type(data) == str:
                df1 = df1.append({'Topic' : Topic , 'Time' : Time, 'Message' : Msg.data, 'Color' : df.loc[Topic].Color} , ignore_index=True)
        except:
            None

    df1 = df1.set_index('Time')
    df1.to_csv('Rosbag_Content.csv', index=True)

bag = rosbag.Bag(bag_names[2])
print('--------------------------------------------------------------------')
df = bag_info(bag, colors)
bag_content(bag, df)
print('--------------------------------------------------------------------')

bag.close()