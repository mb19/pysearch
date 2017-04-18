
import sys, os

from indexes import SchemaBuilder, IndexManager
import json
import os
import argparse
import datetime

class Builder(object):

	def __setup(self, db):
		""" Gets the maximum size of the index fields and caches it if needed. """
		if os.path.exists("stats.json"):
			# use cached database size info for schema.
			js = open('stats.json')
			data = json.load(js)
			return data["size"]

		# Need to calculate max index field size.
		builder = SchemaBuilder()
		biggestRecord = builder.find_max_info(db)

		with open('stats.json', 'w') as outfile:
			json.dump({'size': biggestRecord[0]}, outfile)

		return biggestRecord[0]

	def __main(self, settings, arg):
		db = settings.db
		indexSize = self.__setup(db)
		# arg = self.__get_args()
		manager = IndexManager(arg["index"], indexSize, db)

		if arg['build'] == True:
			# Build index with the specified name
			print "Building index..."
			# Now build the index
			manager.build()
			print "Done building index."
		else:
			# Do search
			print "Searching index..."
			results = manager.search(arg['search'])
			print "Done searching index."

			print "==== Documents Returned in {0} s: {1} ====".format(results.time, len(results.documents))
			for doc in results.documents:
				if arg['expand']:
					# Print everything, score and document.
					print doc
				else:
					# Condensed vesion, only print top 5 properties.
					val = doc['document']
					print "{0}, {1}, {2}, {3}, {4}".format(val['prop1'], val['prop2'], val['prop3'], val['prop4'], val['prop5'])

		return 0

	def build(self, settings, args):
		return self.__main(settings, args)

