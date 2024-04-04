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

> **Note:** For more on architecture, check out the `doc` folder.

## Installation
This project requires [Python](https://www.python.org/): I used version `3.11`. Clone this repo and now you've got all the code!

You can install the required Python dependencies via:
```
make init
```
As for the database, you can either install everything locally or install [Docker](https://www.docker.com/) to spin up containers.

- Local: Visit the [PostgreSQL](https://www.postgresql.org/download/) page and navigate the downloads based on your OS. Likewise install [pgAdmin 4](https://www.pgadmin.org/download/).
- Docker: Visit [their page](https://www.docker.com/get-started/).

Most importantly, remember to download the [data](https://www.kaggle.com/datasets/mexwell/famous-paintings)! Extract the `csv`s to the `data` folder.

## Usage
How the database is setup depends on if you installed PostgreSQL and pgAdmin locally or are using Docker, though the difference is pretty small.

### Setting up the DB locally
We first need to know the credentials of the admin user. The default user is usually `postgres` and the password is normally configured when installing PostgreSQL, but you can always [change it](https://stackoverflow.com/questions/12720967/how-can-i-change-a-postgresql-user-password). 

Open the `pipelines/config.json` file and then edit the `user` and `password` fields in accordingly. Also the `port` field should be `5432`.

Open pgAdmin and make a new server: the host name should be `localhost`, the port is `5432`, and username and password is the admin login.

To create a database, first connect to the default `postgres` database with the admin user. Then run the following query:
```
CREATE DATABASE paintings;
```
A `paintings` database should appear under the Databases drop down menu.

### Setting up the DB via Docker
Spin up the Docker containers via
```
docker compose up
```
Open up the `compose.yml` file. The `POSTGRES_USER` and `POSTGRES_PASSWORD` variables is our database's admin user login, so fill out the `user` and `password` fields in the `pipelines/config.json` file accordingly. 

Also the `port` field should now be `5433` (not `5432`!).

Going to `localhost:5050` in your browser directs you to a login page for pgAdmin: use `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD` to login.

Make a new server like how we did in the local setup, except now the host name should be `db` instead of `localhost`.

A `paintings` database should already be listed under Databases.

The containers can bu shut down via
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
