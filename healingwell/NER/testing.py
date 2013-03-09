from operator import itemgetter
import codecs

import psycopg2
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk, Tree

from healingwell.settings import POSTGRES

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

conn = psycopg2.connect(**POSTGRES)
cur = conn.cursor()
cur.execute("select * from gerd limit 100")

with codecs.open("output.txt", 'w', encoding='utf-8') as f:
	texts = map(itemgetter(6), cur)
	sentences = (s for sublist in map(sent_tokenize, texts) for s in sublist)
	for sentence in sentences:
		f.write('Sentence:\n' + sentence + '\n')
		tokens = word_tokenize(sentence)
		pos_tagged_tokens = pos_tag(tokens)
		phrase_chunks = ne_chunk(pos_tagged_tokens)
		for chunk in filter(lambda c: hasattr(c, 'node'), phrase_chunks):
			f.write('named entity:\n' + unicode(Tree(
				chunk.node, 
				[' '.join(c[0] for c in chunk.leaves())]
			)) + '\n')
		f.write('\n')

cur.close()
conn.close()
