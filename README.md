<p align="center"> <img src="https://raw.githubusercontent.com/qeeqbox/url-sandbox/master/readme/url-sandbox_.png"></p>

[![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/url-sandbox/master/info&label=version&query=$.version&colorB=blue&style=flat-square)](https://github.com/qeeqbox/url-sandbox/blob/master/changes.md)  [![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/url-sandbox/master/info&label=build&query=$.dockercomposebuild&colorB=green&style=flat-square)](https://github.com/qeeqbox/url-sandbox/blob/master/changes.md) [![Generic badge](https://img.shields.io/badge/dynamic/json.svg?url=https://raw.githubusercontent.com/qeeqbox/url-sandbox/master/info&label=test&query=$.automatedtest&colorB=green&style=flat-square)](https://github.com/qeeqbox/url-sandbox/blob/master/changes.md) [![Generic badge](https://img.shields.io/static/v1?label=%F0%9F%91%8D&message=!&color=yellow&style=flat-square)](https://github.com/qeeqbox/url-sandbox/stargazers)

URL Sandbox automate the daily task of analyzing URL or Domains internally without external resources' interaction. It contains a sandbox module that executes the target in an isolated environment (Customizable). The output from that environment is parsed and structured into useful categories. Some of those categories are visualized for better user experience. This project is scalable and can be integrated into your SOC.

## Install
```git clone https://github.com/qeeqbox/url-sandbox.git && cd url-sandbox && chmod +x run.sh && ./run.sh auto_configure```

## Interface
<img src="https://raw.githubusercontent.com/qeeqbox/url-sandbox/master/readme/intro.gif" style="max-width:768px"/>

## Features  
<ul>
<li>Runs locally</li>
<li>DNS info</li>
<li>Headers info</li>
<li>Brwoser info</li>
<li>Certifcate extraction</li>
<li>Target screenshot</li>
<li>Network graph image</li>
<li>Internal sniffer</li>
<li>Custom User Agent</li>
<li>Custom DNS and Proxy options</li>
<li>Auto Tor configuration</li>
<li>HTML and JSON output</li>
<li>No-redirect option</li>
</ul>

## Running
#### One click auto-configure
git clone https://github.com/qeeqbox/url-sandbox.git <br>
cd url-sandbox <br>
chmod +x run.sh <br>
./run.sh auto_configure <br>

The project interface http://127.0.0.1:8000/ will open automatically after finishing the initialization process

## Resources
`ChromeDriver - WebDriver for Chrome, Docker SDK`

## Other Licenses
By using this framework, you are accepting the license terms of all the following packages: `chromedriver, dnspython, docker, docker-compose, firefox-esr, flask, flask_admin, flask_bcrypt, flask_login, Flask-Markdown, flask_mongoengine, geckodriver, gevent, gunicorn, iptables, iptables-persistent, jinja2, jq, libleptonica-dev, libtesseract-dev, matplotlib, netifaces, net-tools, networkx, phantomjs, pymongo, pysocks, pytesseract, python-dateutil, python-magic, pyvirtualdisplay, requests[socks], scapy, selenium, supervisor, tcpdump, termcolor, tesseract, tldextract, unzip, urllib3, validator_collection, werkzeug, wget, xvfb, useragentstring`

## Disclaimer\Notes
- Do not deploy without proper configuration
- Setup some security group rules and remove default credentials

## Other Projects
[![](https://github.com/qeeqbox/.github/blob/main/data/social-analyzer.png)](https://github.com/qeeqbox/social-analyzer) [![](https://github.com/qeeqbox/.github/blob/main/data/analyzer.png)](https://github.com/qeeqbox/analyzer) [![](https://github.com/qeeqbox/.github/blob/main/data/chameleon.png)](https://github.com/qeeqbox/chameleon) [![](https://github.com/qeeqbox/.github/blob/main/data/honeypots.png)](https://github.com/qeeqbox/honeypots) [![](https://github.com/qeeqbox/.github/blob/main/data/mitre-visualizer.png)](https://github.com/qeeqbox/mitre-visualizer) [![](https://github.com/qeeqbox/.github/blob/main/data/woodpecker.png)](https://github.com/qeeqbox/woodpecker) [![](https://github.com/qeeqbox/.github/blob/main/data/docker-images.png)](https://github.com/qeeqbox/docker-images) [![](https://github.com/qeeqbox/.github/blob/main/data/seahorse.png)](https://github.com/qeeqbox/seahorse) [![](https://github.com/qeeqbox/.github/blob/main/data/rhino.png)](https://github.com/qeeqbox/rhino) [![](https://github.com/qeeqbox/.github/blob/main/data/raven.png)](https://github.com/qeeqbox/raven)
