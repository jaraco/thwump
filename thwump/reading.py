import whoosh.reading

class IndexReader(whoosh.reading.IndexReader):
	def __init__(self, index):
		self.index = index

	def __contains__(self, term):
		"""
		Returns True if the given term tuple (fieldname, text) is
		in this reader.
		"""
		fieldname, text = term
		query = dict(fieldname=fieldname, text=text)
		return bool(self.index.collection.find(query).count())

	def __iter__(self):
		"""
		Yields (fieldname, text, docfreq, indexfreq) tuples for each term in
		the reader, in lexical order.
		"""
		fields = 'fieldname', 'text', 'docfreq', 'indexfreq'
		cur = self.index.collection.find(fields=fields).sort('fieldname')
		return (tuple(rec[field] for field in fields) for rec in cur)

	def iter_from(self, fieldname, text):
		"""
		Yields (field_num, text, doc_freq, index_freq) tuples for all terms in
		the reader, starting at the given term.
		"""
		fields = 'fieldname', 'text', 'docfreq', 'indexfreq'
		cur = self.index.collection.find(fields=fields).sort('fieldname')
		return (tuple(rec[field] for field in fields) for rec in cur
			if rec['fieldname'] >= fieldname)

	def stored_fields(self, docnum):
		"""
		Returns the stored fields for the given document number.
		"""
		return self.index.collection.get(docnum).keys()

	def doc_count_all(self):
		"""
		Returns the total number of documents, DELETED OR UNDELETED, in this
		reader.
		"""
		return self.index.collection.count()

	def doc_count(self):
		"""
		Returns the total number of UNDELETED documents in this reader.
		"""
		return self.index.collection.count()

	def doc_field_length(self, docnum, fieldname, default=0):
		"""
		Returns the number of terms in the given field in the given document.
		This is used by some scoring algorithms.
		"""
		doc = self.index.collection.get(docnum, fields=[fieldname])
		field = doc['field']
		return len(field)

	def doc_frequency(self, fieldname, text):
		"""
		Returns how many documents the given term appears in.
		"""
		query = {fieldname: text}
		return self.index.collection.find(query).count()

	def field_length(self, fieldname):
		"""
		Returns the total number of terms in the given field. This is used by
		some scoring algorithms.
		"""
		# todo: is this right?
		query = {fieldname: {'$exists': 1}}
		return self.index.collection.find(query).count()
