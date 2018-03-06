#!/usr/bin/python
import csv
import sys
import subprocess

# sudo tshark -i mon0 -T fields -e wlan_radio.data_rate -e radiotap.mcs.index -e wlan_radio.phy -e wlan_radio.channel -e radiotap.channel.flags.cck -e wlan_radio.11n.bandwidth -f "wlan type data subtype data or wlan type data subtype qos-data" -a duration:300 -E separator=, > capturecsv.csv
# phy definition
# source: https://github.com/wireshark/wireshark/blob/master/wiretap/wtap.h
# 0, PHY not known */
# 1, 802.11 FHSS */
# 2, 802.11 IR */
# 3, 802.11 DSSS */
# 4, 802.11b */
# 5, 802.11a */
# 6, 802.11g */
# 7, 802.11n */
# 8, 802.11ac */
# 9, 802.11ad */

n_rates = []
n_rate = []

direc = sys.argv[1]
directory = "../capture/" + direc + "/"
command = "ls -1 " + "\"" + directory + "\"" + " | wc -l"

r = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(filemax, rerr) = r.communicate()
r_status = r.wait()

y = 0 
while y < int(filemax):
	y+=1

	# 802.11n mcs to mod mapping 
	# source: https://en.wikipedia.org/wiki/IEEE_802.11n-2009
	MCS_BPSK = [0, 8, 16, 24, 32]
	MCS_QPSK = [1, 2, 9, 10, 17, 18, 25, 26]
	MCS_QAM16 = [3, 4, 11, 12, 19, 20, 27, 28]
	MCS_QAM64 = [5, 6, 7, 13, 14, 15, 21, 22, 23, 29, 30, 31]

	BPSK = 0
	QPSK = 0
	QAM16 = 0
	QAM64 = 0
	QAM256 = 0
	asym = 0
	DBPSK = 0
	DQPSK = 0

	b_mod = [0] * 4 # DBPSK, DQPSK, BPSK, QPSK
	g_mod = [0] * 4 # BPSK, QPSK, 16-QAM, 64-QAM
	n_mod = [0] * 5 # BPSK, QPSK, 16-QAM, 64-QAM, Asymetric

	b_rates = [1, 2, 5.5, 11]
	b_rate = [0] * 4 # 1, 2, 5.5, 11
	g_rates = [6, 9, 12, 18, 24, 36, 48, 54]
	g_rate = [0] * 8 # 6, 9, 12, 18, 24, 36, 48, 54
	n_rate = [0] * len(n_rate)
	 
	a = 0
	b = 0
	g = 0
	n = 0
	ac = 0
	b_chan_unk = 0	
	g_chan_unk = 0	
	n_chan_unk = 0	

	ch_intf = [0] * 18 # only index 1 to 13 will be used, extra spots for overflow
	ch_usage = [0] * 18 # only index 1 to 13 will be used, extra spots for overflow
	 
	rate = [] # float
	mcs = []
	phy = []
	chan = []
	cck = []
	n_bw = []

	filecsv = directory + "capture" + str(y) + ".csv"
	with open(filecsv) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			rate.append(float(row[0] or 0))
			mcs.append(int(row[1] or 0))
			phy.append(int(row[2] or 0))
			chan.append(int(row[3] or 0))
			cck.append(int(row[4] or 0))
			n_bw.append(int(row[5] or 0))

	imax = len(rate) 
	i = 0
	while i < imax:
		#if phy[i] == 0: # unknown PHY
		#	
		if phy[i] == 4: # 802.11b
		# http://rfmw.em.keysight.com/wireless/helpfiles/n7617a/dsss_frame_structure.htm#Data_rate
			b+=1
			#determining modulation
			if rate[i] == 1:
				DBPSK+=1
				b_mod[0]+=1
			elif rate[i] == 2 or ((rate[i] == 5.5 or rate[i] == 11) and cck[i] == 1):
				DQPSK+=1 
				b_mod[1]+=1
			elif rate[i] == 5.5 and cck[i] == 0:
				BPSK+=1
				b_mod[2]+=1
			elif rate[i] == 11 and cck[i] == 0:
				QPSK+=1
				b_mod[3]+=1

			# channel interference
			if 1 <= chan[i] <=13:
				ch_usage[chan[i]]+=1
				for x in [r for r in range(-2, 3) if r != 0]:
					ch_intf[chan[i]+x]+=1
			else:
				b_chan_unk+=1	

			# rate usage
