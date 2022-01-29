### Movies dataset

|column | source dataset | column or calculation|
|---|---|---|
|movieId | movielens.movies | (copy)|
|imdbId | movielens.movies | (copy)|
|tmdbId | movielens.movies | (copy)|
|title | movielens.movies | title (first part of the string)|
|year | movielens.movies | title (last part of the string)|
|num_ratings | movielens.ratings | size(rating)|
|avg_rating | movielens.ratings | mean(rating)|
|isAdult | imdb.title | (copy)|
|runtimeMinutes | imdb.title | (copy)|
|directors | imdb.title | (copy)|
|directorId | imdb.title | directors (select the first of the list)|
|genres (various columns) | movielens.movies | genres (converted to dummy variables)|
		
### Directors dataset

| column     | source dataset | column or calculation |
|------------|----------------|-----------------------|
| directorId | imdb.names     | nconst                |
| name       | imdb.names     | primaryName           |
| birthYear  | imdb.names     | (copy)                |
| deathYear  | imdb.names     | (copy)                |    
    
### Ratings dataset    

| column      | source dataset    | column or calculation         |
|-------------|-------------------|-------------------------------|
| userId      | movielens.ratings | (copy)                        |
| movieId     | movielens.ratings | (copy)                        |
| rating      | movielens.ratings | (copy)                        |
| rating_date | movielens.ratings | timestamp converted into date |

### Tags dataset

| column   | source dataset | column or calculation         |
|----------|----------------|-------------------------------|
| userId   | movielens.tags | (copy)                        |
| movieId  | movielens.tags | (copy)                        |
| tag      | movielens.tags | (copy)                        |
| tag_date | movielens.tags | timestamp converted into date |

### Movie_actors dataset

| column        | source               | source field         |
|---------------|----------------------|----------------------|
| movieId       | movies dataset       | movieId              |
| tmdbId        | tmdb API get credits | id                   |
| actor_tmdb_id | tmdb API get credits | cast[i].id           |
| actor_name    | tmdb API get credits | cast[i].name         |
| role          | tmdb API get credits | cast[i].character    |
| profile_path  | tmdb API get credits | cast[i].profile_path |

### Movie_country_certification dataset

| column        | source                 | source field         |
|---------------|------------------------|----------------------|
| movieId       | movies dataset         | movieId              |
| country       | tmdb API release_dates | country_data.iso_3166_1 |
| certification | tmdb API release_dates | country_data.release_dates.certification |

### Movie_region_platform dataset

| column        | source             | source field           |
|---------------|--------------------|------------------------|
| movieId       | movies dataset     | movieId                |
| region        | tmdb API providers | (key name)             |
| platforms     | tmdb API providers | flatrate.provider_name |
