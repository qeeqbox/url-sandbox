'''
    __G__ = "(G)bd249ce4"
    box -> run
'''

from sys import argv
from binascii import hexlify
from pickle import dumps as pdumps
from binascii import unhexlify
from pickle import loads
from tinydb import TinyDB, Query
from qbsandbox import chrome_driver
from qbsniffer import QSniffer
from qtor import Connection
from socket import gethostbyname
from time import sleep

if len(argv) == 2:
    print("[SandBox] Parsing arguments")
    parsed = loads(unhexlify(argv[1]))
    analyzer_logs = TinyDB("{}{}{}".format(parsed['locations']['box_output'], parsed['task'], parsed['locations']['analyzer_logs']))
    if not parsed['use_proxy']:
        print("[SandBox] Using tor")
        c = Connection()
        c.start_supervisord()
        c.run()
    else:
        print("[SandBox] Using proxy")
        prxoy_dns = gethostbyname("proxy")
        if parsed['proxy'] == 'socks5://proxy:9050':
            parsed['proxy'] = 'socks5://{}:9050'.format(prxoy_dns)
        with open("/etc/resolv.conf", 'w') as file:
            file.write("nameserver {}\n".format(prxoy_dns))
    if parsed['sniffer_on']:
        print("[SandBox] Running Sniffer")
        sniffer_logs = TinyDB("{}{}{}".format(parsed['locations']['box_output'], parsed['task'], parsed['locations']['sniffer_logs']))
        x = QSniffer(parsed, '', 'eth0', sniffer_logs)
        x.run_sniffer(process=True)
    print("[SandBox] Testing with chrome webdriver")
    chrome_driver(parsed, analyzer_logs)
    print("[SandBox] Stopping Sniffer")
    if parsed['sniffer_on']:
        x.kill_sniffer(process=True)
    print("[SandBox] Done!!")
