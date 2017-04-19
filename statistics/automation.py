
from requests import request
import os

class Configuration(object):
	
	terms = ['apple', 'pepper', 'bar', 'john', 'phillip', 'Seattle', 'Oregon']
	databases = ['mongo', 'whoosh']
	tables = ['restaurants', 'players']

	def build(self):
		parameters = []
		for term in self.terms:
			for db in self.databases:
				for table in self.tables:
					param = {
						'term': term,
						'db': db,
						'table': table,
						'relevant': 'no',
						'mapping': {}
					}
					if db == 'player':
						param['mapping'] = self.__player_mapping()
					else:
						param['mapping'] = self.__restaurant_mapping()
						
					parameters.append(param)
		return parameters

	def __player_mapping(self):
		return {
			"prop1": "name",
			"prop2": "position",
			"prop3": "number",
			"prop4": "team",
			"prop5": "url"
		}

	def __restaurant_mapping(self):
		return {
			"prop1": "name",
			"prop2": "rating",
			"prop3": "city",
			"prop4": "state",
			"prop5": "url"
		}

class Pass(object):

	def __init__(self, id, payload):
		self.id = id
		self.payload = payload
		self.baseUrl = 'http://127.0.0.1:5000/api'

	def execute(self, calculate=False):
		if calculate:
			self.__calculate()
		else:
			self.__get_stats()

	def __calculate(self):
		pass

	def __get_stats(self):
		query = '{0}/query?lib={1}&db={2}&term={3}&limit=10'.format(
			self.baseUrl,
			self.payload['table'],
			self.payload['db'],
			self.payload['term']
		)

		response = request('GET', query)
		data = response.json()
		self.__output_as_tsv(data)

	def __output_as_tsv(self, stats):
		filename = self.__get_file_name()

		with open(filename, 'a') as tsv:
			rows = []
			# write header
			ordered = self.__get_ordered_mapping()
			rows.append(self.__make_headers())

			for stat in stats['documents']:
				rows.append(self.__make_row(stat['document']))

			tsv.writelines(rows)

	def __get_file_name(self):
		if not os.path.exists("statistics/results"):
			os.mkdir("statistics/results")

		filename = 'statistics/results/pass{0}.tsv'.format(self.id)
		return filename


	def __make_headers(self):
		baseHeaders = "database\ttable\tquery"

		propHeaders = reduce(
			lambda curr, prev: "{0}\t{1}".format(curr, prev), 
			map(lambda (k, v): v, self.__get_ordered_mapping())
		)
		return "{0}\t{1}\t{2}\n".format(baseHeaders, propHeaders, "Is Relevant?")

	
	def __make_row(self, row):
		return "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\n".format(
			self.payload['db'],
			self.payload['table'],
			self.payload['term'],
			row['prop1'],
			row['prop2'],
			row['prop3'],
			row['prop4'],
			row['prop5'],
			'0'
		)

	def __get_ordered_mapping(self):
		return iter(sorted(self.payload['mapping'].items()))

# class Scores(object):

# 	def __init__(self):
# 		self.passes = []

# 	def add(self, completedPass):
# 		self.passes.append()

configs = Configuration().build()
passA = Pass(0, configs[0])
passA.execute()