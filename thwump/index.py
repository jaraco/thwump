import pymongo
import whoosh.index

from . import reading
from . import writing

class Index(whoosh.index.Index):
	database_name = 'thwump'
	collection_name = 'index'
	def __init__(self, schema=None, connection_factory=pymongo.Connection):
		self.schema = schema
		self.connection = connection_factory()
		self.collection = self.connection[self.database_name][
			self.collection_name]

	def is_empty(self):
		return not self.doc_count()

	def reader(self, reuse=None):
		return reuse or reading.IndexReader(self)

	def writer(self, **kwargs):
		return writing.IndexWriter(self)
