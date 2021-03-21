'''
    __G__ = "(G)bd249ce4"
    web interface
'''

from os import environ, getpid, path
from uuid import uuid4
from re import search, DOTALL
from re import compile as rcompile
from random import choice
from datetime import timedelta, datetime
from json import JSONEncoder, dumps
from string import ascii_uppercase
from platform import platform as pplatform
from shutil import disk_usage
from requests import get
from psutil import cpu_percent, virtual_memory, Process
from bson.objectid import ObjectId
from flask import Flask, flash, jsonify, redirect, request, session, url_for
from flask_mongoengine import MongoEngine
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms import form, fields, validators, SelectMultipleField
from flask_admin import AdminIndexView, Admin, expose, BaseView
from flask_admin.menu import MenuLink
from flask_admin.babel import gettext
from flask_admin.contrib.mongoengine import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from flaskext.markdown import Markdown
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
from pymongo import ASCENDING
from redis import Redis
from celery import Celery
from bs4 import BeautifulSoup
from validator_collection import validators, checkers
from werkzeug.exceptions import HTTPException, default_exceptions
from shared.settings import defaultdb, json_settings, meta_files_settings, meta_reports_settings, meta_task_files_logs_settings, meta_users_settings, meta_task_logs_settings
from shared.logger import ignore_excpetion
from shared.mongodbconn import CLIENT, get_it_fs

SWITCHES = [('full_analysis', 'full analysis'), ('use_proxy', 'use proxy'), ('no_redirect', 'no redirect'), ('random_click', 'random click'), ('take_full_screenshot', 'full screenshot'), ('sniffer_on', 'turn sniffer on')]

