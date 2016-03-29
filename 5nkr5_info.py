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
			snkrsUrl='https://www.nike.com/snkrs/thread/'+thread['id']
			print 'https://www.nike.com/snkrs/thread/'+thread['id']
			urllib.urlretrieve(str(thread['product']['imageUrl']), 'images/'+str(thread['product']['imageUrl'].split('DotCom/')[1])+".jpg")
			try:
				print 'Heat Level: '+thread['product']['heatLevel']
			except:
				print 'Heat Level: n/a'
			print thread['product']['price']['formattedCurrentRetailPrice'].split('.')[0]
			launch=thread['product']['estimatedLaunchDate']
			print str(utcToEst(launch)).split('-04:00')[0]
			print thread['product']['selectionEngine']
			print '\n'
		except:
			pass