#			if rate[i] == 1:
#				b_rate[0]+=1
#			elif rate[i] == 2:
#				b_rate[1]+=1
#			elif rate[i] == 5.5:
#				b_rate[2]+=1
#			elif rate[i] == 11:
#				b_rate[3]+=1
			x = 0
			while x <=3:
				if rate[i] == b_rates[x]:
					b_rate[x]+=1
				x+=1

		elif phy[i] == 5: # 802.11a
			# modulation determined by the datarate
			# source: https://en.wikipedia.org/wiki/IEEE_802.11a-1999
			a+=1
			if rate[i] == 6 or rate[i] == 9: # BPSK
				BPSK+=1	
			elif rate[i] == 12 or rate[i] == 18: # QPSK
				QPSK+=1
			elif rate[i] == 24 or rate[i] == 36: # 16-QAM 
				QAM16+=1
			elif rate[i] == 48 or rate[i] == 54: # 64-QAM
				QAM64+=1
			
		elif phy[i] == 6: # 802.11g
			# modulation determined by the datarate
			# source: https://en.wikipedia.org/wiki/IEEE_802.11g-2003 
			g+=1
			# determining modulation
			if rate[i] == 6 or rate[i] == 9: # BPSK
				BPSK+=1	
				g_mod[0]+=1
			elif rate[i] == 12 or rate[i] == 18: # QPSK
				QPSK+=1
				g_mod[1]+=1
			elif rate[i] == 24 or rate[i] == 36: # 16-QAM 
				QAM16+=1
				g_mod[2]+=1
			elif rate[i] == 48 or rate[i] == 54: # 64-QAM
				QAM64+=1
				g_mod[3]+=1

			# channel interference
			if 1 <= chan[i] <=13:
				ch_usage[chan[i]]+=1
				for x in [r for r in range(-2, 3) if r != 0]:
					ch_intf[chan[i]+x]+=1
			else:
				g_chan_unk+=1	

			# rate usage
#			if rate[i] == 6:
#				g_rate[0]+=1
#			elif rate[i] == 9:
#				g_rate[1]+=1
#			elif rate[i] == 12:
#				g_rate[2]+=1
#			elif rate[i] == 18:
#				g_rate[3]+=1
#			elif rate[i] == 24:
#				g_rate[4]+=1
#			elif rate[i] == 36:
#				g_rate[5]+=1
#			elif rate[i] == 48:
#				g_rate[6]+=1
#			elif rate[i] == 54:
#				g_rate[7]+=1

			x = 0
			while x <=7:
				if rate[i] == g_rates[x]:
					g_rate[x]+=1
				x+=1


		elif phy[i] == 7: # 802.11n
			# modulation determined by mcs value
			n+=1
			if mcs[i] in MCS_BPSK:
				BPSK+=1	
				n_mod[0]+=1
			elif mcs[i] in MCS_QPSK:
				QPSK+=1
				n_mod[1]+=1
			elif mcs[i] in MCS_QAM16:
				QAM16+=1
				n_mod[2]+=1
			elif mcs[i] in MCS_QAM64:
				QAM64+=1
				n_mod[3]+=1
			elif 32 <= mcs[i] <= 70: # Asymetric modulation
				asym+=1		
				n_mod[4]+=1

			# BW definition
			# https://mrncciew.com/2014/11/04/cwap-ht-operations-ie/

			# channnel interference
			if 1 <= chan[i] <=13:
				ch_usage[chan[i]]+=1
				if n_bw[i] == 0: # 20Mhz
					for x in [r for r in range(-2, 3) if r != 0]:
						ch_intf[chan[i]+x]+=1

				if n_bw[i] == 1: # 20 or 40Mhz
					for x in [r for r in range(-4, 5) if r != 0]:
						ch_intf[chan[i]+x]+=1
			else:
				n_chan_unk+=1	

			# rate usage
			if rate[i] in n_rates:
				for z in [z for z,x in enumerate(n_rates) if x == rate[i]]:
					n_rate[z]+=1
			else: # no packet with this rate has been received
				n_rates.append(rate[i])
				n_rate.append(1)	
				



		elif phy[i] == 8: # 802.11ac
			# source: https://en.wikipedia.org/wiki/IEEE_802.11ac
			ac+=1
			if mcs[i] == 0: #BPSK
				BPSK+=1
			elif mcs[i] in [1, 2]: #QPSK
				QPSK+=1
			elif mcs[i] in [3, 4]: #16-QAM
				QAM16+=1
			elif mcs[i] in [5, 6, 7]: #64-QAM
				QAM64+=1
			elif mcs[i] in [8, 9]: #256-QAM
				QAM256+=1

		#elif phy[i] == 9: #802.11ad
		i+=1
	
	pre = b, g, n, b_mod, g_mod, n_mod, b_rates, b_rate, g_rates, g_rate, len(n_rates), n_rates, n_rate
	pre = str(pre)
	mid = pre.replace("[", "")
	out = mid.replace("]", "")
	out = out[1:-1]	
	print(out)
	name = "../results/" + direc + ".csv"
	f = open(name, "a")
	f.write(out + "\n")
	f.close()	


#	print ('Number of packets= ' + str(imax))
#	print ('BPSK = ' + str(BPSK))
#	print ('QPSK = ' + str(QPSK))
#	print ('16-QAM = ' + str(QAM16))
#	print ('64-QAM = ' + str(QAM64))
#	print ('Asym mod. = ' + str(asym))
#	print ('256-QAM = ' + str(QAM256))
#	print ('DBPSK = ' + str(DBPSK))
#	print ('DQPSK = ' + str(DQPSK))
#	print ('packets in a = ' + str(a))
#	print ('packets in b = ' + str(b))
#	print ('packets in g = ' + str(g))
#	print ('packets in n = ' + str(n))
#	print ('channel\tusage\tinterference')
#	for i in range(1, 14): # channels 1 to 13
#		print(str(i) + "\t" + str(ch_usage[i]) + "\t" + str(ch_intf[i]))
#	print ('channel 0')
#	print (ch_usage[0])
#	print (str(b_chan_unk) + ' packets with unknown channel with PHY = b')
#	print (str(g_chan_unk) + ' packets with unknown channel with PHY = g')
#	print (str(n_chan_unk) + ' packets with unknown channel with PHY = n')


