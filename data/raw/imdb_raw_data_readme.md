## Note on imdb raw data files

The files containing the raw IMDB data are not included in the Git repository due to their size.

For test runs of the ETL program etl_movies.py it is recommended to use the test environment (by setting environment='test'). The test environment
contains a complete sample of about 9000 movies (corresponding to the movies in the 100k Movielens dataset).

If necessary, the full raw data may be downloaded from https://www.imdb.com/interfaces/ . The files should to be unzipped and renamed as:
- imdb_title.tsv
- imdb_crew.tsv
- imdb_name.tsv
