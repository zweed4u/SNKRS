import json, requests

print '\n'
session=requests.Session()

first=raw_input('First Name: ')
last=raw_input('Last Name: ')
email=raw_input('Nike Account Email: ')
password=raw_input('Nike Account Password: ')
mobilePhone=raw_input('10 Digit Mobile: (no dashed or parentheses) ')
address=raw_input('Street Address: ')
city=raw_input('City: ')
zipCode=raw_input('zipCode: ')
state=raw_input('State: (eg. NY) ')
country=raw_input('Country: (eg. US) ')
print '\n'

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
	"username":email,
	"password":password,
	"client_id":"G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj",
	"ux_id":"com.nike.commerce.snkrs.ios",
	"grant_type":"password"
}

loginUrl='https://unite.nikecloud.com/login?locale=en_US&backendEnvironment=identity'
loginResponse=session.post(loginUrl,data=json.dumps(loginPayload),headers=loginHeaders)

user_id=str(loginResponse.json()['user_id'])
access_token=str(loginResponse.json()['access_token'])
refresh_token=str(loginResponse.json()['refresh_token'])

print 'user_id: '+str(user_id)
print 'access_token: '+str(access_token)
print 'refresh_token: '+str(refresh_token)
print '\n'

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
	"country": country, 
    	"currency": "USD", 
    	"email": email, 
    	"locale": "en_US"

}
checkoutUrl='https://api.nike.com/orders/v1/orders/checkouts'
checkoutResponse=session.post(checkoutUrl,data=json.dumps(checkoutPayload),headers=checkoutHeaders)
checkoutId=checkoutResponse.json()['id']
print 'checkoutId: '+str(checkoutId)
print '\n'

entryHeaders={                                                                                      
	'Content-Type':'application/json; charset=UTF-8',                                                                                                            
	'Origin':'https://www.nike.com',                                                                                                         
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
        	"email": email, 
        	"mobilePhone": "+1"+str(mobilePhone), 
        	"shippingAddress": {
            		"address1": address, 
            		"address2": "", 
		    	"address3": "", 
		    	"city": city, 
		    	"country": country, 
		    	"firstName": first, 
		    	"lastName": last, 
		    	"middleName": "", 
		    	"phoneNumber": str(mobilePhone), 
		    	"postalCode": str(zipCode), 
		    	"state": str(state)
        	}
    	}, 
    	"skuId": "17185630", 
    	"styleColor": "869611-001"
}
#sku eg=>
#https://api.nike.com/commerce/productsize/products/869611-001/availability?country=US&channel=SNKRS

entry='https://api.nike.com/commerce/launchwaitline/launch/waitline/turnToken'
raw_input('Press Enter to send Request...')
entryResponse=session.post(entry,data=json.dumps(entryPayload),headers=entryHeaders)

print entryResponse.json()
print '\n'

#if not desired response, mus get new checkoutId
