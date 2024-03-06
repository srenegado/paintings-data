SELECT
    dim_concept.dim_concept_skey as dim_concept_skey,
    dim_canvas.dim_canvas_skey as dim_canvas_skey,
    dim_artist.dim_artist_skey as dim_artist_skey,
    dim_museum.dim_museum_skey as dim_museum_skey,
    product.sale_price as sale_price,
    product.regular_price as regular_price
FROM product
JOIN dim_canvas on product.canvas_id = dim_canvas.canvas_id
JOIN dim_concept on product.work_id = dim_concept.work_id
JOIN work on product.work_id = work.id
JOIN dim_artist on work.artist_id = dim_artist.artist_id
JOIN dim_museum on work.museum_id = dim_museum.museum_id