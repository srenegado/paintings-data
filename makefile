init: 
	pip install -r requirements.txt

all: staging presentation

test: test-staging test-presentation

staging:
	python -m scripts.init_staging

presentation:
	python -m scripts.init_presentation

test-staging:
	python -m unittest \
	pipelines.artist.test \
	pipelines.canvas.test \
	pipelines.museum.test \
	pipelines.museum_hours.test \
	pipelines.product.test \
	pipelines.work.test \
	pipelines.work_subject.test

test-presentation:
	python -m unittest \
	pipelines.dim_artist.test \
	pipelines.dim_canvas.test \
	pipelines.dim_concept.test \
	pipelines.dim_museum.test \
	pipelines.fact_artwork.test \
	pipelines.fact_museum_hours.test
	