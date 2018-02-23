#!/usr/bin/python
import csv


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

rate = []
mcs = []
phy = []

with open('capturecsv.csv') as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	for row in csvReader:
		rate.append(int(row[0] or 0))
		mcs.append(int(row[1] or 0))
		phy.append(int(row[2] or 0))
imax = len(rate) 
i = 0
while i < imax:
	#if phy[i] == 0: # unknown PHY
	#	
	#elif phy[i] == 4: # 802.11b
	#
	#elif phy[i] == 5 or phy[i] == 6: # 802.11a & 802.11g
	if phy[i] == 5 or phy[i] == 6: # 802.11a & 802.11g
		# modulation determined by the datarate
		# source: https://en.wikipedia.org/wiki/IEEE_802.11g-2003 
		# source: https://en.wikipedia.org/wiki/IEEE_802.11a-1999
		if rate[i] == 6 or rate[i] == 9: # BPSK
			BPSK+=1	
		elif rate[i] == 12 or rate[i] == 18: # QPSK
			QPSK+=1
		elif rate[i] == 24 or rate[i] == 36: # 16-QAM 
			QAM16+=1
		elif rate[i] == 48 or rate[i] == 54: # 64-QAM
			QAM64+=1

	elif phy[i] == 7: # 802.11n
		# modulation determined by mcs value
		if mcs[i] in BPSK:
			BPSK+=1	
		elif mcs[i] in QPSK:
			QPSK+=1
		elif mcs[i] in QAM16:
			QAM16+=1
		elif mcs[i] in QAM64:
			QAM64+=1
		elif 32 <= mcs[i] <= 70: # Asymetric modulation
			asym+=1		

	elif phy[i] == 8: # 802.11ac
		# source: https://en.wikipedia.org/wiki/IEEE_802.11ac
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


print ('BPSK = ' + str(BPSK))
print ('QPSK = ' + str(QPSK))
print ('16-QAM = ' + str(QAM16))
print ('64-QAM = ' + str(QAM64))
print ('Asym mod. = ' + str(asym))
print ('256-QAM = ' + str(QAM256))