SWITCHES_MAPPED = {
    '!Susie': '!Susie (http://www.sync2it.com/susie)',
    '008': 'Mozilla/5.0 (compatible; 008/0.83; http://www.80legs.com/webcrawler.html) Gecko/2008032620',
    'ABACHOBot': 'ABACHOBot',
    'ABrowse': 'Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)',
    'AOL': 'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)',
    'AbiLogicBot': 'Mozilla/5.0 (compatible; AbiLogicBot/1.0; +http://www.abilogic.com/bot.html)',
    'Accoona-AI-Agent': 'Accoona-AI-Agent/1.1.2 (aicrawler at accoonabot dot com)',
    'Acoo Browser': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
    'AddSugarSpiderBot': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
    'Amaya': 'amaya/11.3.1 libwww/5.4.1',
    'America Online Browser': 'Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)',
    'AmigaVoyager': 'AmigaVoyager/3.2 (AmigaOS/MC680x0)',
    'Android Webkit Browser': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'AnyApexBot': 'Mozilla/5.0 (compatible; AnyApexBot/1.0; +http://www.anyapex.com/bot.html)',
    'AppEngine-Google': 'AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)',
    'Arachmo': 'Mozilla/4.0 (compatible; Arachmo)',
    'Arora': 'Mozilla/5.0 (X11; U; UNICOS lcLinux; en-US) Gecko/20140730 (KHTML, like Gecko, Safari/419.3) Arora/0.8.0',
    'Avant Browser': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; Avant Browser; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    'B-l-i-t-z-B-O-T': 'Mozilla/4.0 (compatible; B-l-i-t-z-B-O-T)',
    'Baiduspider': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'BecomeBot': 'Mozilla/5.0 (compatible; BecomeBot/3.0; MSIE 6.0 compatible; +http://www.become.com/site_owners.html)',
    'Beonex': 'Mozilla/5.0 (Windows; U; WinNT; en; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable',
    'BeslistBot': 'Mozilla/5.0 (compatible; BeslistBot; nl; BeslistBot 1.0;  http://www.beslist.nl/',
    'BillyBobBot': 'BillyBobBot/1.0 (+http://www.billybobbot.com/crawler/)',
    'Bimbot': 'Bimbot/1.0',
    'BinGet': 'BinGet/1.00.A (http://www.bin-co.com/php/scripts/load/)',
    'Bingbot': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'BlackBerry': 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+',
    'Blazer': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows 95; PalmSource; Blazer 3.0) 16; 160x160',
    'BlitzBOT': 'Mozilla/4.0 (compatible; BlitzBot)',
    'Bloglines': 'Bloglines/3.1 (http://www.bloglines.com)',
    'Bolt': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; BOLT/2.340) AppleWebKit/530+ (KHTML, like Gecko) Version/4.0 Safari/530.17 UNTRUSTED/1.0 3gpp-gba',
    'BonEcho': 'Mozilla/5.0 (X11; U; Linux i686; nl; rv:1.8.1b2) Gecko/20060821 BonEcho/2.0b2 (Debian-1.99+2.0b2+dfsg-1)',
    'Browser for S60': 'SamsungI8910/SymbianOS/9.1 Series60/3.0',
    'Browzar': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Browzar)',
    'Bunjalloo': 'Bunjalloo/0.7.6(Nintendo DS;U;en)',
    'CSE HTML Validator': 'CSE HTML Validator Lite Online (http://online.htmlvalidator.com/php/onlinevallite.php)',
    'CSSCheck': 'CSSCheck/1.2.2',
    'Camino': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; XH; rv:8.578.498) fr, Gecko/20121021 Camino/8.723+ (Firefox compatible)',
    'CatchBot': 'CatchBot/2.0; +http://www.catchbot.com',
    'Cerberian Drtrs': 'Mozilla/4.0 (compatible; Cerberian Drtrs Version-3.2-Build-1)',
    'Charlotte': 'Mozilla/5.0 (compatible; Charlotte/1.1; http://www.searchme.com/support/)',
    'Charon': 'Mozilla/4.08 (Charon; Inferno)',
    'Cheshire': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko, Safari) Cheshire/1.0.UNOFFICIAL',
    'Chimera': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-PL; rv:1.0.1) Gecko/20021111 Chimera/0.6',
    'Chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'ChromePlus': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) ChromePlus/4.0.222.3 Chrome/4.0.222.3 Safari/532.2',
    'Classilla': 'Mozilla/5.0 (Macintosh; U; PPC; en-US; mimic; rv:9.3.0) Gecko/20120117 Firefox/3.6.25 Classilla/CFM',
    'Cocoal.icio.us': 'Cocoal.icio.us/1.0 (v43) (Mac OS X; http://www.scifihifi.com/cocoalicious)',
    'CometBird': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100409 Firefox/3.6.3 CometBird/3.6.3',
    'Comodo_Dragon': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7',
    'Conkeror': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0.11) Gecko/20100101 conkeror/1.0pre (Debian-1.0~~pre+git120527-1)',
    'ConveraCrawler': 'ConveraCrawler/0.9e (+http://ews.converasearch.com/crawl.htm)',
    'Covario IDS': 'Covario-IDS/1.0 (Covario; http://www.covario.com/ids; support at covario dot com)',
    'Crazy Browser': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; SV1; Crazy Browser 9.0.04)',
    'Cyberdog': 'Cyberdog/2.0 (Macintosh; PPC)',
    'Cynthia': 'Cynthia 1.0',
    'DataparkSearch': 'DataparkSearch/4.37-23012006 ( http://www.dataparksearch.org/)',
    'Deepnet Explorer': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; Deepnet Explorer 1.5.3; Smart 2x2; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'DeskBrowse': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-pl) AppleWebKit/312.8 (KHTML, like Gecko, Safari) DeskBrowse/1.0',
    'DiamondBot': 'DiamondBot',
    'Dillo': 'Dillo/2.0',
    'Discobot': 'Mozilla/5.0 (compatible; discobot/1.0; +http://discoveryengine.com/discobot.html)',
    'DomainsDB.net MetaCrawler': 'DomainsDB.net MetaCrawler v.0.9.7c (http://domainsdb.net/)',
    'Dooble': 'Dooble/0.07 (de_CH) WebKit',
    'Doris': 'Doris/1.15 [en] (Symbian)',
    'Dorothy': 'Mozilla/5.0 (Windows; U; Windows CE; Mobile; like iPhone; ko-kr) AppleWebKit/533.3 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.3 Dorothy',
    'Dotbot': 'Mozilla/5.0 (compatible; DotBot/1.1; http://www.dotnetdotcom.org/, crawler@dotnetdotcom.org)',
    'Edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Element Browser': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ (KHTML, like Gecko) Element Browser 5.0',
    'Elinks': 'ELinks/0.9.3 (textmode; Linux 2.6.9-kanotix-8 i686; 127x41)',
    'EmailSiphon': 'EmailSiphon',
    'EmeraldShield.com WebBot': 'EmeraldShield.com WebBot (http://www.emeraldshield.com/webbot.aspx)',
    'Enigma Browser': 'Enigma Browser',
    'EnigmaFox': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.0.13) Gecko/2009073022 EnigmaFox/3.0.13',
    'Epiphany': 'Mozilla/5.0 (X11; U; Linux x86_64; it-it) AppleWebKit/534.26+ (KHTML, like Gecko) Ubuntu/11.04 Epiphany/2.30.6',
    'Escape': 'Mozilla/4.0 (compatible; MSIE 5.23; Macintosh; PPC) Escape 5.1.8',
    'EsperanzaBot': 'EsperanzaBot(+http://www.esperanza.to/bot/)',
    'Exabot': 'Exabot/2.0',
    'FAST Enterprise Crawler': 'FAST Enterprise Crawler 6 used by Schibsted (webcrawl@schibstedsok.no)',
    'FAST-WebCrawler': 'FAST-WebCrawler/3.8 (atw-crawler at fast dot no; http://fast.no/support/crawler.asp)',
    'FDSE robot': 'Mozilla/4.0 (compatible: FDSE robot)',
    'FeedFetcher-Google': 'Feedfetcher-Google; (+http://www.google.com/feedfetcher.html; feed-id=8639390370582375869)',
    'Fennec': 'Mozilla/5.0 (Android; Linux armv7l; rv:9.0) Gecko/20111216 Firefox/9.0 Fennec/9.0',
    'FindLinks': 'findlinks/2.0.1 (+http://wortschatz.uni-leipzig.de/findlinks/)',
    'Firebird': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Firefox': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0',
    'Fireweb Navigator': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:2.0) Treco/20110515 Fireweb Navigator/2.4',
    'Flock': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Flock/3.5.3.4628 Chrome/7.0.517.450 Safari/534.7',
    'Fluid': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; nl-nl) AppleWebKit/532.3+ (KHTML, like Gecko) Fluid/0.9.6 Safari/532.3+',
    'FurlBot': 'Mozilla/4.0 compatible FurlBot/Furl Search 2.0 (FurlBot; http://www.furl.net; wn.furlbot@looksmart.net)',
    'FyberSpider': 'FyberSpider (+http://www.fybersearch.com/fyberspider.php)',
    'GSiteCrawler': 'GSiteCrawler/v1.20 rev. 273 (http://gsitecrawler.com/)',
    'Gaisbot': 'Gaisbot/3.0+(robot06@gais.cs.ccu.edu.tw;+http://gais.cs.ccu.edu.tw/robot.php)',
    'Galaxy': 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
    'GalaxyBot': 'GalaxyBot/1.0 (http://www.galaxy.com/galaxybot.html)',
    'Galeon': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko/20090327 Galeon/2.0.7',
    'Gigabot': 'Gigabot/3.0 (http://www.gigablast.com/spider.html)',
    'Girafabot': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322; Girafabot [girafa.com])',
    'Go Browser': 'NokiaE66/GoBrowser/2.0.297',
    'Googlebot': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Googlebot-Image': 'Googlebot-Image/1.0',
    'GranParadiso': 'Mozilla/5.0(X11;U;Linux(x86_64);en;rv:1.9a8)Gecko/2007100619;GranParadiso/3.1',
    'GreatNews': 'GreatNews/1.0',
    'GreenBrowser': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506; Media Center PC 5.0; .NET CLR 3.5.21022; GreenBrowser)',
    'Gregarius': 'Gregarius/0.5.2 (+http://devlog.gregarius.net/docs/ua)',
    'GurujiBot': 'Mozilla/5.0 GurujiBot/1.0 (+http://www.guruji.com/en/WebmasterFAQ.html)',
    'HTMLParser': 'HTMLParser/1.6',
    'Hana': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.9 (KHTML, like Gecko) Hana/1.1',
    'HappyFunBot': 'HappyFunBot/1.1 ( http://www.happyfunsearch.com/bot.html)',
    'Holmes': 'holmes/3.9 (someurl.co.cc)',
    'HotJava': 'HotJava/1.1.2 FCS',
    'IBM WebExplorer': 'IBM WebExplorer /v0.94',
    'IBrowse': 'Mozilla/5.0 (compatible; IBrowse 3.0; AmigaOS4.0)',
    'IE Mobile': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',
    'IRLbot': 'IRLbot/3.0 (compatible; MSIE 6.0; http://irl.cs.tamu.edu/crawler/)',
    'IceCat': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121201 icecat/17.0.1',
    'Iceape': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.13) Gecko/20100916 Iceape/2.0.8',
    'Iceweasel': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1',
    'Internet Explorer': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Iris': 'Mozilla/5.0 (Windows NT; U; en) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Iris/1.1.7 Safari/525.20',
    'Iron': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1250.0 Iron/22.0.2150.0 Safari/537.4',
    'IssueCrawler': 'IssueCrawler',
    'Java': 'Java/1.6.0_26',
    'Jaxified Bot': 'Jaxified Bot (+http://www.jaxified.com/crawler/)',
    'Jyxobot': 'Jyxobot/1',
    'K-Meleon': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.21pre) Gecko K-Meleon/1.7.0',
    'K-Ninja': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.4pre) Gecko/20070404 K-Ninja/2.1.3',
    'KKman': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; KKMAN3.2; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C)',
    'KMLite': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.19) Gecko/20081217 KMLite/1.1.2',
    'Kapiko': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.1) Gecko/20080722 Firefox/3.0.1 Kapiko/3.0',
    'Kazehakase': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.7) Gecko Kazehakase/0.5.6',
    'KoepaBot': 'Mozilla/5.0 (compatible; KoepaBot BETA; http://www.koepa.nl/bot.html)',
    'Konqueror': 'Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9',
    'L.webis': 'L.webis/0.87 (http://webalgo.iit.cnr.it/index.php?pg=lwebis)',
    'LDSpider': 'ldspider (http://code.google.com/p/ldspider/wiki/Robots)',
    'LapozzBot': 'LapozzBot/1.4 (+http://robot.lapozz.com)',
    'Larbin': 'Mozilla/5.0 larbin@unspecified.mail',
    'LeechCraft': 'Mozilla/5.0 (X11; U; Linux x86_64; ru-RU) AppleWebKit/533.3 (KHTML, like Gecko) Leechcraft/0.4.55-13-g2230d9f Safari/533.3',
    'LexxeBot': 'LexxeBot/1.0 (lexxebot@lexxe.com)',
    'Linguee Bot': 'Linguee Bot (http://www.linguee.com/bot; bot@linguee.com)',
    'Link Valet': 'Link Valet Online 1.1',
    'Link Validity Check': 'Link Validity Check From: http://www.w3dir.com/cgi-bin (Using: Hot Links SQL by Mrcgiguy.com)',
    'LinkExaminer': 'LinkExaminer/1.01 (Windows)',
    'LinkWalker': 'LinkWalker/2.0',
    'Links': 'Links (6.9; Unix 6.9-astral sparc; 80x25)',
    'LinksManager.com_bot': 'Mozilla/5.0 (compatible; LinksManager.com_bot  http://linksmanager.com/linkchecker.html)',
    'Lobo': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows XP 5.1) Lobo/0.98.4',
    'Lorentz': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3pre) Gecko/20100403 Lorentz/3.6.3plugin2pre (.NET CLR 4.0.20506)',
    'Lunascape': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.28) Gecko/20120410 Firefox/3.6.28 Lunascape/6.7.1.25446',
    'Lynx': 'Lynx/2.8.8dev.3 libwww-FM/2.14 SSL-MM/1.4.1',
    'MIB': 'MOT-L7/NA.ACR_RB MIB/2.2.1 Profile/MIDP-2.0 Configuration/CLDC-1.1',
    'MJ12bot': 'Mozilla/5.0 (compatible; MJ12bot/v1.2.4; http://www.majestic12.co.uk/bot.php?+)',
    'MSRBot': 'MSRBOT (http://research.microsoft.com/research/sv/msrbot/)',
    'MVAClient': 'MVAClient',
    'Madfox': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en; rv:1.7.12) Gecko/20050928 Firefox/1.0.7 Madfox/3.0',
    'Maemo Browser': 'Mozilla/5.0 (X11; U; Linux armv7l; ru-RU; rv:1.9.2.3pre) Gecko/20100723 Firefox/3.5 Maemo Browser 1.7.4.8 RX-51 N900',
    'MagpieRSS': 'MagpieRSS/0.7 ( http://magpierss.sf.net)',
    'Maxthon': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1',
    'Mediapartners-Google': 'Mediapartners-Google/2.1',
    'MetaURI': 'MetaURI API/2.0  metauri.com',
    'Microsoft URL Control': 'Microsoft URL Control - 6.01.9782',
    'Midori': 'Mozilla/5.0 (X11; U; Linux i686; fr-fr) AppleWebKit/525.1+ (KHTML, like Gecko, Safari/525.1+) midori/1.19',
    'Minefield': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre',
    'Minimo': 'Mozilla/5.0 (X11; U; Linux arm7tdmi; rv:1.8.1.11) Gecko/20071130 Minimo/0.025',
    'Mnogosearch': 'Mnogosearch-3.1.21',
    'MojeekBot': 'Mozilla/5.0 (compatible; MojeekBot/2.0; http://www.mojeek.com/bot.html)',
    'Mojoo Robot': 'Mojoo Robot (http://www.mojoo.com/)',
    'Moreoverbot': 'Moreoverbot/5.1 ( http://w.moreover.com; webmaster@moreover.com) Mozilla/5.0',
    'Morning Paper': 'Morning Paper 1.0 (robots.txt compliant!)',
    'Mozilla': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'MyIE2': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; MyIE2; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0)',
    'NCSA_Mosaic': 'NCSA Mosaic/3.0 (Windows 95)',
    'NFReader': 'NFReader/1.4.1.0 (http://www.gaijin.at/)',
    'NG-Search': 'NG-Search/0.9.8 (http://www.ng-search.com)',
    'Namoroka': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2a2pre) Gecko/20090908 Ubuntu/9.04 (jaunty) Namoroka/3.6a2pre GTB5 (.NET CLR 3.5.30729)',
    'Navscape': 'Mozilla/5.0 (X11; U; Linux i686; pt-BR) AppleWebKit/533.3 (KHTML, like Gecko) Navscape/Pre-0.2 Safari/533.3',
    'NetFront': 'SAMSUNG-C5212/C5212XDIK1 NetFront/3.4 Profile/MIDP-2.0 Configuration/CLDC-1.1',
    'NetNewsWire': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; de-de) AppleWebKit/531.22.7 (KHTML, like Gecko) NetNewsWire/3.2.7',
    'NetPositive': 'Mozilla/3.0 (compatible; NetPositive/2.2.2; BeOS)',
    'NetResearchServer': 'NetResearchServer/4.0(loopimprovements.com/robot.html)',
    'NetSeer Crawler': 'Mozilla/5.0 (compatible; NetSeer crawler/2.0; +http://www.netseer.com/crawler.html; crawler@netseer.com)',
    'NetSurf': 'NetSurf/2.0 (RISC OS; armv5l)',
    'Netscape': 'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
    'NewsGator': 'NewsGator/2.5 (http://www.newsgator.com; Microsoft Windows NT 5.1.2600.0; .NET  CLR 1.1.4322.2032)',
    'Nitro PDF': 'Nitro PDF Download',
    'Notifixious': 'Notifixious/LinkChecker (http://notifixio.us)',
    'Nusearch Spider': 'Nusearch Spider (www.nusearch.com)',
    'NutchCVS': 'NutchCVS/0.8-dev (Nutch; http://lucene.apache.org/nutch/bot.html; nutch-agent@lucene.apache.org)',
    'Nymesis': 'Nymesis/1.0 (http://nymesis.com)',
    'OOZBOT': 'OOZBOT/0.20 ( -- ; http://www.setooz.com/oozbot.html ; agentname at setooz dot_com )',
    'Offline Explorer': 'Offline Explorer/2.5',
    'OmniExplorer_Bot': 'OmniExplorer_Bot/6.70 (+http://www.omni-explorer.com) WorldIndexer',
    'OmniWeb': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941',
    'Opera': 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    'Opera Mini': 'Opera/9.80 (Android; Opera Mini/36.2.2254/119.132; U; id) Presto/2.12.423 Version/12.16)',
    'Opera Mobile': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02',
    'Orbiter': 'Orbiter (+http://www.dailyorbit.com/bot.htm)',
    'Orca': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.1.1) Gecko/20090722 Firefox/3.5.1 Orca/1.2 build 2',
    'Oregano': 'Mozilla/1.10 [en] (Compatible; RISC OS 3.70; Oregano 1.10)',
    'P3P Validator': 'P3P Validator',
    'PHP': 'PHP/5.2.9',
    'PageBitesHyperBot': 'PageBitesHyperBot/600 (http://www.pagebites.com/)',
    'Palemoon': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:25.6) Gecko/20150723 PaleMoon/25.6.0',
    'Peach': 'Peach/1.01 (Ubuntu 8.04 LTS; U; en)',
    'Peew': 'Mozilla/5.0 (compatible; Peew/1.0; http://www.peew.de/crawler/)',
    'Phoenix': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.3a) Gecko/20021207 Phoenix/0.5',
    'Playstation 3': 'Mozilla/5.0 (PLAYSTATION 3; 3.55)',
    'Playstation Portable': 'PSP (PlayStation Portable); 2.00',
    'Ploetz + Zeller': 'Ploetz + Zeller (http://www.ploetz-zeller.de) Link Validator v1.0 (support@p-und-z.de) for ARIS Business Architect',
    'Pogo': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.13) Gecko/20080414 Firefox/2.0.0.13 Pogo/2.0.0.13.6866',
    'Pompos': 'Pompos/1.3 http://dir.com/pompos.html',
    'PostPost': 'PostPost/1.0 (+http://postpo.st/crawlers)',
    'Prism': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.3) Gecko/20100402 Prism/1.0b4',
    'Psbot': 'psbot/0.1 (+http://www.picsearch.com/bot.html)',
    'PycURL': 'PycURL/7.23.1',
    'Python-urllib': 'Python-urllib/3.1',
    'Qseero': 'Qseero v1.0.0',
    'QtWeb Internet Browser': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/533.3 (KHTML, like Gecko)  QtWeb Internet Browser/3.7 http://www.QtWeb.net',
    'RAMPyBot': 'RAMPyBot - www.giveRAMP.com/0.1 (RAMPyBot - www.giveRAMP.com; http://www.giveramp.com/bot.html; support@giveRAMP.com)',
    'REL Link Checker Lite': 'REL Link Checker Lite 1.0',
    'Radian6': 'radian6_default_(www.radian6.com/crawler)',
    'Reciprocal Link System PRO': 'InfoWizards Reciprocal Link System PRO - (http://www.infowizards.com)',
    'Rekonq': 'Mozilla/5.0 (X11; U; Linux x86_64; cs-CZ) AppleWebKit/533.3 (KHTML, like Gecko) rekonq Safari/533.3',
    'RockMelt': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) RockMelt/0.9.58.494 Chrome/11.0.696.71 Safari/534.24',
    'RufusBot': 'RufusBot (Rufus Web Miner; http://64.124.122.252/feedback.html)',
    'SBIder': 'SBIder/0.8-dev (SBIder; http://www.sitesell.com/sbider.html; http://support.sitesell.com/contact-support.html)',
    'SEMC-Browser': 'SonyEricssonW800i/R1BD001/SEMC-Browser/4.2 Profile/MIDP-2.0 Configuration/CLDC-1.1',
    'SEOChat::Bot': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0) SEOChat::Bot v1.1',
    'Safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'SandCrawler': 'SandCrawler - Compatibility Testing',
    'ScoutJet': 'Mozilla/5.0 (compatible; ScoutJet;  http://www.scoutjet.com/)',
    'Scrubby': 'Scrubby/2.2 (http://www.scrubtheweb.com/)',
    'SeaMonkey': 'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre',
    'SearchSight': 'SearchSight/2.0 (http://SearchSight.com/)',
    'Seekbot': 'Seekbot/1.0 (http://www.seekbot.net/bot.html) RobotsTxtFetcher/1.2',
    'Sensis Web Crawler': 'Sensis Web Crawler (search_comments\\at\\sensis\\dot\\com\\dot\\au)',
    'SeznamBot': 'SeznamBot/2.0 (+http://fulltext.seznam.cz/)',
    'Shiira': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/419 (KHTML, like Gecko) Shiira/1.2.3 Safari/125',
    'Shim-Crawler': 'Shim-Crawler(Mozilla-compatible; http://www.logos.ic.i.u-tokyo.ac.jp/crawler/; crawl@logos.ic.i.u-tokyo.ac.jp)',
    'Shiretoko': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1b5pre) Gecko/20090424 Shiretoko/3.5b5pre',
    'ShopWiki': 'ShopWiki/1.0 ( +http://www.shopwiki.com/wiki/Help:Bot)',
    'Shoula robot': 'Mozilla/4.0 (compatible: Shoula robot)',
    'SiteBar': 'SiteBar/3.3.8 (Bookmark Server; http://sitebar.org/)',
    'Sitebot': 'Mozilla/5.0 (compatible; SiteBot/0.1; +http://www.sitebot.org/robot/)',
    'Skyfire': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_7; en-us) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Safari/530.17 Skyfire/2.0',
    'Sleipnir': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C; .NET4.0E; Sleipnir/2.9.9)',
    'SlimBrowser': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; SlimBrowser)',
    'Snappy': 'Snappy/1.1 ( http://www.urltrends.com/ )',
    'Snoopy': 'Snoopy v1.2',
    'Sosospider': 'Sosospider+(+http://help.soso.com/webspider.htm)',
    'Speedy Spider': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
    'Sqworm': 'Sqworm/2.9.85-BETA (beta_release; 20011115-775; i686-pc-linux-gnu)',
    'StackRambler': 'StackRambler/2.0 (MSIE incompatible)',
    'Stainless': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; en-us) AppleWebKit/528.16 (KHTML, like Gecko) Stainless/0.5.3 Safari/525.20.1',
    'Sundance': 'Sundance/0.9x(Compatible; Windows; U; en-US;)Version/0.9x',
    'Sunrise': 'Mozilla/6.0 (X11; U; Linux x86_64; en-US; rv:2.9.0.3) Gecko/2009022510 FreeBSD/ Sunrise/4.0.1/like Safari',
    'SuperBot': 'SuperBot/4.4.0.60 (Windows XP)',
    'SurveyBot': 'SurveyBot/2.3+(Whois+Source)',
    'Sylera': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.8.1.9) Gecko/20071110 Sylera/3.0.20 SeaMonkey/1.1.6',
    'SynooBot': 'SynooBot/0.7.1 (SynooBot; http://www.synoo.de/bot.html; webmaster@synoo.com)',
    'TeaShark': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3 TeaShark/0.8',
    'Teleca-Obigo': 'Mozilla/5.0 (compatible; Teleca Q7; Brew 3.1.5; U; en) 480X800 LGE VX11000',
    'TenFourFox': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10.5; rv:10.0.2) Gecko/20120216 Firefox/10.0.2 TenFourFox/7450',
    'Tencent Traveler': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; TencentTraveler 4.0; Trident/4.0; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
    'Teoma': 'Mozilla/2.0 (compatible; Ask Jeeves/Teoma; +http://sp.ask.com/docs/about/tech_crawling.html)',
    'TerrawizBot': 'TerrawizBot/1.0 (+http://www.terrawiz.com/bot.html)',
    'TheSuBot': 'TheSuBot/0.2 (www.thesubot.de)',
    'Thumbnail.CZ robot': 'Thumbnail.CZ robot 1.1 (http://thumbnail.cz/why-no-robots-txt.html)',
    'Thunderbird': 'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Thunderbird/38.2.0 Lightning/4.0.2',
    'TinEye': 'TinEye/1.1 (http://tineye.com/crawler.html)',
    'TurnitinBot': 'TurnitinBot/2.1 (http://www.turnitin.com/robot/crawlerinfo.html)',
    'TweetedTimes Bot': 'Mozilla/5.0 (compatible; TweetedTimes Bot/1.0;  http://tweetedtimes.com)',
    'TwengaBot': 'TwengaBot',
    'URD-MAGPIE': 'URD-MAGPIE/0.73 (Cached)',
    'UniversalFeedParser': 'UniversalFeedParser/3.3 +http://feedparser.org/',
    'Urlfilebot': 'Mozilla/5.0 (compatible; Urlfilebot/2.2; +http://urlfile.com/bot.html)',
    'VYU2': 'VYU2 (GNU; OpenRISC)',
    'Vagabondo': 'Mozilla/4.0 (compatible;  Vagabondo/4.0Beta; webcrawler at wise-guys dot nl; http://webagent.wise-guys.nl/; http://www.wise-guys.nl/)',
    'Vimprobable': 'Vimprobable/0.9.20.5',
    'Vivante Link Checker': 'Vivante Link Checker (http://www.vivante.com)',
    'VoilaBot': 'Mozilla/4.0 (compatible; MSIE 5.0; Windows 95) VoilaBot BETA 1.2 (http://www.voila.com/)',
    'Vonkeror': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1pre) Gecko/20090629 Vonkeror/1.0',
    'Vortex': 'Vortex/2.2 (+http://marty.anstey.ca/robots/vortex/)',
    'W3C-checklink': 'W3C-checklink/4.5 [4.160] libwww-perl/5.823',
    'W3C_CSS_Validator_JFouffa': 'Jigsaw/2.2.5 W3C_CSS_Validator_JFouffa/2.0',
    'W3C_Validator': 'W3C_Validator/1.654',
    'WDG_Validator': 'WDG_Validator/1.6.2',
    'Web Downloader': 'Web Downloader/6.9',
    'WebCapture': 'Mozilla/4.0 (compatible; WebCapture 3.0; Windows)',
    'WebCopier': 'WebCopier v4.6',
    'WebZIP': 'WebZIP/3.5 (http://www.spidersoft.com)',
    'Websquash.com': 'Websquash.com (Add url robot)',
    'WeltweitimnetzBrowser': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR) AppleWebKit/534.12 (KHTML, like Gecko) WeltweitimnetzBrowser/0.25 Safari/534.12',
    'Wget': 'Wget/1.9+cvs-stable (Red Hat modified)',
    'Wii': 'wii libnup/1.0',
    'Windows-Media-Player': 'Windows-Media-Player/11.0.5721.5145',
    'WoFindeIch Robot': 'WoFindeIch Robot 1.0(+http://www.search.wofindeich.com/robot.php)',
    'WomlpeFactory': 'WomlpeFactory/0.1 (+http://www.Womple.com/bot.html)',
    'WorldWideWeb': 'WorldWideweb (NEXT)',
    'Wyzo': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20100121 Firefox/3.5.6 Wyzo/3.5.6.1',
    'Xaldon_WebSpider': 'Xaldon_WebSpider/2.0.b1',
    'Xenu Link Sleuth': 'Xenu Link Sleuth 1.2i',
    'Yahoo! Slurp': 'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Yahoo! Slurp China': 'Mozilla/5.0 (compatible; Yahoo! Slurp China; http://misc.yahoo.com.cn/help.html)',
    'YahooSeeker': 'YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)',
    'YahooSeeker-Testing': 'YahooSeeker-Testing/v3.9 (compatible; Mozilla 4.0; MSIE 5.5; http://search.yahoo.com/)',
    'YandexBot': 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'YandexImages': 'Mozilla/5.0 (compatible; YandexImages/3.0; +http://yandex.com/bots)',
    'Yasaklibot': 'Yasaklibot/v1.2 (http://www.Yasakli.com/bot.php)',
    'Yeti': 'Yeti/1.0 (NHN Corp.; http://help.naver.com/robots/)',
    'YodaoBot': 'Mozilla/5.0 (compatible; YodaoBot/1.0; http://www.yodao.com/help/webmaster/spider/; )',
    'YoudaoBot': 'Mozilla/5.0 (compatible; YoudaoBot/1.0; http://www.youdao.com/help/webmaster/spider/; )',
    'Zao': 'Zao/0.1 (http://www.kototoi.org/zao/)',
    'Zealbot': 'Mozilla/4.0 (compatible; Zealbot 1.0)',
    'ZyBorg': 'Mozilla/4.0 compatible ZyBorg/1.0 DLC (wn.zyborg@looksmart.net; http://www.WISEnutbot.com)',
    'boitho.com-dc': 'boitho.com-dc/0.85 ( http://www.boitho.com/dcbot.html )',
    'boitho.com-robot': 'boitho.com-robot/1.1',
    'btbot': 'btbot/0.4 (+http://www.btbot.com/btbot.html)',
    'cURL': 'curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)',
    'cosmos': 'cosmos/0.9_(robot@xyleme.com)',
    'envolk[ITS]spider': 'envolk[ITS]spider/1.6 (+http://www.envolk.com/envolkspider.html)',
    'everyfeed-spider': 'everyfeed-spider/2.0 (http://www.everyfeed.com)',
    'g2crawler': 'g2Crawler nobody@airmail.net',
    'genieBot': 'genieBot (http://64.5.245.11/faq/faq.html)',
    'hl_ftien_spider': 'hl_ftien_spider_v1.1',
    'htdig': 'htdig/3.1.6 (unconfigured@htdig.searchengine.maintainer)',
    'iCCrawler': 'iCCrawler (http://www.iccenter.net/bot.htm)',
    'iCab': 'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_8) AppleWebKit/537.3+ (KHTML, like Gecko) iCab/5.0 Safari/533.16',
    'iNet Browser': 'Mozilla/5.0 (Future Star Technologies Corp.; Star-Blade OS; x86_64; U; en-US) iNet Browser 4.7',
    'iRider': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; iRider 2.60.0008; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
    'iTunes': 'iTunes/9.1.1',
    'ia_archiver': 'ia_archiver/8.9 (Windows NT 3.1; en-US;)',
    'iaskspider': 'iaskspider/2.0(+http://iask.com/help/help_index.html)',
    'ichiro': 'ichiro/4.0 (http://help.goo.ne.jp/door/crawler.html)',
    'igdeSpyder': 'igdeSpyder (compatible; igde.ru; +http://igde.ru/doc/tech.html)',
    'lftp': 'lftp/4.3.8',
    'libwww-perl': 'libwww-perl/5.821',
    'lmspider': 'lmspider lmspider@scansoft.com',
    'lolifox': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2) Gecko/20070225 lolifox/0.32',
    'lwp-trivial': 'lwp-trivial/1.41',
    'mabontland': 'http://www.mabontland.com',
    'magpie-crawler': 'magpie-crawler/1.1 (U; Linux amd64; en-GB; +http://www.brandwatch.net)',
    'mogimogi': 'mogimogi/1.0',
    'msnbot': 'msnbot/2.1',
    'mxbot': 'Mozilla/5.0 (compatible; mxbot/1.0; +http://www.chainn.com/mxbot.html)',
    'myibrow': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; cs; rv:1.9.2.6) Gecko/20100628 myibrow/4alpha2',
    'nicebot': 'nicebot',
    'noxtrumbot': 'noxtrumbot/1.0 (crawler@noxtrum.com)',
    'obot': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 4.0; obot)',
    'oegp': 'oegp v. 1.3.0',
    'omgilibot': 'omgilibot/0.4 +http://omgili.com',
    'online link validator': 'online link validator (http://www.dead-links.com/)',
    'osb-browser': 'Mozilla/5.0 (X11; U; Linux i686; en-us) AppleWebKit/146.1 (KHTML, like Gecko) osb-browser/0.5',
    'polybot': 'polybot 1.0 (http://cis.poly.edu/polybot/)',
    'pxyscand': 'pxyscand/2.1',
    'retawq': 'retawq/0.2.6c [en] (text)',
    'semanticdiscovery': 'semanticdiscovery/0.1',
    'silk': 'silk/1.0 (+http://www.slider.com/silk.htm)/3.7',
    'sogou spider': 'sogou spider',
    'suggybot': 'Mozilla/5.0 (compatible; suggybot v0.01a, http://blog.suggy.com/was-ist-suggy/suggy-webcrawler/)',
    'surf': 'Surf/0.4.1 (X11; U; Unix; en-US) AppleWebKit/531.2+ Compatible (Safari; MSIE 9.0)',
    'theWorld Browser': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)',
    'truwoGPS': 'truwoGPS/1.0 (GNU/Linux; U; i686; en-US; +http://www.lan4lano.net/browser.html )',
    'uZard Web': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; WOW64; Trident/4.0; uZardWeb/1.0; Server_USA)',
    'updated': 'updated/0.1-beta (updated; http://www.updated.com; updated@updated.com)',
    'uzbl': 'Uzbl (Webkit 1.3) (Linux i686 [i686])',
    'voyager': 'voyager/2.0 (http://www.kosmix.com/crawler.html)',
    'w3m': 'w3m/0.52',
    'webcollage': 'webcollage/1.93',
    'wf84': 'http://www.almaden.ibm.com/cs/crawler   [wf84]',
    'yacy': 'yacybot (x86 Windows XP 5.1; java 1.6.0_12; Europe/de) http://yacy.net/bot.html',
    'yoogliFetchAgent': 'yoogliFetchAgent/0.1',
    'zspider': 'zspider/0.9-dev http://feedback.redkolibri.com/'}

