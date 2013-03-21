from nltk import sent_tokenize, word_tokenize, pos_tag, Tree
from nltk.corpus import conll2002
from nltk.chunk.named_entity import NEChunkParser

train_data = conll2002.chunked_sents('ned.train')[:1000]
sentences = conll2002.sents("ned.train")[:100]

chunker = NEChunkParser(train_data)

for sentence in sentences:
	pos_tagged_tokens = pos_tag(sentence)
	phrase_chunks = chunker.parse(pos_tagged_tokens)
	for chunk in filter(lambda c: hasattr(c, 'node'), phrase_chunks):
		print('named entity:\n' + unicode(Tree(
			chunk.node, 
			[' '.join(c[0] for c in chunk.leaves())]
		)) + '\n')
