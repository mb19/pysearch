
class IndexSearcher(object):

	def search(self, text):
		raise NotImplementedError("Must subclass to use this method.")

class SearchResult(object):
	def __init__(self, top_relevant, total_relevant):
		self.top_relevant = top_relevant
		self.total_relevant = total_relevant

	def calculate_precision(self, relevant):
		if float(self.top_relevant) == 0:
			return 0
		return float(relevant) / float(self.top_relevant)

	def calculate_recall(self, relevant):
		if float(self.total_relevant) == 0:
			return 0

		return float(relevant) / float(self.total_relevant)

	def calculate_f_measure(self, relevant):
		precision = self.calculate_precision(relevant)
		recall = self.calculate_recall(relevant)

		multiplied = 2 * precision * recall
		added = precision + recall

		if added == 0: 
			return 0
		return multiplied / added

	def serialize(self):
		return {
			'top_relevant': self.top_relevant,
			'total_relevant': self.total_relevant
		}

