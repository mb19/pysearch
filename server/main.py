from flask import Flask, render_template, url_for, request
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
		#query = request.form['searchterm']
		resType = ['Team', 'Team', 'Team']
		title = ['Seahawks', 'Raiders', 'Steelers']
		location = ['Seattle', 'Oakland', 'Pittsburgh']
		states = ['Washington', 'California', 'Pennsylvania']
		links = ['https://en.wikipedia.org/wiki/Seattle_Seahawks', 'https://en.wikipedia.org/wiki/Oakland_Raiders', 'https://en.wikipedia.org/wiki/Pittsburgh_Steelers']
		return render_template('results.html', query=query, results=zip(resType, title, location, states, links))

	def run(self, isDebug):
		app.run(debug=isDebug)
