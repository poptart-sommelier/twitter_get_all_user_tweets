#!/usr/bin/python3.5

import requests
import sys
import queue
from threading import Thread
import re

#   references:
#   https://unshorten.it/api/documentation
#   http://docs.python-requests.org/en/master/user/quickstart/ (see redirect portion)
#   threading:
#   http://www.craigaddyman.com/python-queues-and-multi-threading/

#   TODO:
#   test this to make sure that it follows both normal redirects (r.status_code OR r.history) as well as check BODY for any meta tag redirects/refreshes

def unshorten(shorturl):
	# requests does all the work for us, following all redirects
	# TODO: THIS SHOULD BE THREADED
	r = requests.get(shorturl)
	return r.url


# we only want this to run if it is called directly off the command line
if __name__ == "__main__":

	linearray = []
	outarray = []
	with open('file.txt', 'r') as f:
		linearray = f.readlines()

	for line in linearray:
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
	#	outline = str(line.strip('\n')) + "(" + [l for l in urls] + ")"
		if len(urls) != 0:
			for url in urls:
				for i in range(10):
					t = Thread(target=unshorten, args=(url,))
#						unshort = unshorten(url)
					outarray.append(line.strip('\n') + " : (" + t.strip('\n') + ")" + '\n')	
					print(line.strip('\n') + " : (" + t.strip('\n') + ")")
		else:
			outarray.append(line)
			print(line.strip('\n'))

	print(outarray)