USERAGENTS = [
    ('!Susie',
     '!Susie'),
    ('008',
     '008'),
    ('ABACHOBot',
     'ABACHOBot'),
    ('ABrowse',
     'ABrowse'),
    ('AOL',
     'AOL'),
    ('AbiLogicBot',
     'AbiLogicBot'),
    ('Accoona-AI-Agent',
     'Accoona-AI-Agent'),
    ('Acoo Browser',
     'Acoo Browser'),
    ('AddSugarSpiderBot',
     'AddSugarSpiderBot'),
    ('Amaya',
     'Amaya'),
    ('America Online Browser',
     'America Online Browser'),
    ('AmigaVoyager',
     'AmigaVoyager'),
    ('Android Webkit Browser',
     'Android Webkit Browser'),
    ('AnyApexBot',
     'AnyApexBot'),
    ('AppEngine-Google',
     'AppEngine-Google'),
    ('Arachmo',
     'Arachmo'),
    ('Arora',
     'Arora'),
    ('Avant Browser',
     'Avant Browser'),
    ('B-l-i-t-z-B-O-T',
     'B-l-i-t-z-B-O-T'),
    ('Baiduspider',
     'Baiduspider'),
    ('BecomeBot',
     'BecomeBot'),
    ('Beonex',
     'Beonex'),
    ('BeslistBot',
     'BeslistBot'),
    ('BillyBobBot',
     'BillyBobBot'),
    ('Bimbot',
     'Bimbot'),
    ('BinGet',
     'BinGet'),
    ('Bingbot',
     'Bingbot'),
    ('BlackBerry',
     'BlackBerry'),
    ('Blazer',
     'Blazer'),
    ('BlitzBOT',
     'BlitzBOT'),
    ('Bloglines',
     'Bloglines'),
    ('Bolt',
     'Bolt'),
    ('BonEcho',
     'BonEcho'),
    ('Browser for S60',
     'Browser for S60'),
    ('Browzar',
     'Browzar'),
    ('Bunjalloo',
     'Bunjalloo'),
    ('CSE HTML Validator',
     'CSE HTML Validator'),
    ('CSSCheck',
     'CSSCheck'),
    ('Camino',
     'Camino'),
    ('CatchBot',
     'CatchBot'),
    ('Cerberian Drtrs',
     'Cerberian Drtrs'),
    ('Charlotte',
     'Charlotte'),
    ('Charon',
     'Charon'),
    ('Cheshire',
     'Cheshire'),
    ('Chimera',
     'Chimera'),
    ('Chrome',
     'Chrome'),
    ('ChromePlus',
     'ChromePlus'),
    ('Classilla',
     'Classilla'),
    ('Cocoal.icio.us',
     'Cocoal.icio.us'),
    ('CometBird',
     'CometBird'),
    ('Comodo_Dragon',
     'Comodo_Dragon'),
    ('Conkeror',
     'Conkeror'),
    ('ConveraCrawler',
     'ConveraCrawler'),
    ('Covario IDS',
     'Covario IDS'),
    ('Crazy Browser',
     'Crazy Browser'),
    ('Cyberdog',
     'Cyberdog'),
    ('Cynthia',
     'Cynthia'),
    ('DataparkSearch',
     'DataparkSearch'),
    ('Deepnet Explorer',
     'Deepnet Explorer'),
    ('DeskBrowse',
     'DeskBrowse'),
    ('DiamondBot',
     'DiamondBot'),
    ('Dillo',
     'Dillo'),
    ('Discobot',
     'Discobot'),
    ('DomainsDB.net MetaCrawler',
     'DomainsDB.net MetaCrawler'),
    ('Dooble',
     'Dooble'),
    ('Doris',
     'Doris'),
    ('Dorothy',
     'Dorothy'),
    ('Dotbot',
     'Dotbot'),
    ('Edge',
     'Edge'),
    ('Element Browser',
     'Element Browser'),
    ('Elinks',
     'Elinks'),
    ('EmailSiphon',
     'EmailSiphon'),
    ('EmeraldShield.com WebBot',
     'EmeraldShield.com WebBot'),
    ('Enigma Browser',
     'Enigma Browser'),
    ('EnigmaFox',
     'EnigmaFox'),
    ('Epiphany',
     'Epiphany'),
    ('Escape',
     'Escape'),
    ('EsperanzaBot',
     'EsperanzaBot'),
    ('Exabot',
     'Exabot'),
    ('FAST Enterprise Crawler',
     'FAST Enterprise Crawler'),
    ('FAST-WebCrawler',
     'FAST-WebCrawler'),
    ('FDSE robot',
     'FDSE robot'),
    ('FeedFetcher-Google',
     'FeedFetcher-Google'),
    ('Fennec',
     'Fennec'),
    ('FindLinks',
     'FindLinks'),
    ('Firebird',
     'Firebird'),
    ('Firefox',
     'Firefox'),
    ('Fireweb Navigator',
     'Fireweb Navigator'),
    ('Flock',
     'Flock'),
    ('Fluid',
     'Fluid'),
    ('FurlBot',
     'FurlBot'),
    ('FyberSpider',
     'FyberSpider'),
    ('GSiteCrawler',
     'GSiteCrawler'),
    ('Gaisbot',
     'Gaisbot'),
    ('Galaxy',
     'Galaxy'),
    ('GalaxyBot',
     'GalaxyBot'),
    ('Galeon',
     'Galeon'),
    ('Gigabot',
     'Gigabot'),
    ('Girafabot',
     'Girafabot'),
    ('Go Browser',
     'Go Browser'),
    ('Googlebot',
     'Googlebot'),
    ('Googlebot-Image',
     'Googlebot-Image'),
    ('GranParadiso',
     'GranParadiso'),
    ('GreatNews',
     'GreatNews'),
    ('GreenBrowser',
     'GreenBrowser'),
    ('Gregarius',
     'Gregarius'),
    ('GurujiBot',
     'GurujiBot'),
    ('HTMLParser',
     'HTMLParser'),
    ('Hana',
     'Hana'),
    ('HappyFunBot',
     'HappyFunBot'),
    ('Holmes',
     'Holmes'),
    ('HotJava',
     'HotJava'),
    ('IBM WebExplorer',
     'IBM WebExplorer'),
    ('IBrowse',
     'IBrowse'),
    ('IE Mobile',
     'IE Mobile'),
    ('IRLbot',
     'IRLbot'),
    ('IceCat',
     'IceCat'),
    ('Iceape',
     'Iceape'),
    ('Iceweasel',
     'Iceweasel'),
    ('Internet Explorer',
     'Internet Explorer'),
    ('Iris',
     'Iris'),
    ('Iron',
     'Iron'),
    ('IssueCrawler',
     'IssueCrawler'),
    ('Java',
     'Java'),
    ('Jaxified Bot',
     'Jaxified Bot'),
    ('Jyxobot',
     'Jyxobot'),
    ('K-Meleon',
     'K-Meleon'),
    ('K-Ninja',
     'K-Ninja'),
    ('KKman',
     'KKman'),
    ('KMLite',
     'KMLite'),
    ('Kapiko',
     'Kapiko'),
    ('Kazehakase',
     'Kazehakase'),
    ('KoepaBot',
     'KoepaBot'),
    ('Konqueror',
     'Konqueror'),
    ('L.webis',
     'L.webis'),
    ('LDSpider',
     'LDSpider'),
    ('LapozzBot',
     'LapozzBot'),
    ('Larbin',
     'Larbin'),
    ('LeechCraft',
     'LeechCraft'),
    ('LexxeBot',
     'LexxeBot'),
    ('Linguee Bot',
     'Linguee Bot'),
    ('Link Valet',
     'Link Valet'),
    ('Link Validity Check',
     'Link Validity Check'),
    ('LinkExaminer',
     'LinkExaminer'),
    ('LinkWalker',
     'LinkWalker'),
    ('Links',
     'Links'),
    ('LinksManager.com_bot',
     'LinksManager.com_bot'),
    ('Lobo',
     'Lobo'),
    ('Lorentz',
     'Lorentz'),
    ('Lunascape',
     'Lunascape'),
    ('Lynx',
     'Lynx'),
    ('MIB',
     'MIB'),
    ('MJ12bot',
     'MJ12bot'),
    ('MSRBot',
     'MSRBot'),
    ('MVAClient',
     'MVAClient'),
    ('Madfox',
     'Madfox'),
    ('Maemo Browser',
     'Maemo Browser'),
    ('MagpieRSS',
     'MagpieRSS'),
    ('Maxthon',
     'Maxthon'),
    ('Mediapartners-Google',
     'Mediapartners-Google'),
    ('MetaURI',
     'MetaURI'),
    ('Microsoft URL Control',
     'Microsoft URL Control'),
    ('Midori',
     'Midori'),
    ('Minefield',
     'Minefield'),
    ('Minimo',
     'Minimo'),
    ('Mnogosearch',
     'Mnogosearch'),
    ('MojeekBot',
     'MojeekBot'),
    ('Mojoo Robot',
     'Mojoo Robot'),
    ('Moreoverbot',
     'Moreoverbot'),
    ('Morning Paper',
     'Morning Paper'),
    ('Mozilla',
     'Mozilla'),
    ('MyIE2',
     'MyIE2'),
    ('NCSA_Mosaic',
     'NCSA_Mosaic'),
    ('NFReader',
     'NFReader'),
    ('NG-Search',
     'NG-Search'),
    ('Namoroka',
     'Namoroka'),
    ('Navscape',
     'Navscape'),
    ('NetFront',
     'NetFront'),
    ('NetNewsWire',
     'NetNewsWire'),
    ('NetPositive',
     'NetPositive'),
    ('NetResearchServer',
     'NetResearchServer'),
    ('NetSeer Crawler',
     'NetSeer Crawler'),
    ('NetSurf',
     'NetSurf'),
    ('Netscape',
     'Netscape'),
    ('NewsGator',
     'NewsGator'),
    ('Nitro PDF',
     'Nitro PDF'),
    ('Notifixious',
     'Notifixious'),
    ('Nusearch Spider',
     'Nusearch Spider'),
    ('NutchCVS',
     'NutchCVS'),
    ('Nymesis',
     'Nymesis'),
    ('OOZBOT',
     'OOZBOT'),
    ('Offline Explorer',
     'Offline Explorer'),
    ('OmniExplorer_Bot',
     'OmniExplorer_Bot'),
    ('OmniWeb',
     'OmniWeb'),
    ('Opera',
     'Opera'),
    ('Opera Mini',
     'Opera Mini'),
    ('Opera Mobile',
     'Opera Mobile'),
    ('Orbiter',
     'Orbiter'),
    ('Orca',
     'Orca'),
    ('Oregano',
     'Oregano'),
    ('P3P Validator',
     'P3P Validator'),
    ('PHP',
     'PHP'),
    ('PageBitesHyperBot',
     'PageBitesHyperBot'),
    ('Palemoon',
     'Palemoon'),
    ('Peach',
     'Peach'),
    ('Peew',
     'Peew'),
    ('Phoenix',
     'Phoenix'),
    ('Playstation 3',
     'Playstation 3'),
    ('Playstation Portable',
     'Playstation Portable'),
    ('Ploetz + Zeller',
     'Ploetz + Zeller'),
    ('Pogo',
     'Pogo'),
    ('Pompos',
     'Pompos'),
    ('PostPost',
     'PostPost'),
    ('Prism',
     'Prism'),
    ('Psbot',
     'Psbot'),
    ('PycURL',
     'PycURL'),
    ('Python-urllib',
     'Python-urllib'),
    ('Qseero',
     'Qseero'),
    ('QtWeb Internet Browser',
     'QtWeb Internet Browser'),
    ('RAMPyBot',
     'RAMPyBot'),
    ('REL Link Checker Lite',
     'REL Link Checker Lite'),
    ('Radian6',
     'Radian6'),
    ('Reciprocal Link System PRO',
     'Reciprocal Link System PRO'),
    ('Rekonq',
     'Rekonq'),
    ('RockMelt',
     'RockMelt'),
    ('RufusBot',
     'RufusBot'),
    ('SBIder',
     'SBIder'),
    ('SEMC-Browser',
     'SEMC-Browser'),
    ('SEOChat::Bot',
     'SEOChat::Bot'),
    ('Safari',
     'Safari'),
    ('SandCrawler',
     'SandCrawler'),
    ('ScoutJet',
     'ScoutJet'),
    ('Scrubby',
     'Scrubby'),
    ('SeaMonkey',
     'SeaMonkey'),
    ('SearchSight',
     'SearchSight'),
    ('Seekbot',
     'Seekbot'),
    ('Sensis Web Crawler',
     'Sensis Web Crawler'),
    ('SeznamBot',
     'SeznamBot'),
    ('Shiira',
     'Shiira'),
    ('Shim-Crawler',
     'Shim-Crawler'),
    ('Shiretoko',
     'Shiretoko'),
    ('ShopWiki',
     'ShopWiki'),
    ('Shoula robot',
     'Shoula robot'),
    ('SiteBar',
     'SiteBar'),
    ('Sitebot',
     'Sitebot'),
    ('Skyfire',
     'Skyfire'),
    ('Sleipnir',
     'Sleipnir'),
    ('SlimBrowser',
     'SlimBrowser'),
    ('Snappy',
     'Snappy'),
    ('Snoopy',
     'Snoopy'),
    ('Sosospider',
     'Sosospider'),
    ('Speedy Spider',
     'Speedy Spider'),
    ('Sqworm',
     'Sqworm'),
    ('StackRambler',
     'StackRambler'),
    ('Stainless',
     'Stainless'),
    ('Sundance',
     'Sundance'),
    ('Sunrise',
     'Sunrise'),
    ('SuperBot',
     'SuperBot'),
    ('SurveyBot',
     'SurveyBot'),
    ('Sylera',
     'Sylera'),
    ('SynooBot',
     'SynooBot'),
    ('TeaShark',
     'TeaShark'),
    ('Teleca-Obigo',
     'Teleca-Obigo'),
    ('TenFourFox',
     'TenFourFox'),
    ('Tencent Traveler',
     'Tencent Traveler'),
    ('Teoma',
     'Teoma'),
    ('TerrawizBot',
     'TerrawizBot'),
    ('TheSuBot',
     'TheSuBot'),
    ('Thumbnail.CZ robot',
     'Thumbnail.CZ robot'),
    ('Thunderbird',
     'Thunderbird'),
    ('TinEye',
     'TinEye'),
    ('TurnitinBot',
     'TurnitinBot'),
    ('TweetedTimes Bot',
     'TweetedTimes Bot'),
    ('TwengaBot',
     'TwengaBot'),
    ('URD-MAGPIE',
     'URD-MAGPIE'),
    ('UniversalFeedParser',
     'UniversalFeedParser'),
    ('Urlfilebot',
     'Urlfilebot'),
    ('VYU2',
     'VYU2'),
    ('Vagabondo',
     'Vagabondo'),
    ('Vimprobable',
     'Vimprobable'),
    ('Vivante Link Checker',
     'Vivante Link Checker'),
    ('VoilaBot',
     'VoilaBot'),
    ('Vonkeror',
     'Vonkeror'),
    ('Vortex',
     'Vortex'),
    ('W3C-checklink',
     'W3C-checklink'),
    ('W3C_CSS_Validator_JFouffa',
     'W3C_CSS_Validator_JFouffa'),
    ('W3C_Validator',
     'W3C_Validator'),
    ('WDG_Validator',
     'WDG_Validator'),
    ('Web Downloader',
     'Web Downloader'),
    ('WebCapture',
     'WebCapture'),
    ('WebCopier',
     'WebCopier'),
    ('WebZIP',
     'WebZIP'),
    ('Websquash.com',
     'Websquash.com'),
    ('WeltweitimnetzBrowser',
     'WeltweitimnetzBrowser'),
    ('Wget',
     'Wget'),
    ('Wii',
     'Wii'),
    ('Windows-Media-Player',
     'Windows-Media-Player'),
    ('WoFindeIch Robot',
     'WoFindeIch Robot'),
    ('WomlpeFactory',
     'WomlpeFactory'),
    ('WorldWideWeb',
     'WorldWideWeb'),
    ('Wyzo',
     'Wyzo'),
    ('Xaldon_WebSpider',
     'Xaldon_WebSpider'),
    ('Xenu Link Sleuth',
     'Xenu Link Sleuth'),
    ('Yahoo! Slurp',
     'Yahoo! Slurp'),
    ('Yahoo! Slurp China',
     'Yahoo! Slurp China'),
    ('YahooSeeker',
     'YahooSeeker'),
    ('YahooSeeker-Testing',
     'YahooSeeker-Testing'),
    ('YandexBot',
     'YandexBot'),
    ('YandexImages',
     'YandexImages'),
    ('Yasaklibot',
     'Yasaklibot'),
    ('Yeti',
     'Yeti'),
    ('YodaoBot',
     'YodaoBot'),
    ('YoudaoBot',
     'YoudaoBot'),
    ('Zao',
     'Zao'),
    ('Zealbot',
     'Zealbot'),
    ('ZyBorg',
     'ZyBorg'),
    ('boitho.com-dc',
     'boitho.com-dc'),
    ('boitho.com-robot',
     'boitho.com-robot'),
    ('btbot',
     'btbot'),
    ('cURL',
     'cURL'),
    ('cosmos',
     'cosmos'),
    ('envolk[ITS]spider',
     'envolk[ITS]spider'),
    ('everyfeed-spider',
     'everyfeed-spider'),
    ('g2crawler',
     'g2crawler'),
    ('genieBot',
     'genieBot'),
    ('hl_ftien_spider',
     'hl_ftien_spider'),
    ('htdig',
     'htdig'),
    ('iCCrawler',
     'iCCrawler'),
    ('iCab',
     'iCab'),
    ('iNet Browser',
     'iNet Browser'),
    ('iRider',
     'iRider'),
    ('iTunes',
     'iTunes'),
    ('ia_archiver',
     'ia_archiver'),
    ('iaskspider',
     'iaskspider'),
    ('ichiro',
     'ichiro'),
    ('igdeSpyder',
     'igdeSpyder'),
    ('lftp',
     'lftp'),
    ('libwww-perl',
     'libwww-perl'),
    ('lmspider',
     'lmspider'),
    ('lolifox',
     'lolifox'),
    ('lwp-trivial',
     'lwp-trivial'),
    ('mabontland',
     'mabontland'),
    ('magpie-crawler',
     'magpie-crawler'),
    ('mogimogi',
     'mogimogi'),
    ('msnbot',
     'msnbot'),
    ('mxbot',
     'mxbot'),
    ('myibrow',
     'myibrow'),
    ('nicebot',
     'nicebot'),
    ('noxtrumbot',
     'noxtrumbot'),
    ('obot',
     'obot'),
    ('oegp',
     'oegp'),
    ('omgilibot',
     'omgilibot'),
    ('online link validator',
     'online link validator'),
    ('osb-browser',
     'osb-browser'),
    ('polybot',
     'polybot'),
    ('pxyscand',
     'pxyscand'),
    ('retawq',
     'retawq'),
    ('semanticdiscovery',
     'semanticdiscovery'),
    ('silk',
     'silk'),
    ('sogou spider',
     'sogou spider'),
    ('suggybot',
     'suggybot'),
    ('surf',
     'surf'),
    ('theWorld Browser',
     'theWorld Browser'),
    ('truwoGPS',
     'truwoGPS'),
    ('uZard Web',
     'uZard Web'),
    ('updated',
     'updated'),
    ('uzbl',
     'uzbl'),
    ('voyager',
     'voyager'),
    ('w3m',
     'w3m'),
    ('webcollage',
     'webcollage'),
    ('wf84',
     'wf84'),
    ('yacy',
     'yacy'),
    ('yoogliFetchAgent',
     'yoogliFetchAgent'),
    ('zspider',
     'zspider')]

