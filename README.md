# Main API

Built with [Python Flask](http://flask.pocoo.org/).

[![wercker status](https://app.wercker.com/status/36b13e641a708e7a80e969d0fcd01338/s/master "wercker status")](https://app.wercker.com/project/bykey/36b13e641a708e7a80e969d0fcd01338) [![Docker Pulls](https://img.shields.io/docker/pulls/acmplanner/main-api.svg?maxAge=2592000)](https://hub.docker.com/r/acmplanner/main-api/)


> Based on [mrpatiwi/flask-starter](https://github.com/mrpatiwi/flask-starter)


## Running

Clone this repository:

```sh
git clone https://github.com/ACM-Planner/main-api.git
```

Set environment variables:

```sh
export RDF_URI=http://localhost:3030
export RDF_STORE=store
export RDF_USER=admin
export RDF_PASSWORD=pw
```

> Check [ACM-Planner/RDF-store](https://github.com/ACM-Planner/RDF-store) to run a local instance of a HTTP RDF Store.

### Development

Make sure you have [Python 3.4.x](https://www.python.org/) installed.

Install the dependencies with:

```sh
pip install -r requirements.txt
```

Start this application with:

```sh
python main.py
```

Now it's available at [`http://localhost:5000`](http://localhost:5000).

#### Testing

```sh
python test/app_test.py
```
