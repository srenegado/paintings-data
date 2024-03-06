CLUSTER fact_artwork USING fact_artwork_pkey;
CREATE INDEX IF NOT EXISTS fact_artwork_dim_concept_skey_idx ON fact_artwork (dim_concept_skey);
CREATE INDEX IF NOT EXISTS fact_artwork_dim_canvas_skey_idx ON fact_artwork (dim_canvas_skey);
CREATE INDEX IF NOT EXISTS fact_artwork_dim_artist_skey_idx ON fact_artwork (dim_artist_skey);
CREATE INDEX IF NOT EXISTS fact_artwork_dim_museum_skey_idx ON fact_artwork (dim_museum_skey);
