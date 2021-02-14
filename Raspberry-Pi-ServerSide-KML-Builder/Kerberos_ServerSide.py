import serial
import io
import socket
import time
import os
import berryIMU


#GPS init from serial port
GPS_port = "/dev/serial0"
GPS_serialPort = serial.Serial(GPS_port, baudrate = 9600, timeout = 0.5)
GPS_readSerialPort = GPS_serialPort.readline().decode()


def getGPS():
    global Lat
    global Lon
    if GPS_serialPort.isOpen() == False:
        GPS_serialPort.open()
    else:
        GPS_serialPort.close()
        GPS_serialPort.open()
    
    while True:
        GPS_line = GPS_serialPort.readline().decode()
        if "$GNRMC" in str(GPS_line):
            GPS_line = GPS_line.split(',')
            print(GPS_line)
            
            if GPS_line[3] != '' and GPS_line[5] != '':
                DD_Lat = int(float(GPS_line[3])/100)
                DD_Lon = int((float(GPS_line[5]))/100)
                SS_Lat = float(GPS_line[3]) - (DD_Lat*100)
                SS_Lon = float(GPS_line[5]) - (DD_Lon*100)
                
                
                Lat = DD_Lat + (SS_Lat)/60
                Lon = (DD_Lon + (SS_Lon/60))*-1
                break
            
            else:
                Lat = 0
                Lon = 0
                break
        
#Set ethernet IP address
cmd_setIP = os.popen('sudo ifconfig eth0 169.254.76.66')
cmd_read = cmd_setIP.read()

#Start socket connection
HOST = '169.254.76.66'
PORT = 1070
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST,PORT))


s.listen(1)
print("Socket awaiting connection")
(conn,addr) = s.accept()
print("Socket connected")



print("Getting fix . . .")
while True:
    getGPS()
    reqInit = conn.recv(1024)
    
    if reqInit.decode('utf-8') == 'GPS_fixReq':
        print("Request received:  " + reqInit.decode('utf-8'))
    
    GPS_posInit = str(Lat) + ',' + str(Lon)
    print("Sending location:  " + GPS_posInit)

    GPS_pos_bytes_Init = bytes(GPS_posInit, 'utf-8')

    conn.send(GPS_pos_bytes_Init)
    
    
    if Lat != 0 and Lon != 0:
        break
    

print("Testing compass . . .")
for i in range(10):
    berryIMU.readCompass()
    print(berryIMU.tiltCompensatedHeading)
    time.sleep(1)
        

while True:
    berryIMU.readCompass()
    print(berryIMU.tiltCompensatedHeading)
    getGPS()
    
    req = conn.recv(1024)
    
    
    if req.decode('utf-8') == 'GPS_req':
        print("Request received:  " + req.decode('utf-8'))
        GPS_pos = str(Lat) + ',' + str(Lon) + ',' + str(berryIMU.tiltCompensatedHeading)
        print("Sending location:  " + GPS_pos)

        GPS_pos_bytes = bytes(GPS_pos, 'utf-8')

        conn.send(GPS_pos_bytes)
    


