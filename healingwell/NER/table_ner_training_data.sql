CREATE TABLE ner_training_data
(
	gerd_id int references gerd(id) NOT NULL primary key,
	conllstr text NOT NULL
)
