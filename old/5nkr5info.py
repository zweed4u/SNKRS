#Dictionary implementation
import urllib2, json
from time import gmtime, strftime
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

def newParse(url):
	global data
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req)
	data = json.loads(resp.read())

def populate(catalog,data):
	for thread in data['threads']:
		if str(thread['product']['style']+'-'+thread['product']['colorCode']) =='999999-999':
			pass
		else:
			catalog[thread['name']]={}
			catalog[thread['name']].update({'id':'https://www.nike.com/snkrs/thread/'+thread['id']})
			catalog[thread['name']].update({'style':thread['product']['style']+'-'+thread['product']['colorCode']})
			catalog[thread['name']].update({'globalPid':thread['product']['globalPid']})
			#urllib.urlretrieve(str(thread['product']['imageUrl']), 'images/'+str(thread['product']['imageUrl'].split('DotCom/')[1])+".jpg")
			try:
				catalog[thread['name']].update({'heatLevel': thread['product']['heatLevel']})
			except:
				catalog[thread['name']].update({'heatLevel': 'n/a'})
			catalog[thread['name']].update({'formattedCurrentRetailPrice':thread['product']['price']['formattedCurrentRetailPrice'].split('.')[0]})
			launch=thread['product']['estimatedLaunchDate']
			catalog[thread['name']].update({'estimatedLaunchDate':str(utcToEst(launch)).split('-04:00')[0]})
			
			start=thread['product']['startSellDate']
			catalog[thread['name']].update({'startSellDate':str(utcToEst(start)).split('-04:00')[0]})
			try:
				end=thread['product']['endDrawDate']
				catalog[thread['name']].update({'endDrawDate':str(utcToEst(end)).split('-04:00')[0]})
			except:
				pass

			catalog[thread['name']].update({'selectionEngine': thread['product']['selectionEngine']})
		

numOfThreads=raw_input('Number of threads? ')
mainUrl='https://api.nike.com/commerce/productfeed/products/snkrs/threads?country=US&limit='+numOfThreads+'&locale=en_US&withCards=true'

newParse(mainUrl)
print '\n'
catalog={}
populate(catalog,data)
for product in catalog:
	print product
	for attrib in catalog[product]:
		print attrib+' :: '+catalog[product][attrib]
	print '\n'
