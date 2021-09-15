# tutorial: secured requests to the garagescore api
# -*- coding: utf-8 -*-
from collections import OrderedDict
from hashlib import sha1
import hmac
import logging
import requests
import sys
import time
import urllib

logging.basicConfig(level=logging.INFO)

API_URL = 'api.garagescore.com/'
PROTOCOL = 'https'

def _encodeURI(str):
	return urllib.quote(str, safe='~@#$&()*!+=:;,.?/\'')

def _sign(API_KEY, API_SECRET, method, url, parameters):
	timestamp = str(int(time.time()))
	parametersString = urllib.urlencode(parameters)
	encodedUrl = _encodeURI(url)
	signatureString = API_KEY + method + encodedUrl + parametersString + timestamp;
	hashed = hmac.new(API_SECRET, signatureString, sha1)
	return hashed.digest().encode("hex")


# generate an url to the api
def generateURL(API_KEY, API_SECRET, method, uri, params):
	if (params and len(params) > 0):
		params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))
	url = PROTOCOL + '://' + API_URL + uri
	signature = _sign(API_KEY, API_SECRET, method, url, params)
	parametersString = urllib.urlencode(params)
	if (parametersString):
		parametersString = '&' + parametersString
	requestURL = url + '?' + 'signature=' + signature + '&appId=' + API_KEY + parametersString
	logging.info('requestURL = ' + requestURL)
	return requestURL

# request the api
def request(API_KEY, API_SECRET, method, uri, params = {}, jsonPOST = None):
  r = ''
  url = generateURL(API_KEY, API_SECRET, method, uri, params)
  if (method == 'GET'):
  	r = requests.get(url).text
  else:
  	r = requests.post(url, json = jsonPOST).text
  logging.info(repr(r))
  return r

if __name__ == '__main__':
	API_KEY = sys.argv[1]
	API_SECRET = sys.argv[2]
	request(API_KEY, API_SECRET, 'GET', 'garage/searchwith/businessId/31547505300031', {})
	request(API_KEY, API_SECRET, 'GET', 'garage/59397ebf9b90721900cc1f7b/reviews', {})
