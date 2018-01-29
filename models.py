from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

import geocoder
import urllib2
import json

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	email = db.Column(db.String(30), unique=True)
	pwdhash = db.Column(db.String(100))

	def __init__(self, firstname, lastname, email, password):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)


class Place(object):

	def wikipath(self, slug):
		return urllib2.urlparse.urljoin("http://en.wikipedia.org/wiki/", slug.replace(' ', '_'))

	def latlng(self, address):
		g = geocoder.google(address)
		return (g.lat, g.lng)

	def query(self, address):
		lat, lng = self.latlng(address)
		query_url = 'https://en.wikipedia.org/w/api.php?action=query&list=geosearch&gsradius=5000&gscoord={0}%7C{1}&gslimit=20&format=json'.format(lat, lng)
		g = urllib2.urlopen(query_url)
		res = g.read()
		g.close()
		data = json.loads(res)
		places = []
		for place in data['query']['geosearch']:
			name = place['title']
			meters = place['dist']
			lat = place['lat']
			lng = place['lon']
			wiki_url = self.wikipath(name)
			walking_time = int(meters/80)
			d = {
				'name': name,
				'url': wiki_url,
				'time': walking_time,
				'lat': lat,
				'lng': lng
			}
			places.append(d)
		return places


