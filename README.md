# KML-Builder-For-Kerberos-SDR
This is a proof of concept to be further built upon for interfacing the KerberosSDR with Ozzmaker's BerryGPS and IMU v4 in order to compile latitude, longitude, magnetic heading, and direction of arrival from target frequency.  This data is received by the PC over the ethernet port(Lat, Lon, and heading) and over the KerberosSDR hotspot by the raspberry pi acting as a server.   With this data the client-side windows pc builds a static and live-updating KML file to show accurate lines of bearing regardless of which direction antenna array is facing on Google Earth.  

***DISCLAIMER: Code for interfacing with the IMU is taken from Ozzmaker's github repository.  Some of these files are not my own work.  See Ozzmaker's code and GPS product used for this project here:
https://ozzmaker.com/product/berrygps-imu/
https://github.com/ozzmaker/BerryIMU

Code for KerberosSDR
https://github.com/rtlsdrblog/kerberossdr

Guide for setting up KerberosSDR:
https://www.rtl-sdr.com/ksdr/

Guide for setting up BerryGPS:
https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/

Items needed for implementation:

-KerberosSDR
-High quality USB cable
-4 magnetic whip antennas (Male SMA)
-5v Battery pack
-Raspberry Pi 3 B+
-Raspberry Pi 3 B+ wall charger
-BerryGPS IMU v4
-Cat5 ethernet crossover
-Windows 10 PC/laptop/tablet with ethernet port


To implement this proof of concept:

1)Follow the quick start guide for the KerberosSDR and use the KerberosSDR rasbian provided for SD card
2)Follow the quick start guide for the BerryGPS and the IMU
3)Install the following libraries:
    -XRDP
    -GPSD
4) Run the python server-side first on the raspberry pi over XRDP
5) Run the python client-side from the pc
