# Main API

Built with [Python Flask](http://flask.pocoo.org/).

> Based on [mrpatiwi/flask-starter](https://github.com/mrpatiwi/flask-starter)

[![wercker status](https://app.wercker.com/status/d1ef9c42121ef910ba27a90ac6fc78b8/s "wercker status")](https://app.wercker.com/project/bykey/d1ef9c42121ef910ba27a90ac6fc78b8)

## Running

Clone this repository:

```sh
git clone https://github.com/ACM-Planner/main-api.git
```

Set environment variables

```sh
export RDF_URI=http://localhost:3030
export RDF_STORE=store
export RDF_USER=admin
export RDF_PASSWORD=pw
```

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
