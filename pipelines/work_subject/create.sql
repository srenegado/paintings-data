CREATE TABLE work_subject (
	work_id integer REFERENCES work,
	subject text,
	PRIMARY KEY (work_id, subject)
);