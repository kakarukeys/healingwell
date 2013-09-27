import time
import ner


# java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier ner-model.ser.gz -port 8000 -outputFormat inlineXML

statement = u"As diplomats at the United Nations push for a peace conference to end Syria\'s civil war, a collection of some of the country\'s most powerful rebel groups publicly abandoned the opposition\'s political leaders, casting their lot with an affiliate of Al Qaeda."

tagger = ner.SocketNER(port=8000)

print(tagger.tag_text(statement))

now = time.time()
for i in range(1000):
	tagger.get_entities(statement)
print time.time() - now
