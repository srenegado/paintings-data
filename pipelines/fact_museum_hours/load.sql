SELECT
    dim_museum.dim_museum_skey as dim_museum_skey,
    museum_hours.day as day,
    museum_hours.open as opening_hours,
    museum_hours.close as closing_hours
FROM museum_hours
JOIN dim_museum on museum_hours.museum_id = dim_museum.museum_id
