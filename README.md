# Garage48 Open Banking Project
Description here...

## Test credentials
**User account**  
**Email:** test@test.com  
**Password:** test123
  
**Company account**  
**Email:** company@test.com  
**Password:** test123

## Screen shoots
TBD...

## Setting up
##### Add Environment Variables
```cp config.env.example config.env```
Then you need to create a new API KEY and update corresponding env variable APP_KEY.  
`FLASK_CONFIG`: can be `development`, `production`, `default`, `heroku`, `unix`, or `testing`.

##### Install the dependencies
```
$ pip install -r requirements.txt
```

##### Other dependencies for running locally
**Redis:**
_Mac (using [homebrew](http://brew.sh/)):_

```
$ brew install redis
```

_Linux:_

```
$ sudo apt-get install redis-server
```

You will also need to install **PostgresQL**

_Mac (using homebrew):_

```
brew install postgresql
```

##### Create the database, test data, setup environment 
```python manage.py setup_dev```

## Running the app
```python manage.py runserver```

For Windows users having issues with binding to a redis port locally, refer to [this issue](https://github.com/hack4impact/flask-base/issues/132).

## What's included?
* Blueprints
* User and permissions management
* Flask-SQLAlchemy for databases
* Flask-WTF for forms
* Flask-Assets for asset management and SCSS compilation
* Flask-Mail for sending emails
* gzip compression
* Redis Queue for handling asynchronous tasks
* ZXCVBN password strength checker
* CKEditor for editing pages

## Formatting code

Before you submit changes to flask-base, you may want to autoformat your code with `python manage.py format`.

**Documentation for starter-pack is available at [http://hack4impact.github.io/flask-base](http://hack4impact.github.io/flask-base).**

## License
[MIT License](LICENSE.md)
