CREATE TABLE IF NOT EXISTS fact_artwork (
	dim_concept_skey integer REFERENCES dim_concept,
	dim_canvas_skey integer REFERENCES dim_canvas,
	dim_artist_skey integer REFERENCES dim_artist,
	dim_museum_skey integer REFERENCES dim_museum,
	sale_price decimal(12, 2),
	regular_price decimal(12, 2), 
	PRIMARY KEY (dim_concept_skey, dim_canvas_skey)
);