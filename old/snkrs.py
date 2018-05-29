#!/bin/env python2.7
# This could be deprecated. Who knows?
# This is what I used for submitting entries for
# the kobe fade to black drops.
# Play around with it. 
# Not much has changed. There has been confirm
import sys,json,requests

styleCode='863586-010'
skuId='17704479'

# Too lazy - not implementing this but instructions below
#go here and scrape 'https://api.nike.com/commerce/productsize/products/'+styleCode+'/availability?country=US&channel=SNKRS'
#for size in resp.json()[sizes]:
#	if size['size']=='11':
#		skuID=size['sku']

print styleCode+' selected!'
#start session
session=requests.Session()

#LOGIN
print 'Logging in...'
loginUrl='https://unite.nikecloud.com/login?locale=en_US&backendEnvironment=identity'
loginHeaders = {
	'host':'unite.nikecloud.com',                                                                                                                          
	'Content-Type':'text/plain',                                                                                                                                   
	'Origin':'https://s3.nikecdn.com',                                                                                                                       
	'Connection':'keep-alive',                                                                                                                                   
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Accept':'*/*',                                                                                                                                          
	'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Mobile/11D257',
	'Accept-Language':'en-us',                                                                                                                                        
	'Accept-Encoding':'gzip, deflate',  
}
loginPayload={
	"username":"anonymous@mailinator.com",
	"password":"XXXXXXXXXXXXXXXXXXX",
	"client_id":"G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj",		#This is @jayzer1217's iOS device
	"ux_id":"com.nike.commerce.snkrs.ios",
	"grant_type":"password"
}
#logging in to your sneakers account
loginResp=session.post(loginUrl,data=json.dumps(loginPayload),headers=loginHeaders)

#vital information from login response
try:
	user_id=str(loginResp.json()['user_id'])
	access_token=str(loginResp.json()['access_token'])
	refresh_token=str(loginResp.json()['refresh_token'])
	print 'Login successful!\n'
	print 'access_token: '+access_token
except:
	print 'Login failed!'
	print 'Error: '+loginResp.json()['error']
	sys.exit()
#GET PAYMENT INFO
print '\nFinding payment information associated with your account...'
payUrl='https://api.nike.com/commerce/storedpayments/consumer/storedpayments'
payHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Content-Type':'application/json',                                                                                                                             
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Connection':'keep-alive',                                                                                                                                   
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Accept':'*/*',                                                                                                                                          
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)',                                                                                          
	'Accept-Language':'en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5',                                                                                     
	'Authorization':'Bearer '+str(access_token)                                                                                                       
}
#FILL THIS OUT WITH ACCOUNT MATCHING INFORMATION
payPayload={
	"address1": "181 Drury Ln.", 
	"address2": "", 
	"city": "Beverly Hills", 
	"country": "US", 
	"email": "", 
	"firstName": "John", 
	"lastName": "Doe", 
	"phoneNumber": "telephonenumberhere",   #5088675309 
	"postalCode": "90210",					 
    "state": "CA"
}
#getting info - listed: i have paypal. cc and gift card associated with my account
payResp=session.post(payUrl,data=json.dumps(payPayload),headers=payHeaders)
print 'Collecting payment options in hash map...'
ccPidleId=''
giftCardPidleId=''
paypayPidleId=''
debitPidleId=''
for option in payResp.json()['payments']:
	if 'paypal' in option['type'].lower():
		paypayPidleId=option['paymentId']
	if 'giftcard' in option['type'].lower():
		giftCardPidleId=option['paymentId']
	if 'credit' in option['type'].lower():
		if 'XXXX' in option['accountNumber']:
			debitPidleId=option['paymentId']
		else:
			ccPidleId=option['paymentId']

payOptions={}
for method in payResp.json()['payments']:
	payOptions.update({method['type']:method['paymentId']})
#assuming we pick our default payment
print '\n'
print payOptions
print '\n'
print 'Choosing ...'
print giftCardPidleId
print ccPidleId

