# paintings-data

This project is an ETL pipeline that ingests data on museums, artists, and their paintings into a data warehouse in Postgres. The intent here is building the data models and the ETL process from scratch, understanding these concepts by limiting the use of more sophisticated tools. It has the following features:

- Establishes an ETL process with Python using SQLAlchemy and Pandas
- Creates a data warehouse with a staging and presentation area using Postgres as the storage solution
- Validates every deployed table in the data warehouse with a comprehensive test suite

Below is a diagram that overviews the entire process.

<p align="center">
<img src="doc/overview.jpg" width="950"/>
</p>

## Installation
After cloning the repo, run the following in the command line to install the required dependencies:
```
make init
```
This project also requires [PostgreSQL](https://www.postgresql.org/download/). It is recommended to install a SQL client like [pgAdmin](https://www.pgadmin.org/download/).
## Usage


## Data
The data was sourced from [Kaggle](https://www.kaggle.com/datasets/mexwell/famous-paintings).

## License
This project is under the MIT license (see LICENSE.md)