APP = Flask(__name__)
APP.secret_key = json_settings[environ["project_env"]]["backend_key"]
APP.config['MONGODB_SETTINGS'] = json_settings[environ["project_env"]]["web_mongo"]
APP.config['SESSION_COOKIE_SAMESITE'] = "Lax"
ANALYZER_TIMEOUT = json_settings[environ["project_env"]]["analyzer_timeout"]
URL_TIMEOUT = json_settings[environ["project_env"]]["url_timeout"]
RD = Redis.from_url(json_settings[environ["project_env"]]["redis_settings"])
CELERY = Celery(json_settings[environ["project_env"]]["celery_settings"]["name"],
                broker=json_settings[environ["project_env"]]["celery_settings"]["celery_broker_url"],
                backend=json_settings[environ["project_env"]]["celery_settings"]["celery_result_backend"])

CELERY.control.purge()
MONGO_DB = MongoEngine()
MONGO_DB.init_app(APP)
BCRYPT = Bcrypt(APP)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.setup_app(APP)
CSRF = CSRFProtect()
CSRF.init_app(APP)
Markdown(APP)

APP.jinja_env.add_extension('jinja2.ext.loopcontrols')


class Namespace:
    '''
    this namespace for switches
    '''

    def __init__(self, kwargs):
        self.__dict__.update(kwargs)


