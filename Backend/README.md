# Get Me a Movie: API

This directory contains the source code associated to the Get Me a Movie API.
It has been built using **FastAPI** as the web framework and **Poetry** as the
dependency manager. It also contains a Docker image that can be run, which
makes it easier to replicate the production environment.

## Dependencies

In order to run the API on local, you need the following:

- Python3.8
- Poetry

Additionally, you need `docker` if you want to run it for testing purposes or to
simulate the production environment.

## Running the API

### On your machine (local development)

Install Poetry (you can follow [this guide](https://python-poetry.org/docs/#installation))
and Python 3.8. Since you might have multiple Python versions in your device,
create a Python 3.8 virtual environment in this directory as follows:

```
$ python3.8 -m venv .venv
```

Once you've set up the virtual environment, install the dependencies using:

```
$ poetry install
```

Finally, in order to run the API, run the following command:

```
$ poetry run uvicorn app.main:app --reload
```

Additionally, if you have created new tests or you have changed the current
functionality, you can run the tests by using:

```
$ poetry run pytest
```

### Using docker (testing/production environment)

If you have `docker` installed in your machine, first create the image by running
the following command in this directory:

```
$ docker build -t get-me-a-movie-api .
```

Once the image is created, you can easily create a container by running the
following:

```
$ docker run -p 8000:8000 -e PORT=8000 get-me-a-movie-api
```

This will run the API using `gunicorn` with 4 async workers, which are based
on `uvicorn` workers. This configuration has been specifically created for
production environments.

Note that since you are passing the `PORT` on which the API will run as an
environment variable, you have to run the following command in order to stop
the container:

```
$ docker kill CONTAINER_ID
```

