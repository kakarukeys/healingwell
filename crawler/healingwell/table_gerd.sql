CREATE TABLE gerd
(
	id serial NOT NULL primary key,

	page_url character varying(100) NULL,

	post_url  character varying(100) NULL,
	post_author  character varying(30) NULL,
	post_author_url character varying(100) NULL,
	post_date timestamp NULL,
	post_content  text NULL,

	thread_url  character varying(100) NULL,
	thread_title  character varying(150) NULL,

	section_url character varying(100) NULL,
	section_title character varying(50) NULL
)