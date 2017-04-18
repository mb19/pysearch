from flask import Flask, render_template, url_for, request

from searchers.all import build_searcher

app = Flask(__name__)


class Server(object):

	@app.route('/', methods=['GET', 'POST'])
	def index():
		print "Someone is at the home page."

		return render_template('welcome_page.html')

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
