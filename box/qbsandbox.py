'''
    __G__ = "(G)bd249ce4"
    box -> sandbox
'''

from sys import argv
from json import loads, dump, dumps
from warnings import filterwarnings
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tinydb import TinyDB, Query
from binascii import hexlify
from bs4 import BeautifulSoup
from ssl import _ssl, get_server_certificate
from tempfile import mkstemp
from urllib.parse import urlparse
from requests import get as rget, head as rhead
from requests.packages.urllib3.connection import VerifiedHTTPSConnection
from socket import gethostbyname
from networkx import Graph, circular_layout
from io import BytesIO
from re import findall
from PIL import Image
from pytesseract import image_to_string
from dns.resolver import resolve
import matplotlib.pyplot as plt

filterwarnings("ignore", category=DeprecationWarning)
DISPLAY = Display(visible=0, size=(800, 600))
X509 = None


def get_dns(parsed, extracted_table):
    try:
        temp_list = []
        for records in ['A', 'AAAA', 'CNAME', 'MX', 'SRV', 'TXT', 'SOA', 'NS']:
            try:
                answer = resolve(parsed['domain'], records, raise_on_no_answer=False)
                if answer.rrset is not None:
                    temp_list.append({records: answer.rrset.to_text()})
            except BaseException:
                pass
        if len(temp_list) > 0:
            extracted_table.insert({'dns_records': temp_list})
    except Exception as e:
        print(e)
        print("[SandBox] get_dns failed")


def get_words(table, buffer):
    try:
        '''
        get words from page
        '''
        words_list = []
        image = Image.open(BytesIO(buffer))
        image = image.convert("RGBA")
        text = image_to_string(image, config='--psm 6')
        print(text)
        words_list = findall("[\x20-\x7e]{4,}", text)
        table.insert({'all_words': words_list})
        print("[SandBox] words saved")
    except BaseException:
        print("[SandBox] get_words failed")


#os.environ['DISPLAY'] = ':0'

def make_network(analyzer_table, network_graph):
    try:
        list_domain_counters = []
        dict_domain_counters = {}
        domain_counter = 0
        for item in analyzer_table.all():
            try:
                if 'headers' in item:
                    if 'Host' in item['headers']:
                        if item['headers']['Host'] not in list_domain_counters:
                            list_domain_counters.append(item['headers']['Host'])
                            dict_domain_counters.update({domain_counter: item['headers']['Host']})
                            domain_counter += 1
                    if ':authority' in item['headers']:
                        if item['headers'][':authority'] not in list_domain_counters:
                            list_domain_counters.append(item['headers'][':authority'])
                            dict_domain_counters.update({domain_counter: item['headers'][':authority']})
                            domain_counter += 1
            except BaseException:
                pass

        G = Graph()
        if len(list_domain_counters) > 0:
            for key, value in dict_domain_counters.items():
                G.add_node(key, text=value)
                if key != 0:
                    G.add_edge(0, key)

            pos = circular_layout(G)
            fig = plt.figure(figsize=(10, 5), facecolor='w')
            ax = fig.add_subplot(111)
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)

            for edges in G.edges:
                ax.annotate("",
                            xy=pos[edges[0]], xycoords='data',
                            xytext=pos[edges[1]], textcoords='data',
                            arrowprops=dict(arrowstyle='-', color="r", shrinkA=7, shrinkB=7, patchA=None, patchB=None, connectionstyle="arc3,rad=-0.1",),)
            for node in G:
                x, y = pos[node]
                ax.text(x, y, G.nodes[node]['text'], fontsize=10, bbox=dict(boxstyle='round', facecolor='#D3D3D3', alpha=1, linewidth=0), zorder=99)
            ax.axis('off')
            buf = BytesIO()
            plt.savefig(buf, bbox_inches='tight', dpi=100)
            buf.seek(0)
            network_graph.insert({'circular_layout': hexlify(buf.read()).decode('utf-8')})
            print("[SandBox] saved network graph")
    except BaseException:
        print("[SandBox] make_network failed")


