SELECT
    dim_concept.dim_concept_skey as dim_concept_skey,
    CASE WHEN dim_canvas.dim_canvas_skey IS NULL THEN 1
         ELSE dim_canvas.dim_canvas_skey 
    END as dim_canvas_skey,
    dim_artist.dim_artist_skey as dim_artist_skey,
    dim_museum.dim_museum_skey as dim_museum_skey,
    product.sale_price as sale_price,
    product.regular_price as regular_price
FROM dim_concept
LEFT JOIN product ON product.work_id = dim_concept.work_id -- necessary LEFT JOIN
LEFT JOIN dim_canvas ON product.canvas_id = dim_canvas.canvas_id -- necessary LEFT JOIN
LEFT JOIN work on dim_concept.work_id = work.id
LEFT JOIN dim_artist on work.artist_id = dim_artist.artist_id
LEFT JOIN dim_museum on work.museum_id = dim_museum.museum_id
ORDER BY 1, 2