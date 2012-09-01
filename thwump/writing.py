import whoosh.writing

class IndexWriter(whoosh.writing.IndexWriter):
	def __init__(self, index):
		self.index = index

	def add_document(self, **fields):
		self.index.collection.insert(fields)

	def add_reader(self):
		raise NotImplementedError("stubbed")

	def delete_document(self, docnum, delete=True):
		self.index.collection.remove(docnum)