def get_headers(parsed, extracted_table):
    try:
        response = None
        headers = {'User-Agent': parsed['useragent_mapped']}
        if parsed['use_proxy']:
            proxies = {'http': parsed['proxy'],
                       'https': parsed['proxy']}
            response = rhead(parsed['buffer'], proxies=proxies, headers=headers, timeout=2)
            response.headers['response_status'] = response.status_code
        else:
            response = rhead(parsed['buffer'], headers=headers, timeout=2)
            response.headers['response_status'] = response.status_code
        if len(response.headers) > 0:
            extracted_table.insert({'Request_Headers': dict(response.request.headers)})
            extracted_table.insert({'Response_Headers': dict(response.headers)})
            print("[SandBox] extracted request and response headers")
    except Exception as e:
        print("[SandBox] get_headers failed")


def get_cert(parsed, extracted_table):
    try:
        mapped = {b'CN': b'Common Name', b'OU': b'Organizational Unit', b'O': b'Organization', b'L': b'Locality', b'ST': b'State Or Province Name', b'C': b'Country Name'}
        original_connect = VerifiedHTTPSConnection.connect

        def hooked_connect(self):
            global X509
            original_connect(self)
            X509 = self.sock.connection.get_peer_certificate()
        VerifiedHTTPSConnection.connect = hooked_connect
        headers = {'User-Agent': parsed['useragent_mapped']}
        if parsed['use_proxy']:
            proxies = {'http': parsed['proxy'],
                       'https': parsed['proxy']}
            rget(parsed['buffer'], proxies=proxies, headers=headers, timeout=2)
        else:
            rget(parsed['buffer'], headers=headers, timeout=2)
        List_ = {}
        List_['Subjects'] = []
        for subject in X509.get_subject().get_components():
            try:
                List_['Subjects'].append({mapped[subject[0]].decode('utf-8'): subject[1].decode('utf-8')})
            except BaseException:
                pass
        List_['Subject Hash'] = X509.get_subject().hash()
        List_['Issuer'] = []
        for issuer in X509.get_issuer().get_components():
            try:
                List_['Issuer'].append({mapped[issuer[0]].decode('utf-8'): issuer[1].decode('utf-8')})
            except BaseException:
                pass
        List_['Issuer Hash'] = X509.get_issuer().hash()
        List_['Extensions'] = []
        for extension in range(X509.get_extension_count()):
            List_['Extensions'].append({X509.get_extension(extension).get_short_name().decode('utf-8'): X509.get_extension(extension).__str__()})
        List_['Expired'] = X509.has_expired()
        List_['Valid From'] = X509.get_notBefore().decode('utf-8')
        List_['Valid Until'] = X509.get_notAfter().decode('utf-8')
        List_['Signature Algorithm'] = X509.get_signature_algorithm().decode('utf-8')
        List_['Serial Number'] = X509.get_serial_number()
        List_['MD5 Digest'] = X509.digest('md5').decode('utf-8')
        List_['SHA1 Digest'] = X509.digest('sha1').decode('utf-8')
        List_['SHA224 Digest'] = X509.digest('sha224').decode('utf-8')
        List_['SHA256 Digest'] = X509.digest('sha256').decode('utf-8')
        List_['SHA384 Digest'] = X509.digest('sha384').decode('utf-8')
        List_['SHA512 Digest'] = X509.digest('sha512').decode('utf-8')
        extracted_table.insert({'Certificate': List_})
        print("[SandBox] extracted certificate")
    except BaseException:
        print("[SandBox] get_cert failed")


def get_all_links(html, extracted_table):
    try:
        temp_table = []
        parsed_table = []
        for a_tag in BeautifulSoup(html, 'html.parser').findAll("a"):
            try:
                temp_link = "{} > {}".format(a_tag['href'], a_tag.text)
                if temp_link not in temp_table:
                    temp_table.append(temp_link)
                    parsed_table.append({"link": a_tag['href'], "text": a_tag.text})
            except BaseException:
                pass
        if len(parsed_table) > 0:
            extracted_table.insert({"extracted_links": parsed_table})
            print("[SandBox] extracted links")
    except BaseException:
        print("[SandBox] get_all_links failed")


