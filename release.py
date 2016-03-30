import urllib2, json, urllib
from xml.dom import minidom
from datetime import datetime
from dateutil import tz

def utcToEst(date):
	date=date.replace('T', ' ').split('.')[0]
	from_zone = tz.tzutc()
	to_zone = tz.tzlocal()
	utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
	utc = utc.replace(tzinfo=from_zone)
	eastern = utc.astimezone(to_zone)
	return eastern

def newParse():
	global data
	req = urllib2.Request(mainUrl)
	resp = urllib2.urlopen(req)
	data = json.loads(resp.read())

numOfThreads=raw_input('Number of threads? ')
mainUrl='https://api.nike.com/commerce/productfeed/products/snkrs/threads?country=US&limit='+numOfThreads+'&locale=en_US&withCards=true'

newParse()
print '\n'


'''
-Go through numThread items, parsing name and appending to list,
-Have second list revisit and parse for names, if new name found, parse
'''


for thread in data['threads']:
	name=thread['name']
	styleCode=str(thread['product']['style']+'-'+thread['product']['colorCode'])
	if str(thread['product']['style']+'-'+thread['product']['colorCode']) =='999999-999':
		pass
	else:
		pid=thread['product']['globalPid']
		print thread['name']+' : '+thread['product']['style']+'-'+thread['product']['colorCode']+' : '+thread['product']['globalPid']
		try:
			launch=thread['product']['estimatedLaunchDate']
			print 'EstimatedLaunchDate: '+str(utcToEst(launch)).split('-04:00')[0]
			start=thread['product']['startSellDate']
			print 'StartSellDate: '+str(utcToEst(start)).split('-04:00')[0]
			try:
				end=thread['product']['endDrawDate']
				print 'EndDrawDate: '+str(utcToEst(end)).split('-04:00')[0]
			except:
				pass
			print thread['product']['selectionEngine']
			print '\n'
		except:
			pass