def convert_size(_size):
    '''
    convert size to unit
    '''
    for _unit in ['B', 'KB', 'MB', 'GB']:
        if _size < 1024.0:
            return "{:.2f}{}".format(_size, _unit)
        _size /= 1024.0
    return "File is too big"


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    '''
    load user
    '''
    return User.objects(id=user_id).first()


class User(MONGO_DB.Document):
    '''
    this class has all users
    '''
    login = MONGO_DB.StringField(max_length=80, unique=True)
    password = MONGO_DB.StringField(max_length=64)
    meta = meta_users_settings

    @property
    def is_authenticated(self):
        '''
        is the user authenticated or not
        '''
        return True

    @property
    def is_active(self):
        '''
        is the user active or not
        '''
        return True

    @property
    def is_anonymous(self):
        '''
        is the user anonymous (this function not used)
        '''
        return False

    def get_id(self):
        '''
        get user id from the database
        '''
        return str(self.id)

    def __unicode__(self):
        '''
        unicode
        '''
        return self.login


class UserView(ModelView):
    '''
    user view (visable)
    '''
    list_template = 'list.html'
    can_create = False
    can_delete = True
    can_edit = False

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))

    @expose('/')
    def index_view(self):
        '''
        User list route
        '''
        self._template_args['card_title'] = 'Current users'
        return super(UserView, self).index_view()


