CLUSTER fact_museum_hours USING fact_museum_hours_pkey;
CREATE INDEX IF NOT EXISTS fact_artwork_dim_museum_skey_idx ON fact_artwork (dim_museum_skey);