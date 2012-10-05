import bson
import whoosh.writing

class IndexWriter(whoosh.writing.IndexWriter):
	def __init__(self, index):
		self.index = index

	@property
	def schema(self):
		return self.index.schema

	def add_document(self, **fields):
		field_names = sorted(name for name in fields.keys()
			if not name.startswith('_') and fields[name] is not None)
		doc_id = bson.objectid.ObjectId()
		doc = dict(
			_id = doc_id,
		)
		for field_name in field_names:
			value = fields[field_name]
			field = self.schema[field_name]

			if field.indexed:
				# Get the index details for the field
				scorable = field.scorable
				# store the details
				for text, freq, weight, vector in field.index(value):
					if scorable:
						doc_field = doc.setdefault(field_name, {})
						doc_field['length'] = doc_field.get('length', 0) + freq
					self.index.collection.posts.insert(dict(
						doc_id = doc_id,
						field_name=field_name,
						text = text,
						weight = weight,
						vector = vector,
						), safe=True)
			if field.separate_spelling():
				raise NotImplementedError()
			if field.vector:
				raise NotImplementedError()

			stored_value = fields.get('_stored_%s' % field_name, value)

			if field.stored:
				doc_field = doc.setdefault(field_name, {})
				doc_field['value'] = stored_value

		self.index.collection.insert(doc)

	def add_reader(self, reader):
		"""
		Add the documents from the reader to the writer (?). Parent class
		doesn't document what this is supposed to do.
		Return None
		"""
		for item in reader.index.collection.find():
			self.index.insert(item)

	def delete_document(self, docnum, delete=True):
		if not delete:
			raise NotImplementedError()
		doc_id = next(self.index.collection.find().skip(docnum-1))['_id']
		self.index.collection.remove(doc_id)
		self.index.collection.posts.remove({'doc_id': doc_id})
