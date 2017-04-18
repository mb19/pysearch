
import sys, os

from indexes import SchemaBuilder, IndexManager
import json
import os
import argparse
import datetime

class Builder(object):
	def __main(self, db, indexName):
		manager = IndexManager(indexName, db)

		# Build index with the specified name
		print "Building index..."
		# Now build the index
		manager.build()
		print "Done building index."


		# if arg['build'] == True:
			
		# else:
		# 	# Do search
		# 	print "Searching index..."
		# 	results = manager.search(arg['search'])
		# 	print "Done searching index."

		# 	print "==== Documents Returned in {0} s: {1} ====".format(results.time, len(results.documents))
		# 	for doc in results.documents:
		# 		if arg['expand']:
		# 			# Print everything, score and document.
		# 			print doc
		# 		else:
		# 			# Condensed vesion, only print top 5 properties.
		# 			val = doc['document']
		# 			print "{0}, {1}, {2}, {3}, {4}".format(val['prop1'], val['prop2'], val['prop3'], val['prop4'], val['prop5'])

		# return 0

	def build(self, db, indexName):
		return self.__main(db, indexName)

