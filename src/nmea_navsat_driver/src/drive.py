#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Pose

def callback1(data):
    rospy.loginfo("x = %f, y = %f, z = %f \n", data.position.x, data.orientation.y)

try:
    rospy.init_node('drive_commander', anonymous=True)
    while not rospy.is_shutdown():
        rospy.Subscriber("/distance", Pose, callback1)
                

except rospy.ROSInterruptException:
     pass
