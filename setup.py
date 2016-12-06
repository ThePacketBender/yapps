#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name = "yapps",
	version = "0.0.8",
	packages = find_packages(),
	scripts = ['yapps_ncurses.py', 'advanced_scan.py', 'simple_scan.py', 'yapps.py'],

	install_requires = ['curses','locale','time','sys','socket','struct','threading','netaddr','getopt'],
	
	packet_data = {
	
	},

	author = "Jonathon Bohr",
	author_email = "jjbohr@uwm.edu",
	description = "yet another python port scanner",
	license = "",
	keywords = "port scan banner grab socket_RAW ip header tcp udp curses packet",
	url = "https://github.com/sh-sudo-chown"
)
