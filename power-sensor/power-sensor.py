import urllib, json
import time
import urllib2

while True:
	url = "http://192.168.25.76/emoncms/nodes/5/rx/1?apikey=2648851abbda99e007df14377d7381e7"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	data['timestamp'] = time.time()
	payload = json.dumps(data)
	api = "http://34.192.244.29/energyData/"
	req = urllib2.Request(api, payload, {'Content-Type': 'application/json'})
	f = urllib2.urlopen(req)
	response = f.read()
	f.close()
	time.sleep(3)
