# paintings-data

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Claude_Monet_-_Woman_with_a_Parasol_-_Madame_Monet_and_Her_Son_-_Google_Art_Project.jpg/270px-Claude_Monet_-_Woman_with_a_Parasol_-_Madame_Monet_and_Her_Son_-_Google_Art_Project.jpg"
  width="250"/>
</p>

<p align="center">
  <a href="https://en.wikipedia.org/wiki/Woman_with_a_Parasol_%E2%80%93_Madame_Monet_and_Her_Son">Woman with a Parasol – Madame Monet and Her Son</a>, <i>1875 by Claude Monet, <br>National Gallery of Art, Washington DC</i>
</p>

This project is an ETL pipeline that ingests data on museums, artists, and their paintings into a data warehouse in Postgres. The intent here is building the data models and the ETL process from scratch, understanding these concepts by limiting the use of more sophisticated tools. It has the following features:

- Establishes an ETL process with Python using SQLAlchemy and Pandas
- Creates a data warehouse with a staging and presentation area using Postgres as the storage solution
- Validates every deployed table in the data warehouse with a comprehensive test suite

Below is a diagram that overviews the entire process.

<p align="center">
<img src="doc/overview.jpg" width="950"/>
</p>

> **Note:** For more on data modeling and data quality, check out the [docs](https://github.com/srenegado/paintings-data/tree/main/doc).

## Installation
This project requires [Python](https://www.python.org/): I used version `3.11`.

Clone this repo. Then you can install the required Python dependencies via:
```
make init
```
To install the database either:
- Install [PostgreSQL](https://www.postgresql.org/download/) and [pgAdmin 4](https://www.pgadmin.org/download/) locally; or
- Install [Docker](https://www.docker.com/get-started/).

Download the [data](https://www.kaggle.com/datasets/mexwell/famous-paintings) and extract the `csv`s to the `data` folder.

## Usage
How the database is setup depends on if you installed PostgreSQL and pgAdmin locally or are using Docker.

### Setting up the DB locally
Usually the default user is `postgres` and the password is normally configured when installing PostgreSQL, but you can always [change it](https://stackoverflow.com/questions/12720967/how-can-i-change-a-postgresql-user-password). 

Inside the `pipelines/config.json` file, set the following values:
```
"user": "your_default_postgres_username",
"password": "your_default_postgres_password",
"host": "localhost",
"port": 5432
```

Open pgAdmin and make a new server, filling in the following areas:
```
Host name/address: localhost
Port: 5432
Username: your_default_postgres_username
Password: your_default_postgres_password
```

To create a database, first connect to the default `postgres` database with the default user. Then run the following query:
```
CREATE DATABASE paintings;
```
A `paintings` database should appear under the Databases drop down menu.

### Setting up the DB via Docker
Spin up the Docker containers via
```
docker compose up
```
Open up the `compose.yml` file for reference.

Inside the `pipelines/config.json` file, set the following values:
```
"user": POSTGRES_USER,         # from compose.yml
"password": POSTGRES_PASSWORD, # from compose.yml
"host": "localhost",
"port": 5433
```

Go to `localhost:5050` in your browser directs and login using `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD`.

Make a new server with the following values:
```
Host name/address: db
Port: 5432
Username: POSTGRES_USER
Password: POSTGRES_PASSWORD
```

A `paintings` database should already be listed under Databases.

To shut down the containers, use:
```
docker compose down
```

### Running the pipeline
You can deploy the tables using
```
make all
```
You should see these tables now in the ``paintings`` database: check it out through pgAdmin.

Then you can validate the tables with
```
make test
```
and see all the tests results in the console.

## Data
The data was sourced from [Kaggle](https://www.kaggle.com/datasets/mexwell/famous-paintings).

## License
This project is under the MIT license (see [LICENSE](LICENSE))
