#!/usr/bin/env python
import socket, sys, threading
from struct import *
import curses
import yapps.yapps

def checksum(data):
	q = 0
	for i in range(0, len(data), 2):
		w = ord(data[i]) + (ord(data[i+1]) << 8)
		q = q + w
		q = (q & 0xffff) + (q >> 16)
	return ~q & 0xffff

class IP_Header:
	def __init__(self):
		#ip header field defaults -see rfc791
		self.ver = 4 #4 bits, format of internet header, e.g. ipv4
		self.ihl = 5 #4 bits, internet header length in 32-bit words, thus points to beginning of data (minimum correct value = 5)
		self.tos = 0 #8 bits, type of service
			   #bits 0-2: Precedence - 111 Network Control, 110 Internetwork Control, 101 CRITIC/ECP, 100 Flash Override
			   #011 Flash, 010 Immediate, 001 Priority, 000 Routine
			   #bit 3: 0 = Normal Delay,		1 = Low Delay
			   #bit 4: 0 = Normal Throughput, 	1 = High Throughput
			   #bit 5: 0 = Normal Reliablity,	1 = High Reliability
			   #bits 6-7: Reserved for Future Use
		self.tot_len = 0 #kernel will automatically fill correct total len
		self.id = 4241
		self.frag_off = 0
		self.ttl = 255
		self.check = 10
		self.proto = socket.IPPROTO_TCP
		self.saddr = socket.inet_aton(source_ip)	#source ip can be spoofed
		self.daddr = socket.inet_aton(dest_ip)
		self.ihl_ver = (self.ver << 4) + self.ihl
		try:
			self.packet_header()
		except error as e:
			print e
			return -1
		self.checks()

	def packet_header(self):
		self.header = pack('!BBHHHBBH4s4s' , self.ihl_ver, self.tos, self.tot_len, self.id, self.frag_off, self.ttl, self.proto, self.check, self.saddr, self.daddr)


class TCP_Header:
#takes object as argument, expects ip header
	def __init__(self):
		#tcp header field defaults -see rfc793
		self.source = 127 #port
		self.dest = 123   #port
		self.seq = 454
		self.ack_seq = 0
		self.ack = 1
		self.syn = 1
		self.fin = 0
		self.doff = 5    
		self.rst = 0
		self.psh = 0
		self.urg = 0
		self.urg_ptr = 0
		self.window = socket.htons(4160) # max_size for window
		self.offset_res = (self.doff << 4) + 0
		self.flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh <<3) + (self.ack << 4) + (self.urg << 5)
		self.obj = header()
		try:
			self.packet_header()
		except error as e:
			print e
			return -1
		#include scan type presets:
		#SYN	| SYN, ACK
		#ACK	| ACK
		#X-mas	| FIN, URG, PSH
		#NULL	|

	#def yapps_ncurses.view_header(self)
	def checksum(self):
		pseudoheader = pack('!4s4sBBH', ip.saddr, ip.daddr, 0, socket.IPPROTO_TCP , len(self.header))
		pseudoheader += self.header
		self.check = socket.hotns(checksum(c))
		return self.check
	def packet_header(self):
		self.header = pack('!HHLLBBH', self.source, self.dest, self.seq, self.ack_seq, self.offset_res, self.flags, self.window)
		self.header = ip.header + self.header
		self.checksum()
		self.header += pack('H' , self.check) + pack('!H' , self.urg_ptr)
		return self.header

class UDP_Header:
	def __init__(self, header):
		self.source = 127 #port
		self.dest = 123   #port
		try:
			self.packet_header()
		except error as e:
			print e
			return -1
		self.obj = header


	def checksum(self):
		pseudoheader = pack('!4s4sBBH', ip.saddr, ip.daddr, 0, socket.IPPROTO_TCP , len(self.header))
		pseudoheader += self.header
		self.check = socket.hotns(checksum(c))
		return self.check
	def packet_header(self):
		self.header = struct.pack('!HHHH', source, dest, 8)
		self.header = ip.header + self.header
		self.check = socket.htons(checksum(self.header))
		self.header += pack('H', self.check)