#GET CART ID/SESSION
print '\nGetting cartId...'
checkoutUrl='https://api.nike.com/orders/v1/orders/checkouts'
checkoutHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Accept':'*/*',                                                                                                                                          
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Authorization':'Bearer '+str(access_token),                                                                                                          
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Accept-Language':'en-us',                                                                                                                                        
	'Content-Type':'application/json',                                                                                                              
	'Connection':'keep-alive',                                                                                                                                   
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)'
}

checkoutPayload={
	"country": "US", 
    "currency": "USD", 
    "email": "anonymous@mailinator.com", 
    "locale": "en_US"
}
#CART ID INSTANTIATION
checkoutResp=session.post(checkoutUrl,data=json.dumps(checkoutPayload),headers=checkoutHeaders)
#cartId
checkoutId=checkoutResp.json()['id']

#PUT request for item
print 'Associating item with cartId... (Press enter when item goes live!) '
raw_input()
item='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/items'
itemHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Content-Type':'application/json',                                                                                                                             
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Connection':'keep-alive',                                                                                                                                   
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Accept':'*/*',                                                                                                                                          
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)',                                                                                          
	'Accept-Language':'en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5',                                                                                     
	'Authorization':'Bearer '+str(access_token)                                                                                                       
}

#STYLE CODE GOES HERE
itemPayload={
	"color":str(styleCode.split('-')[1]),
	"quantity":"1",
	"size":"11",
	"style":str(styleCode.split('-')[0])

}
itemResp=session.put(item,data=json.dumps(itemPayload),headers=itemHeaders)
try:
	if itemResp.json()['status']=='CREATED':
		print 'CartId instance with item created!'
	else:
		print itemResp.json()['status']
except:
	print '\nProblem with PUT request!'
	print itemResp.json()
	#loop on itself request
	#exiting for now
	sys.exit()


#PUT Shipping select
print 'Selecting STANDARD for shipping method...'
shipping='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/shippingmethod'
shippingHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Content-Type':'application/json',                                                                                                                             
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Connection':'keep-alive',                                                                                                                                   
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Accept':'*/*',                                                                                                                                          
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)',                                                                                          
	'Accept-Language':'en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5',                                                                                     
	'Authorization':'Bearer '+str(access_token)
}
shippingPayload={
	"id":"STANDARD"
}
shippingResp=session.put(shipping,data=json.dumps(shippingPayload),headers=shippingHeaders)
#print shippingResp.json()


#PUT shipping address
print 'Associating shipping address with cart instance...'
address='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/shippingaddress'
addressHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Content-Type':'application/json',                                                                                                                             
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Connection':'keep-alive',                                                                                                                                   
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Accept':'*/*',                                                                                                                                          
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)',                                                                                          
	'Accept-Language':'en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5',                                                                                     
	'Authorization':'Bearer '+str(access_token)
}
addressPayload={
    "address1": "181 Drury Ln.", 
    "city": "Beverly Hills", 
    "country": "US", 
    "firstName": "John", 
    "lastName": "Doe", 
    "phoneNumber": "5088675309", 
	"postalCode": "90210", 
	"state": "CA"

}
addressResp=session.put(address,data=json.dumps(addressPayload),headers=addressHeaders)
#print addressResp.json()



