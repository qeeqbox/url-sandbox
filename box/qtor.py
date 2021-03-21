'''
    __G__ = "(G)bd249ce4"
    box -> qtor
'''

from subprocess import Popen, PIPE, check_output
from shutil import copyfile
from os import remove
from time import sleep


class Connection():
    def start_supervisord(self):
        Popen("supervisord >/dev/null 2>&1", shell=True)
        sleep(3)

    def delete_tor_file(self):
        try:
            remove("/etc/tor/qtorrc")
        except BaseException:
            pass

    def setuptor_new(self):
        self.delete_tor_file()
        file = 'VirtualAddrNetwork 10.192.0.0/10\nAutomapHostsOnResolve 1\nTransPort 9040\nDNSPort 5353'
        with open("/etc/tor/qtorrc", 'w') as f:
            f.write(file)
            return "Done"
        return "Error"

    def setup_iptables(self):
        file = '''DONOT_TOR="127.0.0.0/9 127.128.0.0/10 127.0.0.0/8 172.16.0.0/12 192.168.0.0/16"
iptables -F
iptables -t nat -F
iptables -t nat -A OUTPUT -m owner --uid-owner $(id -ur debian-tor) -j RETURN
iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353
for NET in $DONOT_TOR; do
 iptables -t nat -A OUTPUT -d $NET -j RETURN
done
iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
for NET in $DONOT_TOR; do
 iptables -A OUTPUT -d $NET -j ACCEPT
done
iptables -A OUTPUT -m owner --uid-owner $(id -ur debian-tor) -j ACCEPT
iptables -A OUTPUT -j REJECT'''
        process = Popen(file, shell=True)
        out, err = process.communicate()
        return "Done"

    def setup_resolve(self):
        file = '#X#TOR#X#\nnameserver 127.0.0.1\n'
        with open("/etc/resolv.conf", 'w') as f:
            f.write(file)
        return "Done"

    def kill_tor(self):
        process = Popen("supervisorctl stop tor > /dev/null 2>&1", shell=True)
        out, err = process.communicate()
        return "Done"

    def start_tor(self):
        process = Popen("supervisorctl start tor > /dev/null 2>&1", shell=True)
        out, err = process.communicate()
        ret = False
        print("[>] Waiting on Tor..")
        for x in range(0, 10):
            with open('/var/log/tor_s.logs') as file:
                if 'Bootstrapped 100%: Done' in file.read():
                    ret = True
                    break
                else:
                    sleep(2)
        if not ret:
            return "Error"
        return "Done"

    def run(self):
        print("[>] Setup tor.. 1-6 {}".format(self.kill_tor()))
        print("[>] Setup tor.. 2-6 {}".format(self.delete_tor_file()))
        print("[>] Setup tor.. 3-6 {}".format(self.setuptor_new()))
        print("[>] Setup tor.. 4-6 {}".format(self.setup_resolve()))
        print("[>] Setup tor.. 5-6 {}".format(self.start_tor()))
        print("[>] Setup tor.. 6-6 {}".format(self.setup_iptables()))

#c = Connection("xuser","genmon-7","127.0.0.1","9051","pass")
# c.run()
