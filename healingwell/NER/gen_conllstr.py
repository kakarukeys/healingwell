import psycopg2
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk.chunk.util import tree2conllstr

from healingwell.settings import POSTGRES

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

SEP = '\n\n'

def gen_conllstr(post_content):
	sentences = sent_tokenize(post_content)
	conllstr_l = map(tree2conllstr, map(ne_chunk, map(pos_tag, map(word_tokenize, sentences))))
	return SEP.join(conllstr_l)

conn = psycopg2.connect(**POSTGRES)
cur_read = conn.cursor()
cur_write = conn.cursor()
cur_read.execute("select id, post_content from gerd limit 100")

try:
	for record in cur_read:
		cur_write.execute("insert into ner_training_data (gerd_id, conllstr) values (%s, %s)", (record[0], gen_conllstr(record[1])))
except psycopg2.Error as e:
    conn.rollback()
    print e
else:
    conn.commit()

cur_read.close()
cur_write.close()
conn.close()
