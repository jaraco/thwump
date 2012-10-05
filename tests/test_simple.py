from __future__ import print_function, unicode_literals

from whoosh import fields
from whoosh.qparser import QueryParser
from thwump.index import Index

def test_quick_example():
	"""
	Exercise the behavior using the quick example given in the Whoosh
	documentation.
	"""
	schema = fields.Schema(
		title=fields.TEXT(stored=True),
		path=fields.ID(stored=True),
		context=fields.TEXT,
	)
	ix = Index()
	writer = ix.writer()
	writer.add_document(title="First Document", path="/a",
		content="This is the first document we've added!",
	)
	writer.add_document(title="Second Document", path="/b",
		content="The second one is even more interesting!",
	)
	writer.commit()
	with ix.searcher() as searcher:
		query = QueryParser('content', ix.schema).parse('first')
		results = searcher.search(query)
		print(results[0])
