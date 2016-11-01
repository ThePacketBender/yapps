#!/usr/bin/env python
import getopt
from socket import *
from netaddr import *
from threading import *
import sys

screenLock = Semaphore(value=1)

def usage():
	print "yet another python port scanner"
	print
	print "Usage: python ./yapps.py -t target_ip -p port"
	print "e.g.: python ./yapps.py -t 192.168.0.1 -p 80"
	print
	print "-f --filename	- import hostslist from filename"
	print "-c --connection	- connection protocol: tcp or udp"
	print "-h --help	- return usage"
	print "-p --port	- set port to scan"
	print "-t --target	- set target ip to scan; accepts ip address (e.g. 192.168.0.1), ip address range (e.g. 192.168.1.1-192.168.1.255), CIDR notation (e.g. 192.168.1.0/24), DNS name (e.g. google.com)"
	print "-u --timeout	- set tcp connection attempt timeout"

def tcp_conn(host, port, protocol):
	try:
		conn = socket(AF_INET, SOCK_STREAM)
		conn.connect((host, port))
		conn.send('request\r\n')
		results = conn.recv(1024)	
		screenLock.acquire()
		print "[+]" + str(port) + "/" + protocol + " open\n" + "[+]" + str(results)
	except timeout, err:
		screenLock.acquire()
		print "[-]" + str(port) + "/" + protocol + " closed"
	finally:
		screenLock.release()
		conn.close()

def udp_conn(host, port, protocol):
	try:
		conn = socket(AF_INET, SOCK_DGRAM)
		conn.sendto('request\r\n', (host, port))
		conn.bind('', port)
		while True:
			results, addr = conn.recvfrom(1024)
		screenLock.acquire()
		print "[+]" + str(port) + "/" + protocol + " open\n" + "[+]" + results
	except error, err:
		screenLock.acquire()
		print "[-]" + str(port) + "/" + protocol + " closed"
	finally:
		screenLock.release()
		conn.close()

def port_scan(hosts, ports, protocol):
	if protocol == "tcp":
		for host in hosts[0:]:
			try:
				print "scanning host " + host + " " + gethostbyaddr(host)
			except herror, err:
				print "[-]scanning host " + str(host)
			for port in ports:
				t=Thread(target = tcp_conn, args = (host, int(port), protocol))
				t.start()
			t.join()
	elif protocol == "udp":
		for host in hosts:
			try:
				print "scanning host " + host + " " + gethostbyaddr(host)
			except herror, err:
				print "[-]scanning host " + str(host)
			for port in ports:
				t=Thread(target = udp_conn, args = (host, int(port), protocol))
				t.start()
			t.join()

def main(parseargs):
	hosts = ['127.0.0.1',]
	ports = [80,]
	protocol = "tcp"
	setdefaulttimeout(4)
	
	#getopt option parser
	try:
		opts, args = getopt.getopt(parseargs, "hf:c:u:t:p:", ["help", "filename", "connection", "timeout", "target", "port"])
	except getopt.GetoptError as e:
		print "[-]Error initializing option parser" + str(e)
		usage()
		return -1
	for o,a in opts:
		if o in ("-h", "--help"):
			usage()
			return 0
		elif o in ("-c", "--connection"):
			if a in ("udp","tcp"):
				protocol = str(a).strip()
			else:
				print("[-]connection protocol " + a + " not invalid, default protocol: tcp")
		elif o in ("-p", "--port"):
			ports_temp = (port for port in a.split(","))
			ports = []
			for p in ports_temp:
				if len(str(p).split("-")) == 2:
					r = str(p).split("-")
					for port in range(int(r[0]),int(r[1])): ports.append(int(port))
				else:
					ports.append(p)
		elif o in ("-f", "--filename"):
			fhosts = []
			ip_reg = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
			url_reg = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|(?<=[a-zA-z]|[0-9]|[$-_@.&+]|[!*\(\),]){2,60}\.[a-zA-Z]{2,3}')
			try:
				f = open(a, "r")
				lines = f.readlines()
				f.close()
			except IOError as e:
				print "[-]Error reading file passed as hostlist" + str(e)
				if not ('-t' | '--target') in opts: return -1
			for host in map((ip_reg.findall(line) | url_reg.findall(line)),[line for line in lines]): fhosts += str(host)
			if not ('-t' | '--target') in opts: main((argparse.extend(['-t',','.join(fhosts)])))
		elif o in ("-t", "--target"):
			hosts = []
			for h in a.split(","):
				if len(h.split(".")) in (1,2):
					try:
						ip = netaddr.IPAddress(gethostbyname(h),"ipv4")
						
					except Exception:
						pass
				elif len(h.split(".")) == 4:
					if len(h.split("/")) == 2:
						hosts += (str(ip) for ip in list(IPNetwork(h)))
					elif "*" in h.split("."):
						hosts += (str(ip) for ip in list(IPGlob(h)))
					else:
						hosts.append(str(IPAddress(h)))
				elif len(h.split(":")) == 8:
					if len(h.split("/")) == 2:
						hosts += (ip for ip in list(IPNetwork(h)))
					else:
						hosts.append(str(IPAddress(h, 6)))
				elif len(h.split("-")) == 2:
					hosts += (ip for ip in list(IPSet(IPRange(h.split[0],h.split[1]))))
				else:
					print "[-]error handling target hosts " + h + ", discarded"
		elif o in ("-u", "--timeout"):
			try:
				setdefaulttimeout(int(a))
			except Exception as e:
				print "[-]timeout defaulting to 4, could not accept argument" + str(a) + ":" + str(e)
		else:
			assert False,"[-]unhandled option" + o
	try:
		port_scan(hosts, ports, protocol)
	except:
		return -1
if __name__ == "__main__":
	argparse = sys.argv[1:]
	main(argparse)
