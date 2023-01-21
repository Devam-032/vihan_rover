#!/usr/bin/python3
import serial
import datetime
import re
def dec2deg(value):
   dec = value/100.00
   deg = int(dec)
   min = (dec - int(dec))/0.6
   position = deg + min
   position = "%.7f" %(position)
   return position

mapscale = 18
while True:
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
        print(gpsdata)
        lat = float(gpsdata[2])
        a=int(lat*100)
        b=float(a%100)/3600+float(a%10000-a%100)/6000+float(a%1000000-a%10000)/10000
        lon = float(gpsdata[4])
        d=int(lon*100)
        c=float(d%100)/3600+float(d%10000-d%100)/6000+float(d%1000000-d%10000)/10000
        alt = gpsdata[9]
        satcount = gpsdata[7]
        message = "Altitude={}, Satellites={}\n".format(alt, satcount)
        # gearth = "https://earth.google.com/web/search/@{},{},{}\n".format(lat,lon,alt)
        # mapsapp = "geo:{},{}\n".format(lat, lon)
        # map = "https://www.openstreetmap.org/#map={}/{}/{}\n\n".format(mapscale, lat, lon)
        #print(message, gearth, mapsapp, map)
        print(message, lat, lon,b,c)
    except:
      print("unable to process", gpsdata)
  except:
    print("unable to decode", gpsdata)