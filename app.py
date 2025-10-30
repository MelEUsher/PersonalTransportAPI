from flask import Flask, render_template, request, redirect, url_for, make_response
from geopy.distance import distance as geodesic
import json, werkzeug
from http import HTTPStatus

app=Flask(__name__)

# root
@app.route('/')
def home():
	return redirect(url_for('view_all_available'))
	
@app.route('/view_all_available')
def view_all_available():
	db = init_db()
	available_bikes = [bike for bike in db if not bike.is_reserved]
	available_bikes_dictlist = convert_db_to_dictlist(available_bikes)
	return json.dumps(available_bikes_dictlist), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return a json-ified list of all the bikes with status 200


# Search for bikes
@app.route('/search', methods=['GET'])
def search():
	# Search for bikes in the database
	# parse request params
	try:
		search_lat, search_lng, search_radius = \
			float(request.args['lat']), \
			float(request.args['lng']), \
			float(request.args['radius'])	# parse request for search criteria
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	except ValueError:
		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	# validate lat and long values
	if not -90 <= search_lat <= 90:
		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	if not -180 <= search_lng <= 180:
		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	
	db = init_db()	# initialize db

	search_results = []
	for bike in db:
		# Calculate distance between the bike location point and the search location point, in metres
		distance = geodesic((bike.lat, bike.lng), (search_lat, search_lng)).m
		if distance <= search_radius and not bike.is_reserved:
			# this bike is available and within the search area
			search_results.append({	'id':bike.id, 
									'lat':bike.lat, 
									'lng':bike.lng
								  })
			
	return json.dumps(search_results), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# return json-ified search results list with status 200

	
# Start a reservation 
@app.route('/reservation/start', methods=['GET'])
def start_reservation():
	# parse request params
	try:
		reserve_id = request.args['id']	# parse request for id of bike to be reserved
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	db = init_db()
	
	# try and find the bike with specified id
	bike = get_bike_with_id(reserve_id, db)
	if bike:
		# reserve if possible
		if not bike.is_reserved:
			# bike can be reserved
			bike.is_reserved = True
			write_db(db)	# update db
			success = { 'msg': f'Bike {reserve_id} was reserved successfully.' }
			return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200

		else:
			# the bike is already reserved
			error = { 'msg': f'Error 422 - Bike with id {reserve_id} is already reserved.' }
			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	else:
		# no bike with the reserve id was found
		error = { 'msg': f'Error 422 - No bike with id {reserve_id} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# End a reservation
@app.route('/reservation/end', methods=['GET'])
def end_reservation():
	# parse request params
	try:
		bike_id_to_end = request.args['id']	# parse request for id of bike whose reservation to be ended
		end_lat, end_lng = \
			float(request.args['lat']), \
			float(request.args['lng'])
		db = init_db()
	except werkzeug.exceptions.BadRequestKeyError:
		# the required parameters are not present in the search query
		error = { 'msg': 'Error 422 - Please include all required parameters in search query' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	except ValueError:
		error = { 'msg': 'Error 422 - Lat/Lng values must be numbers' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422

	# validate lat and long values
	if not -90 <= end_lat <= 90:
		error = { 'msg': 'Error 422 - Latitude must be in the [-90, 90] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	if not -180 <= end_lng <= 180:
		error = { 'msg': 'Error 422 - Longitude must be in the [-180, 180] range.'}
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
		
	# try and find the bike with specified id
	bike = get_bike_with_id(bike_id_to_end, db)
	if bike:
		# end reservation if possible
		if bike.is_reserved:
			# bike is reserved and can be ended
			
			# initiate payment
			payment_response = pay(bike, end_lat, end_lng)
			if payment_response['status']:
				# the payment was completed successfully
				
				# update bike's reserved status and location
				bike.is_reserved = False
				bike.lat, bike.lng = end_lat, end_lng
				write_db(db)
				# construct successful response
				success =	{	'msg': f'Payment for bike {bike_id_to_end} was made successfully and the reservation was ended.',
								'txn_id': payment_response['txn_id']
							}
				return json.dumps(success), HTTPStatus.OK.value, {'Content-Type':'application/json'}	# respond with status 200
			else:
				# the payment failed for some reason
				error = { 'msg': payment_response['msg'] }
				response_code = payment_response['code']
				return json.dumps(error), response_code, {'Content-Type':'application/json'}
		else:
			# the bike is not currently reserved
			error = { 'msg': f'Error 422 - No reservation for bike {bike_id_to_end} presently exists.' }
			return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422
	else:
		# no bike with the id was found
		error = { 'msg': f'Error 422 - No bike with id {bike_id_to_end} was found.' }
		return json.dumps(error), HTTPStatus.UNPROCESSABLE_ENTITY.value, {'Content-Type':'application/json'}	# respond with status 422


# ==================
#  HELPER FUNCTIONS	
# ==================


def pay(bike, end_lat, end_lng):
	# Initialise the payment process
	# construct location point tuples
	old_location = (bike.lat, bike.lng)
	new_location = (end_lat, end_lng)
	# calculate distance between points, in metres
	distance_ridden = geodesic(old_location, new_location).m
	distance_ridden = round(distance_ridden)
	# calculate cost (currently a dummy function that returns the distance as the cost)
	cost = calculate_cost(distance_ridden)	# returns cost = distance for now
	# redirect to payment gateway and return response (currently a dummy function that returns a hypothetical transaction id)
	return payment_gateway(cost)	# returns hypothetical success and txn id for now
	
def payment_gateway(cost):
	# TODO: Implement real payment processing in future
	txn_id = 379892831
	return 	{	'status': True,
				'txn_id': txn_id
			}

def calculate_cost(distance):
	# TODO: Implement meaningful cost calculation in future
	return distance

		
def init_db():
	db_json = open('bike_db.json', 'r').read()
	db_list = json.loads(db_json)
	# populate Bike objects for easier access later
	db = []
	for bike in db_list:
		bike_obj = Bike(	bike['id'], 
								bike['lat'], 
								bike['lng'], 
								bike['is_reserved']
							 )
		db.append(bike_obj)
	return db
	
	
def get_bike_with_id(search_id, db):
	try:
		bike = next(bike for bike in db if bike.id == search_id)	# get the bike with specified id
		return bike
	except StopIteration:
		# no bike with the id was found
		return None
	

def write_db(db):
	# serialize Bike objects 
	db_list = convert_db_to_dictlist(db)
	db_json = json.dumps(db_list)
	open('bike_db.json', 'w').write(db_json)
	return True
		
# class bike for internal use
class Bike:
	def __init__(self, bike_id, lat, lng, is_reserved):
		self.id = bike_id
		self.lat = lat
		self.lng = lng
		self.is_reserved = is_reserved
	
	def to_dict(self):
		return {	'id':self.id, 
					'lat':self.lat, 
					'lng':self.lng, 
					'is_reserved':self.is_reserved
			   }
		
def convert_db_to_dictlist(db):
	db_list = []
	for bike in db:
		db_list.append(bike.to_dict())
	return db_list
		


if __name__== "__main__":
	# TODO: Turn debug flag off for production system
	app.run('localhost', 8080)