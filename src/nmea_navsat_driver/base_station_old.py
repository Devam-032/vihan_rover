#!/usr/bin/env python3
from glob import glob
import rospy,numpy
from math import *
from geometry_msgs.msg import Pose
print("lat = 21.16694")
print("long = 72.78565")
latB=21.166997
lonB=72.785755
#latB = float(input("Enter Latitude:"))
#lonB = float(input("Enter Longitude:"))
def callback(msg):
    global lonB,latB
    pub = rospy.Publisher('/base_station_node', Pose,queue_size = 10)
    lat1 = msg.position.y 
    lon1 = msg.position.z
    lon1, lat1, lon2, lat2 = map(radians, [lonB,latB, lon1, lat1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    x = cos(lat2) * sin(dlon)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    brng = numpy.arctan2(x, y)
    brng = numpy.degrees(brng)
    base = Pose()
    base.position.x = msg.position.y
    base.position.y = msg.position.z
    base.orientation.z = latB
    base.orientation.w= lonB
    base.orientation.y = -brng
    pub.publish(base)

def listener():
  rospy.init_node('listener', anonymous=True)
  rospy.Subscriber('/distance', Pose, callback)
  rospy.spin()

listener()
