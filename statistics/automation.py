
from requests import request, post
import os
import json


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

	def __output_meta(self, stat):
		filename = self.__get_file_name("meta")

		with open(filename, 'w') as tsv:
			content = "{0}\t{1}\n".format(
				stat['stats']['top_relevant'],
				stat['stats']['total_relevant'],
			)
			tsv.write(content)

	def __output_as_tsv(self, stats):
		filename = self.__get_file_name()

		with open(filename, 'w') as tsv:
			rows = []
			# write header
			ordered = self.__get_ordered_mapping()
			rows.append(self.__make_headers())

			for stat in stats['documents']:
				rows.append(self.__make_row(stat['document']))

			tsv.writelines(rows)
		self.__output_meta(stats)

	def __get_file_name(self, suffix=''):
		if not os.path.exists("statistics/results"):
			os.mkdir("statistics/results")

		filename = 'statistics/results/pass{0}{1}.tsv'.format(self.id, suffix)
		return filename


	def __make_headers(self):
		baseHeaders = "database\ttable\tquery"

		propHeaders = reduce(
			lambda curr, prev: "{0}\t{1}".format(curr, prev), 
			map(lambda (k, v): v, self.__get_ordered_mapping())
		)
		return "{0}\t{1}\t{2}\n".format(baseHeaders, propHeaders, "Is Relevant?")

	
	def __make_row(self, row):
		for key in row:
			if type(row[key]) == unicode:
				row[key] = row[key].replace(u'\ufeff', '')

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

class Scorer(object):

	def __init__(self, id, payload):
		self.id = id
		self.payload = payload

	def read(self):
		meta = {
			'top_relevant': '',
			'total_relevant': ''
		}

		datafile = self.__get_file_name()
		metafile = self.__get_file_name("meta")

		with open(metafile, 'r') as tsv:
			content = tsv.readline().strip().split('\t')
			meta['top_relevant'] = content[0]
			meta['total_relevant'] = content[1]

		rows = []

		with open(datafile, 'r') as tsv:
			# Skip the header
			sawHeader = False
			for line in tsv.readlines():
				if not sawHeader:
					sawHeader = True
					continue

				content = line.strip().split('\t')

				data = {
					'prop1': content[3],
					'prop2': content[4],
					'prop3': content[5],
					'prop4': content[6],
					'prop5': content[7],
					'relevant': content[8]
				}
				rows.append(data)

		return {
			'stats': meta,
			'documents': rows,
			'query': self.payload
		}

	def __get_file_name(self, suffix=''):
		if not os.path.exists("statistics/results"):
			os.mkdir("statistics/results")

		filename = 'statistics/results/pass{0}{1}.tsv'.format(self.id, suffix)
		return filename


class Statistics(object):

	configs = Configuration().build()

	def build_data(self):
		id = 0
		total = len(self.configs)
		for config in configs:
			print "Running pass {0}/{1}\n".format(id + 1, total)
			nextPass = Pass(id, self.configs[id])
			nextPass.execute()
			id += 1

	def process_scores(self):
		id = 0
		total = len(self.configs)
		results = []
		for config in self.configs:
			result = self.__handle_metric(id)
			del config['mapping']
			data = {
				'query': config,
				'results': result
			}
			results.append(data)
			id += 1

		self.__write_output(results)

		return results

	def __write_output(self, results):
		filename = 'statistics/final-statistics.json'
		with open(filename, 'w') as output:
			output.write(json.dumps(results, sort_keys=True, indent=4))

	def __handle_metric(self, id):
		scorer = Scorer(id, self.configs[id])
		payload = scorer.read()

		def calculate_relevant(data):
			totalRelevant = 0
			for document in data['documents']:
				if document['relevant'] == '1':
					totalRelevant += 1
			return totalRelevant

		relevantCount = calculate_relevant(payload)

		return self.__post_stats(payload['stats']['top_relevant'], 
			payload['stats']['total_relevant'], 
			relevantCount)

	def __post_stats(self, top, total, relevant):
		url = 'http://127.0.0.1:5000/api/measure'
		body = {
			'top': int(top),
			'total': int(total),
			'relevant': int(relevant)
		}
		response = post(url, data = body)
		return response.json()

stats = Statistics()

#stats.build_data()
print stats.process_scores()