def hex():
	hexes = packet.encode('hex')
	hex_format = ""
	x = False
	n = 0
	while (n+2) <= len(hexes):
		for i in range(8):
			hex_format += "%s " % (hexes[n:n+2])
			n += 2
		hex_format += " "
		if x == True: hex_format += "\n"
		x = not x
	return hex_format

def build_packet(transport_header, data):
	packet = ''
	#simple packet injection function for raw socket
	packet = transport_header + data
	#ipheader expected prepending transport header, necessary for checksum

	return packet

class sock_raw(socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)):
	#creates RAW socket
	def __init__(self, header):
		self.data = "\0"
		self.addr = self.getsockname()
		self.header = header
		self.host = self.header.daddr
		#local(icmp) lookup of own name returned from hostname in socket returns access point name
		self.gateway = socket.gethostbyname(socket.gethostname())
		self.captures = list()

	def flood():
		while(curses.getch()):
			for i in range(22-yapps.yapps.pool_sema):
				yapps.yapps.Threadpool
				while True: s.sendto(self.header.packet_header(), (host, 0))
				Threadpool.join()

	def traceroute():
		s1 = socket.getprotobyname('icmp')
		s2 = socket.getprotobyname('udp')
		max_hops = 30
		ttl = 1
		while True:
			srv = socket.socket(socket.AF_INET, socket.SOCK_RAW, 'icmp')
			cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 'udp')
			srv.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
			srv.bind(("", self.header.port)
			cli.sendto("", (self.header.daddr, 0))
			try:
				_, caddr = srv.recvfrom(512)
				caddr = caddr[0]
				try:
					caddr = socket.gethostbyaddr(caddr)[0]
				except socket.error:
					cname = caddr
			except socket.error:
				pass
			finally:
				srv.close()
				cli.close()

			if caddr is True:
				chost = str(cname + " ("+caddr+")")
			else
				chost = "*"
			print "%d\t%s" % (ttl, chost)
			ttl += 1

			if caddr == self.header.daddr or ttl &gt; max_hops:
				break

	def sniff(port):
		self.bind(gateway, 0)
			#set promiscuous mode
		self.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
		while(curses.getch()):
			pcap, pcap_addr=sock.recvfrom(65565)
			iphdr = ip(pcap[:20])
			screen.addstr(iphdr.parse())
			curses.refresh
			captures.append(pcap)
		return captures
	
	def pcap_read(self.captures):
		for pcap in captures:
			cap = screen.addstr(struct.unpack("!BBHHHBBHII", pcap)
			screen.addstr(cap([:20])
			screen.addstr(cap([20:])
			screen.addstr(hex(cap))
			curses.getch()
	#def pcap_decode(self.captures)		
	#		
	#def save_pcaps(self.captures)
		

	def __del__(self):
		return s

def test():
	tcp = TCP_Header()
	tcp_header = tcp.packet_header()
	packet = build_packet(tcp_header, data)
	hexes = packet.encode('hex')
	x = False
	n = 0
	while (n+2) <= len(hexes):
		for i in range(8):
			sys.stdout.write("%s " % (hexes[n:n+2]))
			n += 2
		sys.stdout.write(" ")
		if x == True: print
		x^=True
	s = sock_raw()
	s.sendto(packet, (dest_ip, 0))

def main():
	#define global presets
	global dest_ip, source_ip, data
	global ip, transport
	data = "this is my packet, there are many others like it, but this one is mine"
	dest_ip = "127.0.0.1"
	source_ip = "127.0.0.1" #for LAN address set socket.gethostbyname(socket.gethostname())
	ip = IP_Header()
	ip_header = ip.packet_header()
	test()

if __name__ == "__main__":
	main()
