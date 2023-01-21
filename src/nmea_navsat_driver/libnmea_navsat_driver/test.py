#!/usr/bin/python3
import serial
import datetime
import rospy,numpy
from math import *
from geometry_msgs.msg import Pose
from sensor_msgs.msg import NavSatFix, NavSatStatus, TimeReference
rover_cord = NavSatFix()
lonB = 0
latB = 0
latitude = "nan"
longitude = "nan"
i = 0
oldlat = 0
oldlon = 0
distance_pub = rospy.Publisher('/distance', Pose, queue_size=50)
pub = rospy.Publisher('rover/fix',NavSatFix,queue_size=1)
print("Enter the Goal Location GPS coordinates")
latB = float(input("Enter Latitude:"))
lonB = float(input("Enter Longitude:"))
def dec2deg(value):
   dec = value/100.00
   deg = int(dec)
   min = (dec - int(dec))/0.6
   position = deg + min
   position = "%.7f" %(position)
   return position

rospy.init_node('gps_pub', anonymous=True)
mapscale = 18
while not rospy.is_shutdown():
    port="/dev/ttyUSB0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    gpsdata=ser.readline()
    try:
    #print(gpsdata)
        gpsdata = gpsdata.decode("utf8")
        try:
      #print(gpsdata)
            gpsdata = gpsdata.split(',')
            if "GNRMC" in gpsdata[0]:
                hrs, min, sec = gpsdata[1][0:2], gpsdata[1][2:4], gpsdata[1][4:6]
                day, month, year = gpsdata[9][0:2], gpsdata[9][2:4], gpsdata[9][4:6]
                datetimeutc = "{}:{}:{} {}/{}/{}".format(hrs, min, sec, day, month, year)
                datetimeutc = datetime.datetime.strptime(datetimeutc, '%H:%M:%S %d/%m/%y')
                speed = round(float(gpsdata[7])*1.852,2)
                message = "Datetime={} ,speed={} kmph".format(datetimeutc, speed)
                print(message)
            if "GNGGA" in gpsdata[0]:
            #print(gpsdata)
                lat = float(gpsdata[2])
                a=int(lat*100)
                lat = float(a%100)/3600+float(a%10000-a%100)/6000+float(a%1000000-a%10000)/10000
                lon = float(gpsdata[4])
                d=int(lon*100)
                lon=float(d%100)/3600+float(d%10000-d%100)/6000+float(d%1000000-d%10000)/10000
                alt = gpsdata[9]
                satcount = gpsdata[7]
                message = "Altitude={}, Satellites={}\n".format(alt, satcount)
                # gearth = "https://earth.google.com/web/search/@{},{},{}\n".format(lat,lon,alt)
                # mapsapp = "geo:{},{}\n".format(lat, lon)
                # map = "https://www.openstreetmap.org/#map={}/{}/{}\n\n".format(mapscale, lat, lon)
                #print(message, gearth, mapsapp, map)
                print(message, lat, lon)
            if lat == 0:
                print("GPS not connected with satellite")
                lat1 = oldlat
                lon1 = oldlon
            else:
                lat1 = lat
                lon1 = lon
                if i<1:
                    print("1")
                    i = i+ 1
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
                rover_cord.latitude = lat
                rover_cord.longitude = lon
                pub.publish(rover_cord)
                rospy.loginfo(pose)
                print("\n")
                oldlon = lon
                oldlat = lat  
        except:
            print("unable to process", gpsdata)
    except:
        print("unable to decode", gpsdata)