from flask import Flask, render_template, url_for, request, redirect

from searchers.all import build_searcher
import httplib2

app = Flask(__name__)


class Server(object):

	@app.route('/', methods=['GET', 'POST'])
	def index():
		print "Someone is at the home page."
		return render_template('welcome_page.html')

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

	@app.route('/results/', methods=['GET', 'POST'])
	def results():
		if request.method == 'POST':
			data = request.form
		else:
			data = request.args

		query = data.get('searchterm')
		dbType = data.get('searchDatabase')
		table = data.get('library')

		searcher = build_searcher()
		results = []
		if(dbType == 'mongo'):
			# Fetches results from the mongo database. 
			# It toggles the search table based on user selected drop down
			if table == 'players':
				results = searcher.mongo.players.search(query)
			else:
				results = searcher.mongo.restaurants.search(query)
				
		else:
			# Queries the whoosh index for the user specified table.
			results = searcher.whoosh.search(query, table).documents

		return render_template('results.html', query=query, results=results)

	def run(self, isDebug):
		app.run(debug=isDebug)
