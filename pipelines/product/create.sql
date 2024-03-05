CREATE TABLE product (
	work_id integer REFERENCES work,
	canvas_id integer REFERENCES canvas,
	sale_price decimal(12, 2),
	regular_price decimal(12, 2), 
	PRIMARY KEY (work_id, canvas_id)
);