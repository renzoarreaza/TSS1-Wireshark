#! /usr/bin/python

import argparse
import subprocess
import time
import datetime
import csv
import math

#/* https://github.com/wireshark/wireshark/blob/master/wiretap/wtap.h
# * PHY types.
# */
#define PHDR_802_11_PHY_11G            	6 /* 802.11g */
#define PHDR_802_11_PHY_11N          	7 /* 802.11n */

phy_types = ['Unknown', '802.11 FHSS', '802.11 IR', '802.11 DSSS', '802.11b', '802.11a', '802.11g',
		'802.11n', '802.11ac', '802.11ad',]

#/* 802.11n MSC vs Modulation https://en.wikipedia.org/wiki/IEEE_802.11n-2009 */
modulation_802_11n_mcs = ['BPSK', 'QPSK', 'QPSK', '16QAM', '16QAM', '64QAM', '64QAM', '64QAM', 
				'BPSK', 'QPSK', 'QPSK', '16QAM', '16QAM', '64QAM', '64QAM', '64QAM',
				'BPSK', 'QPSK', 'QPSK', '16QAM', '16QAM', '64QAM', '64QAM', '64QAM',
				'BPSK', 'QPSK', 'QPSK', '16QAM', '16QAM', '64QAM', '64QAM', '64QAM']

# /* 802.11g Data Rate vs Modulation https://en.wikipedia.org/wiki/IEEE_802.11g-2003 */
modulation_802_11g_datarate = {6:'BPSK', 9:'BPSK', 12:'QPSK', 18:'QPSK', 24:'16QAM', 36:'16QAM', 48:'64QAM', 54:'64QAM'}


#Reading input arguments
parser = argparse.ArgumentParser()
parser.add_argument("interface", help="Interface to be monitored")
parser.add_argument("BSSID", help="BSSID of the AP to be monitored")
parser.add_argument("MAC", help="MAC address of the host to be monitored")
parser.add_argument("FileName", help="Name of the file used to store the frames")
parser.add_argument("Duration", help="Time duration of the test (minutes)", type=int)
args = parser.parse_args()

interface = args.interface
bssid = args.BSSID
bssid = bssid.lower()
mac = args.MAC
mac = mac.lower()
filename = args.FileName
duration = args.Duration

time_interval = 1

#Starting Tshark
ts = time.time()
print datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

args = "sudo tshark -i "+interface+" -T fields -e wlan_radio.phy -e wlan_radio.data_rate -e wlan_radio.11n.mcs_index -e wlan.bssid -e wlan.da -e frame.time_epoch -e wlan_radio.signal_dbm -f \"wlan type data subtype data or wlan type data subtype qos-data\" -E separator=, -E quote=d -a duration:"+str(duration*60)+" > "+filename
p = subprocess.Popen(args, shell=True)
p.wait()


#Opening CSV files
results_802_11n_file = open(filename+'_mcs_802_11n.csv', 'w')
results_802_11n_file_csv = csv.writer(results_802_11n_file)
results_802_11n_file_csv.writerow(['time', 'modulation', 'datarate', 'total'])

results_802_11g_file = open(filename+'_mcs_802_11g.csv', 'w')
results_802_11g_file_csv = csv.writer(results_802_11g_file)
results_802_11g_file_csv.writerow(['time', 'modulation', 'datarate', 'total'])


#Parsing file - Modulation/Data rate vs Time (time_interval)
i = 1
count_802_11n = {}
count_802_11g = {}


with open(filename) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if (float(row[5]) <= ts + i*(60*time_interval)) and (row[3] == bssid) and (row[4] == mac):
	    if int(row[0]) == 7:
		index = row[1],modulation_802_11n_mcs[int(row[2])]
		if index in count_802_11n.keys():
		    count_802_11n[index] = count_802_11n[index] + 1
    		else:
		    count_802_11n[index] = 1
	    if int(row[0]) == 6:
		index = row[1],modulation_802_11g_datarate[int(row[1])]
		if index in count_802_11g.keys():
		    count_802_11g[index] = count_802_11g[index] + 1
   		else:
		    count_802_11g[index] = 1
	elif (row[3] == bssid) and (row[4] == mac):
	    for (datarate,modulation),total in count_802_11n.items():
	        datarate = datarate.replace(',','.')
	        results_802_11n_file_csv.writerow([i*time_interval, modulation, float(datarate), total])
	    for (datarate,modulation),total in count_802_11g.items():
	        datarate = datarate.replace(',','.')
	        results_802_11g_file_csv.writerow([i*time_interval, modulation, float(datarate), total])
	    i = i + 1
	    count_802_11n = {}
	    count_802_11g = {}

if count_802_11n or count_802_11n:
    for (datarate,modulation),total in count_802_11n.items():
	datarate = datarate.replace(',','.')
	results_802_11n_file_csv.writerow([i*time_interval, modulation, float(datarate), total])
    for (datarate,modulation),total in count_802_11g.items():
	datarate = datarate.replace(',','.')
	results_802_11g_file_csv.writerow([i*time_interval, modulation, float(datarate), total])

results_802_11n_file.close()
results_802_11g_file.close()