class Reports(MONGO_DB.Document):
    '''
    reports doc
    '''
    task = MONGO_DB.StringField()
    type = MONGO_DB.StringField()
    file = MONGO_DB.FileField()
    time = MONGO_DB.DateTimeField()
    meta = meta_reports_settings


class ReportsViewJSON(ModelView):
    '''
    json reports view (visable)
    '''
    list_template = 'list.html'
    can_create = False
    can_delete = True
    can_edit = False
    column_searchable_list = ['task']
    column_default_sort = ('time', True)

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))

    def get_query(self):
        '''
        return json object
        '''
        return Reports.objects(type="application/json")

    @expose('/')
    def index_view(self):
        '''
        json reports list route
        '''
        self._template_args['card_title'] = 'Generated JSON reports'
        return super(ReportsViewJSON, self).index_view()


class ReportsViewHTML(ModelView):
    '''
    html reports view (visable)
    '''
    list_template = 'list.html'
    can_create = False
    can_delete = True
    can_edit = False
    column_searchable_list = ['task']
    column_default_sort = ('time', True)

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))

    def get_query(self):
        '''
        return html object
        '''
        return Reports.objects(type="text/html")

    @expose('/')
    def index_view(self):
        '''
        html reports list route
        '''
        self._template_args['card_title'] = 'Generated HTML reports'
        return super(ReportsViewHTML, self).index_view()


