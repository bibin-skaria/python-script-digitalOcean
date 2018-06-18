#!/usr/bin/python3

import requests
import json

#token of my digital ocean account
TOKEN = "1930907adb94092e01039ad0892a87368fafb66f2c863addb4a01026cc0b959e"

#api of digital ocean for sending or reciving requests
ENDPOINT = "https://api.digitalocean.com/v2"

# each request consist of header and data and this "HEADER" is the header of our request header
HEADER = {'Content-type': 'application/json' , "Authorization": "Bearer %s" % TOKEN}

#function to fetch info of droplet in my digi ocean account
def digiO_info():

#now for requesting api and for droplets we use SOURCE_URL
	SOURCE_URL = ENDPOINT + '/droplets'

#sending request to get json file of droplets
	DROPLETPCK = requests.get(SOURCE_URL,headers=HEADER).json()['droplets']

#to convert json into dictory for our use
	OUTPUT_DICT = {}

	for Droplet in DROPLETPCK:
		ID = Droplet['id']
		NAME = Droplet['name']
		RAM = Droplet['memory']
		CPU = Droplet['vcpus']
		DISK = Droplet['disk']
		IPV4 = Droplet['networks']['v4'][0]['ip_address']
		IPV6 = None if len(Droplet['networks']['v6']) == 0 else Droplet['network']['v6'][0]['ip_address']
		OS = Droplet['image']['slug']
		STATUS = Droplet['status']
		TAGS = Droplet['tags']

		OUTPUT_DICT[ID] = {'name':NAME , 'ram':RAM , 'cpu':CPU , 'disk':DISK , 'ipv4':IPV4 , 'ipv6':IPV6 , 'os':OS , 'status':STATUS , 'tags':TAGS }

	return OUTPUT_DICT
	
###########################################
# to shutdown droplet function

def digiO_shutdown_droplet(ID):
	ID=str(ID)
	SOURCE_URL = ENDPOINT + '/droplets/' + ID + '/actions'
	RESPONSE = requests.post(SOURCE_URL, headers=HEADER , data='{"type":"shutdown"}').json()['action']
	status = RESPONSE['status']
	if status in ["in-progress", "completed"]:
		return True
	else:
		return False
##########################################
# to power on droplet fuction

def digiO_poweron_droplet(ID):
	ID=str(ID)
	SOURCE_URL =  ENDPOINT + '/droplets/' + ID + '/actions'
	RESPONSE = requests.post(SOURCE_URL, headers=HEADER , data='{"type":"power_on"}').json()['action']
	status = RESPONSE['status']
	if status in ["in-progress", "completed"]:
		return True
	else:
		return False

##########################################

def do_ssh_copykey(KEYNAME, TO_TOKEN):
	TO_ENDPOINT ="https://api.digitalocean.com/v2"
	TO_HEADERS = {'Content-type': 'application/json', "Authorization": "Bearer %s" % TO_TOKEN}

	templist = []
	API_URL = ENDPOINT + '/account/keys'
	try:
		RESPONSE = requests.get(API_URL, headers=HEADERS)
		if RESPONSE.status_code ==200:
			for keyInfo in RESPONSE.json()['ssh_keys']:
				keyPub = keyInfo['public_key']
				tempList.append(keyPub)
			if tempList:
				for key in tempList:
					DATA = json.dumps({"name":KEYNAME , "public_key":key})
					RESPONSE = requests.post('https://api.digitalocean.com/v2/account/keys' , headers=TO_HEADERS , data=DATA)
					print('copying Key :', end= '')
					if RESPONSE.status_code == 201:
						print('OK')
					else:
						print('FAILED')
			else:
				return False
		else:
			return False
	except Exception as err:
		print(err)
##################################################################
def do_tags_getall():
	try:
		tempDict = {}
		api_url = ENDPOINT + "/tags"
		RESPONSE = requests.get(api_url, headers=HEADERS).json()
		for tagDict in RESPONSE['tags']
			dropletCount= tagDict['resources']['droplets']['count']
			tagName = tagDict['name']
			tagDict[tagName] = dropletCount
		return tempDict
	except Exception as err:
		print(err)
