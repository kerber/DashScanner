#!/usr/bin/python
import binascii
import logging
import socket
import struct
import sys
import urllib
import urllib2

# URL receiving MAC as post
DASH_URL="http://localhost:1880/dash"
# ARP packet type in bytes
ARP_TYPE='\x08\x06'
# ARP discovery opcode in bytes
ARP_DISC_OPCODE='\x00\x01'
# Source IP of the Dash's discover arp
DASH_SOURCE_IP='0.0.0.0'

# Open raw socket to receive packets
rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
logging.basicConfig(format='%(asctime)s %(message)s')
while True:
	try:
		# Receive packet
		packet = rawSocket.recvfrom(2048)

		# Get ethernet details and filter out non-ARP packets
		ethernet_header = packet[0][0:14]
		ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)
		ethertype = ethernet_detailed[2]
		if ethertype == ARP_TYPE:
			# Get ARP details and filter out non-discovery packets
			arp_header = packet[0][14:42]
			arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)
			opcode = arp_detailed[4]
			source_ip = socket.inet_ntoa(arp_detailed[6])
			if opcode == ARP_DISC_OPCODE and source_ip == DASH_SOURCE_IP:
				try:
					# Get Dash MAC and post it to receiving web service
					source_mac = binascii.hexlify(arp_detailed[5])
					data = urllib.urlencode(dict(mac=source_mac))
					urllib2.urlopen(DASH_URL,data)
				except Exception as e:
					logging.warning("Problem connecting to Dash receiving service: "+DASH_URL+" - "+str(e))
	except:
		logging.warning("Problem connecting to Dash receiving service at: "+DASH_URL+".")
		raise
