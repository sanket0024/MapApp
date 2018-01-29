# Map App

This application will let you login into the system and explore the locations over the map.

## Version
1.0 <br />

## Author
* Sanket Mathur

## Directory Structure
* All the logic and the backend python files can be found under the MapApp folder
* All the html templates are in MapApp/templates
* All the static files (images and styles) are under MapApp/static folder

## To setup:
$ pip install virtualenv <br />
$ virtualenv venv <br />
$ source venv/bin/activate <br />
$ pip install -r requirements.txt

## Database:
* Postgres
* One table Users.
* Create Database MapApp
* Create Table Users(uid serial primary key, firstname varchar(20) not null, lastname varchar(20) not null, email varchar(30) not null unique, pwdhash varchar(20))

## To run flask app
$ python routes.py

## To get out of the virtualenv:
$ deactivate

## Acknowledgement
This project uses code from the following third party librarys: <br />

Flask<br />
Bootstrap <br />
WTForms <br />
Leaflet
