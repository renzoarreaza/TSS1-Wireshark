#!/bin/bash
dt=$(date '+%d-%m-%Y %H:%M:%S');
mkdir ../capture/"$dt"/

for i in {1..180}
do
	sudo tshark -i mon0 -T fields -e wlan_radio.data_rate -e radiotap.mcs.index -e wlan_radio.phy -e wlan_radio.channel -e radiotap.channel.flags.cck -e wlan_radio.11n.bandwidth -f "wlan type data subtype data or wlan type data subtype qos-data" -a duration:60 -E separator=, > ../capture/"$dt"/capture$i.csv
done
exit 0
