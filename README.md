#YAPPS - YET ANOTHER PYTHON PORT SCANNER

***NOTE***
Final program is being written to create any possible packet header(s) or raw
socket prior to initating connections while implementing shortcuts to/for
specific configurations and functionalities.
**********

Port scanner written for python 2.7 using standard libraries and netaddr libraries. simple_scan.py is a fully functional module that can be launched independently and advanced_scan.py is a module for raw sockets and packet manipulation. yapps_ncurses.py will add a multi-window gui to control packet creation/port scanning function over advanced_scan.py and can act as an entry point to launch simple_scan.py. yapps.py will act as a general purpose launcher implementing functions (e.g. multithreading, logging) to effectively pass information between socket and gui component scripts once linked.

Build incomplete, do not attempt to run setup.py
