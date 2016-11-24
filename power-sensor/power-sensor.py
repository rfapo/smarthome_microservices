import urllib, json
import time
import requests

while True:
	url = "http://192.168.25.76/emoncms/nodes/5/rx/1?apikey=2648851abbda99e007df14377d7381e7"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	data['timestamp'] = time.time()
	payload = json.dumps(data)
	api = "http://34.192.244.29/energyData/"
	headers = {'Content-Type': 'application/json'}
	response = requests.post(api, data=payload, headers=headers)
	time.sleep(3)