class Logs(MONGO_DB.Document):
    '''
    logs doc
    '''
    task = MONGO_DB.StringField()
    type = MONGO_DB.StringField()
    file = MONGO_DB.FileField()
    time = MONGO_DB.DateTimeField()
    meta = meta_task_files_logs_settings


class LogsView(ModelView):
    '''
    logs view (visable)
    '''
    list_template = 'list.html'
    can_create = False
    can_delete = True
    can_edit = False
    column_searchable_list = ['task']
    column_default_sort = ('time', True)

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))

    @expose('/')
    def index_view(self):
        '''
        logs list route
        '''
        self._template_args['card_title'] = 'Generated logs'
        return super(LogsView, self).index_view()


class Input(MONGO_DB.Document):
    '''
    logs doc
    '''
    start = MONGO_DB.DateTimeField()
    task = MONGO_DB.StringField()
    use_proxy = MONGO_DB.StringField()
    proxy = MONGO_DB.StringField()
    buffer = MONGO_DB.StringField()
    useragent = MONGO_DB.StringField()
    useragent_mapped = MONGO_DB.StringField()
    meta = meta_task_logs_settings


class InputView(ModelView):
    '''
    logs view (visable)
    '''
    list_template = 'list.html'
    can_create = False
    can_delete = True
    can_edit = False
    column_searchable_list = ['buffer']
    column_default_sort = ('start', True)

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))

    @expose('/')
    def index_view(self):
        '''
        logs list route
        '''
        self._template_args['card_title'] = 'Generated logs'
        return super(InputView, self).index_view()


class LoginForm(form.Form):
    '''
    login form (username and password)
    '''
    login = fields.StringField(render_kw={"placeholder": "Username", "autocomplete": "off"})
    password = fields.PasswordField(render_kw={"placeholder": "Password", "autocomplete": "off"})

    def validate_login(self, field):
        '''
        log in
        '''
        user = self.get_user()  # fix AttributeError: 'NoneType' object has no attribute 'password'
        if user is not None:
            if not BCRYPT.check_password_hash(user.password, self.password.data):
                raise validators.ValidationError('Invalid password')

    def get_user(self):
        '''
        get log in
        '''
        return User.objects(login=self.login.data).first()


class RegistrationForm(form.Form):
    '''
    register form (username and password)
    '''
    login = fields.StringField(render_kw={"placeholder": "Username"})
    password = fields.PasswordField(render_kw={"placeholder": "Password"})

    def validate_login(self, field):
        '''
        get log in
        '''
        if User.objects(login=self.login.data):
            raise validators.ValidationError('Duplicate username')


