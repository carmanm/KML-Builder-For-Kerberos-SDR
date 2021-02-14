import numpy as np
import time
import math
import serial
import pynmea2
import io
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys




Lat = 0.00
Lon = 0.00

gpsList = []

#SOCKET CONNECT
HOST = "169.254.76.66"
PORT = 1070

pause = False
stop = False


#Start web driver
browser = webdriver.Edge(executable_path = r'C:\Users\matts\AppData\Local\Programs\Python\Python39\Lib\site-packages\selenium\webdriver\edge\msedgedriver.exe')
browser.get("http://192.168.4.1:8081/compass.html")
assert 'Animated Compass' in browser.title


def piConnect():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Attempting connection . . .")
    s.connect((HOST,PORT))
    print("Connected to: " + str(HOST))

    

def getCoord():
    global s
    
    GPS_req = bytes('GPS_req', 'utf-8')
    s.send(GPS_req)
    while True:
        gps = s.recv(1024)
        
        if not gps:
            print("No data to receive")
            break
            
        coord = gps.decode('utf-8')
        print("_______________________________________________________________________")
        print("DECODED MESSAGE: " + coord)

        coord = coord.split(',')

        
        Lat = float(coord[0])
        Lon = float(coord[1])
        Heading = int(float(coord[2]))
        print("RECEIVED LAT: " + str(Lat))
        print("RECEIVED LON: " + str(Lon))
        print("RECEIVED HEADING: " + str(Heading))

        #Extract doa javascript variable from compass.html
        elem = browser.find_element_by_id('doa')
        str_elem = elem.get_attribute('innerHTML')
        DOA = str_elem[15:18]
        if DOA[2] == 'd':
            DOA = str_elem[15]
            if DOA == '0':
                print("Ensure DOA is enabled on Kerberos app!")
        print("DOA: " + DOA)

        
        gpsList.append((Lat,Lon,Heading,DOA))
        break

def getInitFix():
    global s
    
    GPS_fixReq = bytes('GPS_fixReq', 'utf-8')
    

    while True:
        s.send(GPS_fixReq)
        gpsInit = s.recv(1024)
        
        if not gpsInit:
            print("No data to receive")

            
        fix = gpsInit.decode('utf-8')
        print("_______________________________________________________________________")
        print("INIT DECODED MESSAGE: " + fix)
        fixInit = fix.split(',')

        
        LatInit = int(float(fixInit[0]))
        LonInit = int(float(fixInit[1]))

        print(str(LatInit) + "         " + str(LonInit))

        if LatInit != 0 and LonInit != 0:
            print("Fix successful")
            break
        else:
            print("No fix")



def pause():
    global pause
    pause = True

def resume():
    global pause
    pause = False

def stop():
    global stop
    stop = True


#CONNECT PI
piConnect()



#VARIABLE DEFINITION
x = 0

getInitFix()

#KML BUILD
while True:
    if pause != True:
        getCoord()
        
        lat = gpsList[x][0]
        lon = gpsList[x][1]

        if lat != 0 or lon != 0:
            #COORD
            if x == 0:
                coord = "<Placemark><name>" + str(x) + "</name><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (lon,lat)
            else:
                coord+="\n<Placemark><name>" + str(x) + "</name><Point><coordinates>%s,%s,0</coordinates></Point></Placemark>" % (lon,lat)


            #LINE
            if len(gpsList[x]) > 3:
                heading = gpsList[x][2]
                angle = gpsList[x][3]

                comp_angle = int(float(heading)) + int(float(angle))

                if comp_angle <= 360:
                    comp_angle -= 360
                
                endx = 2 * math.cos(math.radians(comp_angle))
                endy = 2 * math.sin(math.radians(comp_angle))
            
                lat_DOA = lat + endx
                lon_DOA = lon + endy
                
                coord += "<Placemark><LineString><coordinates>%s,%s,1. %s,%s,1.</coordinates></LineString></Placemark>" % (lon,lat, lon_DOA, lat_DOA)
            

            #WRITE   
            with open("posRep.kml", "w") as pos:
                
                pos.write("""<?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2">
            <Document>
                """ +coord+
                """
            </Document>
            </kml>""")
                
        else:
            print("No fix . . .")

        if stop == True:
            break
        
        time.sleep(1)
        x+=1
        




