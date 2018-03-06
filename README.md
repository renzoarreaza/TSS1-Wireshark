# TSS1-Wireshark
Wireshark project of the TSS1 group for the Wireless Networking course 2017/2018

The implementation-1 and 2 folders have old code of different approaches we tried before arriving at the main code in implementation-3


How to run the code:
First, the wireless card has to be set to promiscious mode. We did this by using the airmon-ng command.
sudo airmon-ng start <wireless-intf>

Then you can run the source.py script as follows:
  ./source.py <interface> <bssid> <file> <duration>
 
interface: Interface to be monitored
bssid: BSSID of the AP to be monitored
file: Name of the file used to store the frames
duration: Time duration of the test (minutes)

After starting the matlab code it will request the zone boundaries, and the file name of the csv file (output of the python script)