class CustomAdminIndexView(AdminIndexView):
    '''
    Custom login view
    '''
    @expose('/')
    def index(self):
        '''
        main route
        '''
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        # return redirect("/stats")

        self._template_args['filename'] = "https://github.com/qeeqbox/url-sandbox"
        self._template_args['intro'] = "Do not forget to check my other project!"
        #self._template_args['location_tree'] = "Home"
        return super(CustomAdminIndexView, self).index()

    @expose('/login/', methods=['POST', 'GET'])
    def login_view(self):
        '''
        login route
        '''
        temp_form = LoginForm(request.form)
        if request.method == 'POST' and temp_form.validate():
            user = temp_form.get_user()
            if user is not None:
                login_user(user)

        if current_user.is_authenticated:
            session["navs"] = []
            return redirect(request.args.get('next') or url_for('.index'))

        self._template_args['form'] = temp_form
        self._template_args['active'] = "Login"
        self._template_args['intro'] = ""
        self._template_args['link'] = '<p>Register? <a href="{}">Click here</a></p>'.format(url_for('.register_view'))
        return super(CustomAdminIndexView, self).index()

    @expose('/register/', methods=('GET', 'POST'))
    def register_view(self):
        '''
        register route
        '''
        temp_form = RegistrationForm(request.form)
        if request.method == 'POST' and temp_form.validate():
            user = User()
            temp_form.populate_obj(user)
            if len(user["password"]) > 0 and len(user["login"]) > 0:
                user["password"] = BCRYPT.generate_password_hash(user["password"]).decode('utf-8')
                user.save()
                login_user(user)
                session["navs"] = []
                return redirect(url_for('.index'))

        self._template_args['form'] = temp_form
        self._template_args['active'] = "Register"
        self._template_args['intro'] = ""
        self._template_args['link'] = '*Please do not enter a used username or password<p><p>Login? <a href="{}">Click here</a></p>'.format(url_for('.login_view'))
        return super(CustomAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        '''
        logout route
        '''
        logout_user()
        session["navs"] = []
        return redirect(url_for('.index'))

    @expose('/toggled', methods=('GET', 'POST'))
    def is_toggled(self):
        '''
        toggled route (this will keep track of toggled items)
        '''
        with ignore_excpetion(Exception):
            if current_user.is_authenticated:
                json_content = request.get_json(silent=True)
                for key, value in json_content.items():
                    if value == "false":
                        session["navs"].remove(key)
                    else:
                        session["navs"].append(key)
        return jsonify("Done")

    def is_visible(self):
        '''
        Do not show items in the sidebar
        '''
        return False


class MultiCheckboxField(SelectMultipleField):
    '''
    this class will be used for mulit checckbox
    '''
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class BufferForm(form.Form):
    '''
    needs more check
    '''
    choices = MultiCheckboxField('Assigned', choices=SWITCHES)
    buffer = fields.TextAreaField(render_kw={"class": "buffer"})
    proxy = fields.StringField(render_kw={"class": "proxy", "placeholder": "socks5://proxy:9050"})
    useragents = fields.SelectField('useragents', choices=USERAGENTS, default="Firefox")
    urltimeout = fields.SelectField('urltimeout', choices=[(5, '5 sec URL timeout'), (10, '10 sec URL timeout'), (30, '30 sec URL timeout'), (60, '1 min URL timeout')], default=(URL_TIMEOUT), coerce=int)
    analyzertimeout = fields.SelectField('analyzertimeout', choices=[(30, '30 sec analyzing timeout'), (60, '1 min analyzing timeout'), (120, '2 mins analyzing timeout')], default=(ANALYZER_TIMEOUT), coerce=int)
    submit = fields.SubmitField(render_kw={"class": "btn"})
    submitandwait = fields.SubmitField('Submit And Wait', render_kw={"class": "btn"})
    __order = ('buffer', 'proxy', 'choices', 'useragents', 'urltimeout', 'analyzertimeout', 'submit', 'submitandwait')

    def __iter__(self):
        temp_fields = list(super(BufferForm, self).__iter__())
        def get_field(fid): return next((f for f in temp_fields if f.id == fid))
        return (get_field(fid) for fid in self.__order)


class CustomViewBufferForm(BaseView):
    '''
    upload buffer main form
    '''
    extra_js = ['/static/checktask.js']

    @expose('/', methods=['POST', 'GET'])
    def index(self):
        '''
        main route
        '''
        temp_form = BufferForm(request.form)
        if request.method == 'POST':
            if temp_form.buffer.data != "":
                good_url = False
                try:
                    validators.url(temp_form.buffer.data)
                    good_url = True
                except BaseException:
                    pass
                if good_url:
                    task = str(uuid4())
                    result = {}
                    for item in SWITCHES:
                        result.update({item[0]: False})
                    for item in request.form.getlist("choices"):
                        result.update({item: True})
                    result["buffer"] = temp_form.buffer.data
                    result["proxy"] = temp_form.proxy.data
                    result["task"] = task
                    result["analyzer_timeout"] = temp_form.analyzertimeout.data
                    result["url_timeout"] = temp_form.urltimeout.data
                    result["useragent"] = temp_form.useragents.data
                    result["useragent_mapped"] = SWITCHES_MAPPED[temp_form.useragents.data]
                    if result['use_proxy']:
                        if len(result['proxy']) == 0:
                            result['proxy'] = 'socks5://proxy:9050'
                    _task = CELERY.send_task(json_settings[environ["project_env"]]["worker"]["name"],
                                             args=[result],
                                             queue=json_settings[environ["project_env"]]["worker"]["queue"])
                    if request.form.get('submitandwait') == 'Submit And Wait':
                        flash(gettext(task), 'successandwaituuid')
                    else:
                        flash(gettext('Done submitting buffer Task {}'.format(task)), 'success')
                else:
                    flash(gettext("Invalid URL"), 'error')
            else:
                flash(gettext("Something wrong"), 'error')
        return self.render("upload.html", header="Scan URL", form=temp_form, switches_details="")

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


def get_stats():
    '''
    get stats from databases
    '''
    stats = {}
    with ignore_excpetion(Exception):
        for coll in (defaultdb["reportscoll"], defaultdb["filescoll"], "fs.chunks", "fs.files"):
            if coll in CLIENT[defaultdb["dbname"]].list_collection_names():
                stats.update({"[{}] Collection".format(coll): "Exists"})
            else:
                stats.update({"[{}] Collection".format(coll): "Does not exists"})
    with ignore_excpetion(Exception):
        stats.update({"[Reports] Total reports": CLIENT[defaultdb["dbname"]][defaultdb["reportscoll"]].find({}).count(),
                      "[Reports] Total used space": "{}".format(convert_size(CLIENT[defaultdb["dbname"]].command("collstats", defaultdb["reportscoll"])["storageSize"] + CLIENT[defaultdb["dbname"]].command("collstats", defaultdb["reportscoll"])["totalIndexSize"]))})
    with ignore_excpetion(Exception):
        stats.update({"[Files] Total files uploaded": CLIENT[defaultdb["dbname"]][defaultdb["filescoll"]].find({}).count()})
    with ignore_excpetion(Exception):
        stats.update({"[Files] Total uploaded files size": "{}".format(convert_size(CLIENT[defaultdb["dbname"]]["fs.chunks"].find().count() * 255 * 1000))})
    with ignore_excpetion(Exception):
        stats.update({"[Users] Total users": CLIENT[defaultdb["dbname"]][defaultdb["userscoll"]].find({}).count()})
    with ignore_excpetion(Exception):
        total, used, free = disk_usage("/")
        stats.update({"CPU memory": cpu_percent(),
                      "Memory used": virtual_memory()[2],
                      "Current process used memory": "{}".format(convert_size(Process(getpid()).memory_info().rss)),
                      "Total disk size": "{}".format(convert_size(total)),
                      "Used disk size": "{}".format(convert_size(used)),
                      "Free disk size": "{}".format(convert_size(free)),
                      "Host platform": pplatform()})
    CLIENT.close()
    return stats


class CustomStatsView(BaseView):
    '''
    Stats view
    '''
    @expose('/', methods=['GET'])
    def index(self):
        '''
        state route
        '''
        return self.render("stats.html", stats=get_stats())

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


def find_and_srot(database, collection, key, var):
    '''
    hmm finding by time is weird?
    '''
    temp_list = []
    if key == "time":
        items = list(CLIENT[database][collection].find().sort([('_id', -1)]).limit(1))
    else:
        items = list(CLIENT[database][collection].find({key: {"$gt": var}}).sort([(key, ASCENDING)]))
    for item in items:
        temp_list.append("{} {}".format(item["time"].isoformat(), item["message"]))
    if len(temp_list) > 0:
        return "\n".join(temp_list), str(items[-1]["_id"])
    return "", 0


def get_last_logs(json):
    '''
    get last item from logs
    '''
    items = []
    if json['id'] == 0:
        items, startid = find_and_srot(defaultdb["dbname"], defaultdb["alllogscoll"], "time", datetime.now())
    else:
        items, startid = find_and_srot(defaultdb["dbname"], defaultdb["alllogscoll"], "_id", ObjectId(json['id']))
    return {"id": startid, "logs": items}


class CustomLogsView(BaseView):
    '''
    logs view
    '''
    extra_js = ['/static/activelogs.js']

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        '''
        main entry
        '''
        if request.method == 'GET':
            return self.render("activelogs.html")
        elif request.method == 'POST':
            if request.json:
                json_content = request.get_json(silent=True)
                return dumps(get_last_logs(json_content))
        return jsonify({"Error": "Something wrong"})

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


class CheckTask(BaseView):
    '''
    check task view (This acts as api)
    '''
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        '''
        check task route
        '''
        if request.method == 'POST':
            if request.json:
                json_content = request.get_json(silent=True)
                item = CLIENT[defaultdb["dbname"]][defaultdb["taskdblogscoll"]].find_one({"task": json_content["task"]})
                if item:
                    if item["end"]:
                        item = get_it_fs(defaultdb["dbname"], {"task": json_content["task"], 'contentType': 'text/html'})
                        if item:
                            return BeautifulSoup(item).find('body').decode_contents()
                        return "Something wrong"
            return ""
        return self.render("activelogs.html")

    def is_visible(self):
        '''
        not visable in the bar (just an api)
        '''
        return False

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


class SendLogs(BaseView):
    '''
    Send logs (This acts as api)
    '''
    @CSRF.exempt
    @expose('/', methods=['POST', 'GET'])
    def index(self):
        '''
        Add logs
        '''
        file = request.files.get('file')

    def is_visible(self):
        '''
        not visable in the bar (just an api)
        '''
        return False


class TimeEncoder(JSONEncoder):
    '''
    json encoder for time
    '''

    def default(self, obj):
        '''
        override default
        '''
        if isinstance(obj, datetime):
            return obj.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")
        return JSONEncoder.default(self, obj)


def find_items_without_coll(database, collection, items):
    '''
    ???
    '''
    temp_dict = {}
    for item in items:
        if item != '':
            temp_ret = CLIENT[database][collection].find_one({"_id": ObjectId(item)}, {'_id': False})
            if temp_ret is not None:
                temp_dict.update({item: temp_ret})
    return temp_dict


class CustomMenuLink(MenuLink):
    '''
    items will the header top left
    '''

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


class StarProject(MenuLink):
    '''
    ??
    '''

    def is_accessible(self):
        '''
        is accessible
        '''
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        '''
        if not accessible then go to login
        '''
        return redirect(url_for('admin.login_view', next=request.url))


ADMIN = Admin(APP, "QeeqBox", index_view=CustomAdminIndexView(url='/'), base_template='base.html', template_mode='bootstrap3')
ADMIN.add_link(CustomMenuLink(name='', category='', url="https://github.com/qeeqbox/url-sandbox", icon_type='glyph', icon_value='glyphicon-star'))
ADMIN.add_link(CustomMenuLink(name='', category='', url="https://github.com/qeeqbox/url-sandbox/archive/master.zip", icon_type='glyph', icon_value='glyphicon-download-alt'))
ADMIN.add_link(CustomMenuLink(name='', category='', url="https://github.com/qeeqbox/url-sandbox/subscription", icon_type='glyph', icon_value='glyphicon glyphicon-eye-open'))
ADMIN.add_link(CustomMenuLink(name='Logout', category='', url="/logout", icon_type='glyph', icon_value='glyphicon glyphicon-user'))
ADMIN.add_view(CustomViewBufferForm(name="URL", endpoint='url', menu_icon_type='glyph', menu_icon_value='glyphicon-edit', category='Analyze'))
ADMIN.add_view(ReportsViewHTML(Reports, name="HTML", endpoint='reportshtml', menu_icon_type='glyph', menu_icon_value='glyphicon-list-alt', category='Reports'))
ADMIN.add_view(ReportsViewJSON(Reports, name="JSON", endpoint='reportsjson', menu_icon_type='glyph', menu_icon_value='glyphicon-list-alt', category='Reports'))
ADMIN.add_view(LogsView(Logs, name='Tasks', menu_icon_type='glyph', menu_icon_value='glyphicon-info-sign', category='Logs'))
ADMIN.add_view(InputView(Input, name='Input', menu_icon_type='glyph', menu_icon_value='glyphicon-info-sign', category='Logs'))
ADMIN.add_view(CustomLogsView(name="Active", endpoint='activelogs', menu_icon_type='glyph', menu_icon_value='glyphicon-flash', category='Logs'))
ADMIN.add_view(CustomStatsView(name="Stats", endpoint='stats', menu_icon_type='glyph', menu_icon_value='glyphicon-stats'))
ADMIN.add_view(UserView(User, menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
ADMIN.add_view(CheckTask('Task', endpoint='task', menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
#ADMIN.add_view(SendLogs('Send', endpoint='send', menu_icon_type='glyph', menu_icon_value='glyphicon-user'))
#app.run(host = "127.0.0.1", ssl_context=(certsdir+'cert.pem', certsdir+'key.pem'))
#app.run(host = "127.0.0.1", port= "8001", debug=True)


@APP.before_request
def before_request():
    '''
    needed session fields
    '''
    session.permanent = True
    APP.permanent_session_lifetime = timedelta(minutes=60)
    session.modified = True


def handle_all_errors(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return jsonify(error='Error', code=code)


for exc in default_exceptions:
    APP.register_error_handler(exc, handle_all_errors)
