CREATE TABLE IF NOT EXISTS dim_canvas (
	dim_canvas_skey serial PRIMARY KEY,
	canvas_id integer,
	width text,
	height text,
	label text 
);