from flask import Flask, jsonify
from flask import make_response, request
import json
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient

#from app import app
app = Flask(__name__)

connection = MongoClient("mongo_instance_001", 27017)
db = connection.SmartHomeDB
db2 = connection.Luminosity

def toJson(data):
	"""Convert Mongo object(s) to JSON"""
	return json.dumps(data, default=json_util.default)

@app.route('/')

@app.route('/index')
def index():
        return 'SmartHome RESTful API'

@app.route('/energyData/', methods=['GET'])
def showAll_energyData():
	"""Return a list of all companies energyData
	ex) GET /energyData/?limit=10&offset=20
	"""
	if request.method == 'GET':
		lim = int(request.args.get('limit', 100))
		off = int(request.args.get('offset', 0))
		results = db['SmartHomeDB'].find().skip(off).limit(lim)
		json_results = []
	for result in results:
  		json_results.append(result)
	return toJson(json_results)

@app.route('/luminosity/', methods=['GET'])
def showAll_luminosity():
	"""Return a list of all LUMINOSITY DATA
	ex) GET /luminosity/?limit=10&offset=20
	"""
	if request.method == 'GET':
		lim = int(request.args.get('limit', 100))
		off = int(request.args.get('offset', 0))
		results = db2['Luminosity'].find().skip(off).limit(lim)
		json_results = []
	for result in results:
  		json_results.append(result)
	return toJson(json_results)

@app.route('/energyData/<energyData_id>', methods=['GET'])
def showCompany_energyData(energyData_id):
	"""Return specific Company energyData
	ex) GET /energyData/123456
	"""
	if request.method == 'GET':
		""" To get the last LUMINOSITY record
		ex: results = db['Luminosity'].find().sort("timestamp",-1).limit(1)
		"""
		result = db['SmartHomeDB'].find_one({'_id': ObjectId(energyData_id)})
		return toJson(result)

@app.route('/energyData/', methods = ['POST'])
def create_energyData():
	if not request.json or not 'Customer' in request.json:
		abort(400)
	energyData = {
		'unit': request.json['unit'],
		'name': request.json['name'],
		'value': request.json['value'],
		'timestamp': request.json['timestamp'],
	}
	Datas = db['SmartHomeDB'].insert(energyData)
	
	results = db['SmartHomeDB'].find().skip(0).limit(10)
	json_results = []
	for result in results:
		json_results.append(result)
	return toJson(json_results), 201

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True, port=80)
