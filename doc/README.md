# Reference manual

This document examines the data set, its patterns, and the overall structure of the data warehouse.

## Data 
The data set has already come in a somewhat normalized form (It's in 2NF, but not 3NF), with there being several many-to-one relationships between tables. For simplicity, we preserve the normalized structure of our data set. The heavy work of our investigation is located in the `data/intial_eda.ipynb` notebook. In here we will summarise the key bits.

### Data quality
Let's point out any notable issues within each source table of our data set.

#### product (product_size)

The primary key of `product` is `(work_id, canvas_id)`:
- There are **116 decimal-valued** `canvas_id`s
- There are **212** `canvas_id`s that have the **invalid** value `'#VALUE!'`

To fix the latter issue, a default record is inserted into `canvas`:
```
(id, width, height, label) = (0, 'None', 'None', 'Missing Canvas Information')
```
Records with `canvas_id` `'#VALUE!'` are changed to having value `0`.

See below for the solution to the decimal-valued ids.

#### work
There are **10223 null** `museum_id`s. This is an issue because it would create null foreign keys up in a fact table. This is fixed with inserting a default record into `museum`:
```
(id, name, address, city, state, postal, country, phone) = 
(0, 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown')
```
All the null `museum_id`s are changed to having value `0`.
#### museum_hours
There's a record which has an **invalid value** in `close`, that value being `08 :00:PM` (the single space character). This is easily fixed by removing the space character.

### Relationships 
The cardinalities and participation can be seen in the staging ERD; most tables are in total participation with the other table in the relationship, while a few are not:
- **8709 rows** in `work` are **not associated** with any row in `work_subject` 
- **86 rows** in `work` are **not associated** with any row in `product` 
- **130 rows** in `canvas` are **not associated** with any row in `product`



### Domain knowledge
Fields can have encoded information which may help in data cleansing. Namely we see this in the `canvas` table.
#### canvas
The `id` field encodes the dimension(s) of the canvas. For example, consider the following record:
```
(id, width, height, label) = (1522, "15", "22.0", "15"" x 22""(38 cm x 56 cm)")
```
The `id` `1522` concats the `width` and `height` dimension.

Another example:
```
(id, width, height, label) = (20, "20", null, "20"" Long Edge")
```
In this case, `height` is null. The `id` `20` represents the canvas' `width`.

#### Fixing canvas_ids
Knowing how the `id` of `canvas` encodes information, we can make a fix for the 116 decimal-valued `canvas_id`s in `product`. We know now that these ids represent the dimensions of their canvas.

As examples, if a product record has `canvas_id` `3628.7`, then its canvas has a width of 36" and a height of 28.7"; whereas if a record has `canvas_id` `28.836`, then its canvas has a width of 28.836".

For each decimal-valued `canvas_id`, we convert it into an integer by multplying by 1000 and inserting the appropriate record into `canvas`. 

Continuing our two examples, a product record having `canvas_id` `3628.7` would be converted to `3628700`, and the following record would be inserted into `canvas`:
```
(id, width, height, label) = (3628700, "36", "28.7", "36"" x 28.7""")
```
A product record having `canvas_id` `28.836` would be converted to `28836`, with the following record inserted:
```
(id, width, height, label) = (28836, "28.836", null, "28.836"" Long Edge")
```
## Entity-relationship diagrams
### Staging Area

<p align="center">
<img src="staging_area.jpg" width="650"/>
</p>

| Target table | Source |
| ------------ | ------ |
| artist       | artist.csv |
| canvas       | canvas_size.csv |
| museum       | museum.csv |
| museum_hours | museum_hours.csv |
| work         | work.csv |
| work_subject | subject.csv |
| product      | product_size.csv |
| work         | work.csv |

### Presentation Area

<p align="center">
<img src="presentation_area.jpg" width="650"/>
</p>

| Target table | Source table |
| ------------ | ------------ |
| dim_artist   | artist |
| dim_museum   | museum |
| dim_concept  | work, work_subject |
| dim_canvas   | canvas |
| fact_artwork | product, work, dim_canvas, dim_artist, dim_museum |
| fact_museum_hours | museum_hours, dim_museum |