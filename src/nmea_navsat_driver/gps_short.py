#!/usr/bin/python3
import serial
import datetime
import rospy,numpy
from math import *
from geometry_msgs.msg import Pose
serial_port = rospy.get_param('~port', '/dev/ttyUSB0')
serial_baud = rospy.get_param('~baud', 9600)
ser = serial.Serial(port=serial_port, baudrate=serial_baud, timeout=1)
lonB = 0
latB = 0
latitude = "nan"
longitude = "nan"
i = 0
oldlat = 0
oldlon = 0
while True:
    gpsdata = ser.readline()
    try:
        gpsdata = gpsdata.decode("utf8")
        try:
            gpsdata = gpsdata.split(',')
            
            if "GNRMC" in gpsdata[0]:
                hrs, min, sec = gpsdata[1][0:2], gpsdata[1][2:4], gpsdata[1][4:6]
                day, month, year = gpsdata[9][0:2], gpsdata[9][2:4], gpsdata[9][4:6]
                datetimeutc = "{}:{}:{} {}/{}/{}".format(
                    hrs, min, sec, day, month, year)
                datetimeutc = datetime.datetime.strptime(
                    datetimeutc, '%H:%M:%S %d/%m/%y')
                speed = round(float(gpsdata[7])*1.852, 2)
                message = "Datetime={} ,speed={} kmph".format(
                    datetimeutc, speed)
                print(message)
            if "GNGGA" in gpsdata[0]:
                lat = float(gpsdata[2])/100
                lon = float(gpsdata[4])/100
                alt = gpsdata[9]
                satcount = gpsdata[7]
                message = "Altitude={}, Satellites={}\n".format(alt, satcount)
            if lat == 0:
                  print("GPS not connected with satellite")
                  lat1 = oldlat
                  lon1 = oldlon
            else:
             lat1 = lat
             lon1 = lon
             if i<1:
                print("Enter the Goal Location GPS coordinates")
                latB = float(input("Enter Latitude:"))
                lonB = float(input("Enter Longitude:"))
                i = i+ 1
             distance_pub = rospy.Publisher('/distance', Pose, queue_size=50)

            # rospy.Subscriber('/fix', NavSatFix, get_xy_based_on_lat_long, distance_pub)
             lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lonB, latB])
             dlon = lon2 - lon1
             dlat = lat2 - lat1
             x = cos(lat2) * sin(dlon)
             y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
             a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
             brng = numpy.arctan2(x, y)
             brng = numpy.degrees(brng)
             c = 2 * atan2(sqrt(a), sqrt(1-a))
             Base = 6371 * c
             pose = Pose()
             pose.position.x = Base*1000
             pose.position.y = lat
             pose.position.z = lon
             pose.orientation.x = 0
             pose.orientation.y = brng
             distance_pub.publish(pose)
             rospy.loginfo(pose)
             print("\n")
             oldlon = lon
             oldlat = lat
        except:
            print("unable to process", gpsdata)
            ser.close()
    except:
        print("unable to decode", gpsdata)