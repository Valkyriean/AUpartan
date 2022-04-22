"""
from OWSLib.wfs import WebFeatureService
wfs11 = WebFeatureService(url="https://openapi.aurin.org.au/wfs", version='1.0')
wfs11.identification.title
"""
#code from https://github.com/AURIN/openapi-examples/tree/master/python adjested from python 2 code
import configparser
import urllib3
from lxml import etree

config = configparser.RawConfigParser()
config.read('openapi.cfg')
username=config.get('Auth', 'username')
password=config.get('Auth', 'password')

def openapi_request(url):
    password_manager = urllib3.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_manager = urllib3.HTTPBasicAuthHandler(password_manager)
    opener = urllib3.build_opener(auth_manager)
    urllib3.install_opener(opener)
    req = urllib3.Request(url)
    handler = urllib3.urlopen(req)

    return handler.read()



