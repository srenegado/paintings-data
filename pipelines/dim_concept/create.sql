CREATE TABLE IF NOT EXISTS dim_concept (
	dim_concept_skey serial PRIMARY KEY,
	work_id integer,
	name text,
	style text,
	subject text
);