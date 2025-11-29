import requests
from requests.auth import HTTPBasicAuth
import base64
from  datetime import datetime
CONSUMER_KEY = "dudrAo3eYowBFA9EDD0rrbpmXwXwYG9m"
CONSUMER_SECRET = "JDhu1tm42MF8LTAW"
PASSKEY = "34ca40fe8e5d89015d85c835f80b2073778635c5e8f7ee0cb1df002702af2bfb"
BUSINESS_SHORT_CODE = 825770

def encode(string):
	encode_data = base64.b64encode(string.encode('utf-8'))
	decode_data = encode_data.decode('utf-8')
	return decode_data

def get_access_token():

	url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
	data = requests.get(url,auth = HTTPBasicAuth(CONSUMER_KEY,CONSUMER_SECRET)).json()
	return data['access_token']

def STKPush(phonenumber,amount,narration):
	token = get_access_token()
	now = datetime.now()
	timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
	base64_string = encode(str(BUSINESS_SHORT_CODE)+PASSKEY+timestamp)
	headers = {
		'Authorization': "Bearer " + token,
		"Content-Type": "application/json"
	}
	payload = {
		"BusinessShortCode": BUSINESS_SHORT_CODE,
		"Password": base64_string,
		"Timestamp": timestamp,
		"TransactionType": "CustomerPayBillOnline",
		"Amount": amount,
		"PartyA": phonenumber,
		"PartyB": BUSINESS_SHORT_CODE,
		"PhoneNumber": phonenumber,
		"CallBackURL": "https://ruaraka.methodistkenya.org/api/mpayments/acknowledge-payments/",
		"AccountReference": narration,
		"TransactionDesc": narration
	}
	response = requests.post('https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json=payload, headers=headers)
	return response