#ASSOCIATE PAYMENT WITH CART
# This will need to be tinkered with!
# This is valid for my account not yours
print '\nAdding paymentId to cart...'
cart='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/payments'
cartHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Accept':'*/*',                                                                                                                                          
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Authorization':'Bearer '+str(access_token),                                                                                                          
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Accept-Language':'en-us',                                                                                                                                        
	'Content-Type':'application/json',                                                                                                              
	'Connection':'keep-alive',                                                                                                                                   
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)'
}
cartPayload={
	"paymentType": "paypalbillingagreement", 
	"token": str(ccPidleId)
}

cartResp=session.post(cart,data=json.dumps(cartPayload),headers=cartHeaders)
print 'Payment added!\n'

#ASSOCIATE giftPAYMENT WITH CART
print '\nAdding gift card paymentId to cart...'
cart2='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/payments'
cart2Headers={
	'host':'api.nike.com',                                                                                                                                 
	'Accept':'*/*',                                                                                                                                          
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Authorization':'Bearer '+str(access_token),                                                                                                          
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Accept-Language':'en-us',                                                                                                                                        
	'Content-Type':'application/json',                                                                                                              
	'Connection':'keep-alive',                                                                                                                                   
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)'
}
cart2Payload={
	"paymentType": "paypalbillingagreement", 
	"token": str(giftCardPidleId)
}

cartResp2=session.post(cart2,data=json.dumps(cart2Payload),headers=cart2Headers)
print 'Alt. payment added!\n'

#PASSWORD CHECK-CONFIRM
print 'Confirming entry with password...'
passUrl='https://api.nike.com/userCheck'
passHeaders={
	'host':'api.nike.com',                                                                                                                                 
	'Accept':'*/*',                                                                                                                                          
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Authorization':'Bearer '+str(access_token),                                                                                                          
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Accept-Language':'en-us',                                                                                                                                        
	'Content-Type':'application/json',                                                                                                              
	'Connection':'keep-alive',                                                                                                                                   
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)'
}
passPayload={
	"password": "XXXXXXXXXXXXXXXXXXX"
}

passResp=session.post(passUrl,data=json.dumps(passPayload),headers=passHeaders)
try:
	passResp.json()['nuId']
	print 'Password confim successful!\n'
except:
	passResp.json()['errors'][0]['message']
	sys.exit()

validate='https://api.nike.com/orders/v1/orders/checkouts/'+str(checkoutId)+'/validate'
validateResp=session.get(validate,headers=passHeaders)

#should equal true->
try:
	if validateResp.json()['valid']==True:
		print 'Valid Entry! Ready for submission!\n'
	else:
		print 'Not a valid entry!'
		print validateResp.json()
		sys.exit()
except:
	print validateResp.json()
	sys.exit()
#ENTRY REQUEST
entry='https://api.nike.com/commerce/launchwaitline/launch/waitline/turnToken'

entryHeaders={                                                                                      
	'Content-Type':'application/json',                                                                                                            
	'host':'api.nike.com',                                                                                                                                 
	'Accept':'*/*',                                                                                                                                          
	'Proxy-Connection':'keep-alive',                                                                                                                                   
	'Authorization':'Bearer '+str(access_token),                                                                                                          
	'Accept-Encoding':'gzip, deflate',                                                                                                                                
	'Accept-Language':'en-us',                                                                                                                                        
	'Connection':'keep-alive',                                                                                                                                   
	'User-Agent':'SNKRS-inhouse/2.0.1 (iPhone; iOS 7.1.2; Scale/2.00)'
}

entryPayload={
	"checkoutId": str(checkoutId), 
    	"country": "US", 
    	"personalInfo": {
		"email": "anonymous@mailinator.com", 
		"mobilePhone": "+15088675309", 
		"shippingAddress": {
	    		"address1": "181 Drury Ln.", 
	    		"address2": "", 	
		    	"address3": "", 
		    	"city": "Beverly Hills", 
		  	"country": "US", 
		    	"firstName": "John", 
		    	"lastName": "Doe", 
		    	"middleName": "", 
		    	"phoneNumber": "5088675309", 
		    	"postalCode": "90210", 
		    	"state": "CA"
		}
	}, 
	"skuId": str(skuId), 
	"styleColor": str(styleCode)
}
#sku eg=>
#https://api.nike.com/commerce/productsize/products/848692-033/availability?country=US&channel=SNKRS
raw_input('Press Enter to send request...')
##stubbed for safety->
entryResp=session.post(entry,data=json.dumps(entryPayload),headers=entryHeaders)
print entryResp.json()