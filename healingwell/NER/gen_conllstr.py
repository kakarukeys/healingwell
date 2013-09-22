import psycopg2
from nltk import sent_tokenize, word_tokenize, pos_tag
from nltk.chunk.util import tree2conllstr

from healingwell.crawler.models import GERD
from healingwell.models import db
from healingwell.NER.models import NERTrainingData

SEP = '\n\n'

def sentence2conllstr(sentence):
	return tree2conllstr(pos_tag(word_tokenize(sentence)))

def gen_conllstr(post_content):
	sentences = sent_tokenize(post_content)
	conllstr_l = map(sentence2conllstr, sentences)
	return SEP.join(conllstr_l)

records = GERD.select(GERD.id, GERD.post_content).limit(100)

db.set_autocommit(False)
try:
	for record in records:
		NERTrainingData.create(gerd=record, conllstr=gen_conllstr(record.post_content))
except psycopg2.Error as e:
    db.rollback()
    print e
else:
    db.commit()
finally:
	db.set_autocommit(True)
