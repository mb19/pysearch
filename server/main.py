from flask import Flask, render_template, url_for, request, redirect, make_response, jsonify
import socket
from searchers.all import build_searcher
from searchers.base import SearchResult
import httplib2
import urllib

app = Flask(__name__)

def fetch_data(term, db, lib, limit=10):
	searcher = build_searcher()
	results = []
	if(db == 'mongo'):
		# Fetches results from the mongo database. 
		# It toggles the search table based on user selected drop down
		if lib == 'players':
			results = searcher.mongo.players.search(term, limit)
		elif lib == 'restaurants':
			results = searcher.mongo.restaurants.search(term, limit)
			
	elif db == 'whoosh':
		# Queries the whoosh index for the user specified table.
		results = searcher.whoosh.search(term, lib, limit)

	return results


class Server(object):

	@app.route('/', methods=['GET', 'POST'])
	def index():
		server = socket.gethostname()
		return render_template('welcome_page.html', server=server)

	@app.route('/navigate', methods=['GET'])
	def navigate():
		data = request.args
		if len(data) != 1:
			# Error page.
			return redirect("/bad_request")
		else:
			h = httplib2.Http()

			def is_valid(method):
				resp = h.request(data['url'], method)
				print resp[0]['status']
				return int(resp[0]['status']) < 400

			if is_valid('HEAD') or is_valid('GET'):
				# redirect to the webpage.
				return redirect(data['url'])
			else:
				# failure, go to failed page.
				return redirect("/not_found")


	@app.route('/not_found')
	def error_404():
		error = "404 - Not Found: The requested resource does not exist."
		return render_template('error.html', error=error)

	@app.route('/bad_request')
	def error_400():
		error = "400 - Bad Request: The request was malformed or could not be processed."
		return render_template('error.html', error=error)

	@app.route('/api/query', methods=['GET'])
	def query():
		data = request.args

		def makeError():
			return make_response(jsonify({'error': 'Missing arguements'}), 400)
			
		if len(data) is not 4: 
			return makeError()

		if not data.has_key('term') or not data.has_key('db') or not data.has_key('lib') or not data.has_key('limit'):
			return makeError()

		term = data.get('term')
		db = data.get('db')
		lib = data.get('lib')
		limit = data.get('limit')

		if term == '' or db == '' or lib == '' or limit == '':
			return makeError()

		results = fetch_data(term, db, lib, int(limit))
		results['stats'] = results['stats'].serialize()

		return jsonify(results)

	@app.route('/api/measure', methods=['POST'])
	def measure():
		data = request.form

		def makeError():
			return make_response(jsonify({'error': 'Missing arguements'}), 400)
			
		if len(data) is not 3: 
			return makeError()

		if not data.has_key('top') or not data.has_key('total') or not data.has_key('relevant'):
			return makeError()

		top = data.get('top')
		total = data.get('total')
		relevant = data.get('relevant')

		if top == '' or total == '' or relevant == '':
			return makeError()

		intTop = int(top)
		intTotal = int(total)

		stats = SearchResult(top, total)
		return jsonify({
			'precision': stats.calculate_precision(relevant),
			'recall': stats.calculate_recall(relevant),
			'f-measure': stats.calculate_f_measure(relevant)
		})

	@app.route('/results/', methods=['GET', 'POST'])
	def results():
		if request.method == 'POST':
			data = request.form
		else:
			data = request.args

		query = data.get('searchterm')
		dbType = data.get('searchDatabase')
		table = data.get('library')
		propNames = []
		if table == 'players': 
			propNames = ['Name', 'Position', 'Number', 'Team' ]
		else:
			propNames = ['Name', 'Rating', 'City', 'State']

		results = fetch_data(query, dbType, table)

		for doc in results['documents']:
			doc['document']['prop5'] = urllib.quote_plus(doc['document']['prop5'])

		return render_template('results.html', 
			query=query, 
			results=results['documents'], 
			actual=results['stats'].top_relevant, 
			total=results['stats'].total_relevant,
			propNames=propNames)

	def run(self, isDebug):
		app.run(debug=isDebug, host="0.0.0.0")