def get_all_scripts(html, extracted_table):
    try:
        temp_table = []
        parsed_table = []
        for script in BeautifulSoup(html, 'html.parser').findAll("script"):
            temp_link = "{}".format(script)
            if temp_link not in temp_table:
                temp_table.append(temp_link)
                try:
                    parsed_table.append({"script": str(script)})
                except BaseException:
                    pass
        if len(parsed_table) > 0:
            extracted_table.insert({"extracted_scripts": parsed_table})
            print("[SandBox] extracted scripts")
    except BaseException:
        print("[SandBox] get_all_links failed")


def take_normal_screen_shot(driver, screenshot_table, words_table):
    '''
    get normal screenshit
    '''
    try:
        screenshot = driver.get_screenshot_as_png()
        screenshot_table.insert({'normal_image': hexlify(screenshot).decode('utf-8')})
        print("[SandBox] Screenshot saved")
        # get_words(words_table,screenshot)
    except BaseException:
        print("[SandBox] take_normal_screen_shot failed")


def take_full_screen_shot(driver, screenshot_table, words_table):
    '''
    this function needs checking
    '''
    try:
        element = driver.find_element_by_tag_name('html')
        screenshot = element.get_screenshot_as_png()
        screenshot_table.insert({'full_image': hexlify(screenshot).decode('utf-8')})
        print("[SandBox] Screenshot saved")
        # get_words(words_table,screenshot)
    except BaseException:
        print("[SandBox] take_full_screen_shot failed")


def find_key(key, data):
    '''
    recursive key checking
    '''
    for k, v in data.items():
        if k == key:
            return v
        elif isinstance(v, list):
            for i in v:
                if isinstance(i, dict):
                    return find_key(key, i)
        elif isinstance(v, dict):
            return find_key(key, v)


def parse_ouput(logs, table):
    try:
        performance_events = [loads(e['message'])['message'] for e in logs]
        network_events = [e for e in performance_events if 'network.' in e['method'].lower()]
        #temp_list = [e for e in network_events if find_key("headers",e) is not None]
        temp_list = []
        for _ in network_events:
            rec = find_key("headers", _)
            if rec:
                if "Network.responseReceived" in _["method"]:
                    table.insert({"type": "Recvied", "headers": rec})
                elif "Network.requestWillBeSent" in _["method"]:
                    table.insert({"type": "Sent", "headers": rec})
        print("[SandBox] parsed output")
    except BaseException:
        print("[SandBox] parse_ouput failed")


def chrome_driver(parsed, analyzer_db):
    '''
    init webdriver and submit parsed options
    '''
    DISPLAY.start()
    analyzer_table = analyzer_db.table('analyzer_table')
    extracted_table = analyzer_db.table('extracted_table')
    screenshot_table = analyzer_db.table('screenshot_table')
    network_table = analyzer_db.table('network_table')
    words_table = analyzer_db.table('words_table')
    get_dns(parsed, extracted_table)
    get_headers(parsed, extracted_table)
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--user-agent={}'.format(parsed['useragent_mapped']))
    if parsed['use_proxy']:
        chrome_options.add_argument('--proxy-server=%s' % parsed['proxy'])
    chrome_options.binary_location = "/usr/bin/google-chrome"
    d = DesiredCapabilities.CHROME
    d["goog:loggingPrefs"] = {"performance": "ALL"}
    chromebrowser = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=d)
    if parsed["no_redirect"]:
        chromebrowser.implicitly_wait(0.1)
        try:
            chromebrowser.get(parsed["buffer"])
        except BaseException:
            pass
        # WebDriverWait(chromebrowser,1).until(EC.visibility_of_element_located((By.TAG_NAME,'body'))).send_keys(Keys.ESCAPE)
    else:
        chromebrowser.implicitly_wait(int(parsed["url_timeout"]))
        try:
            chromebrowser.get(parsed["buffer"])
        except BaseException:
            pass
    performance_logs = chromebrowser.get_log('performance')
    get_cert(parsed, extracted_table)
    get_all_links(chromebrowser.page_source, extracted_table)
    get_all_scripts(chromebrowser.page_source, extracted_table)
    if parsed['take_full_screenshot']:
        take_full_screen_shot(chromebrowser, screenshot_table, words_table)
    take_normal_screen_shot(chromebrowser, screenshot_table, words_table)
    parse_ouput(performance_logs, analyzer_table)
    make_network(analyzer_table, network_table)
    chromebrowser.quit()
    DISPLAY.stop()
    print("[SandBox] main logic done")
