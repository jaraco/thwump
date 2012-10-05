import whoosh.writing

class IndexWriter(whoosh.writing.IndexWriter):
	def __init__(self, index):
		self.index = index

	@property
	def schema(self):
		return self.index.schema

	def add_document(self, **fields):
		self.index.collection.insert(fields)

	def add_reader(self, reader):
		"""
		Add the documents from the reader to the writer (?). Parent class
		doesn't document what this is supposed to do.
		Return None
		"""
		for item in reader.index.collection.find():
			self.index.insert(item)

	def delete_document(self, docnum, delete=True):
		self.index.collection.remove(docnum)
