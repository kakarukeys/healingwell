from nltk.chunk.util import conllstr2tree
from nltk.chunk.named_entity import NEChunkParser
from healingwell.NER.models import NERTrainingData


# java -cp stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -prop austen.prop

SEP = '\n\n'

results = NERTrainingData.select(NERTrainingData.conllstr).order_by(NERTrainingData.id.asc()).limit(10)
training_data = map(conllstr2tree, (d.conllstr for d in results))
chunker = NEChunkParser(training_data)
ner = chunker.parse

results = NERTrainingData.select(NERTrainingData.conllstr).order_by(NERTrainingData.id.asc()).limit(10)
evaluation_data = map(conllstr2tree, (d.conllstr for d in results))

for tree in evaluation_data:
	phrase_chunks = ner(tree)
	for chunk in filter(lambda c: hasattr(c, 'node'), phrase_chunks):
		print('named entity:\n' + unicode(Tree(
			chunk.node,
			[' '.join(c[0] for c in chunk.leaves())]
		)) + '\n')

#  -> training -> save chunker using pickle