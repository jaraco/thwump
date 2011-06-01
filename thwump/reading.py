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
