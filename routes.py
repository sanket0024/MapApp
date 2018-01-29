from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mapapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))
	form = SignupForm()
	if request.method == 'GET':
		return render_template("signup.html", form = form)
	elif request.method == 'POST':
		if form.validate() == False:
			return render_template("signup.html", form = form)
		else:
			newUser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newUser)
			db.session.commit()
			session['email'] = newUser.email
			return redirect(url_for('home'))

@app.route("/home", methods=["GET", "POST"])
def home():
	if 'email' not in session:
		return redirect(url_for('login'))

	form=AddressForm()
	places = []
	coord = (0,0)
	if request.method == "POST":
		if form.validate() == False:
			return render_template('home.html', form=form)
		else:
			#get the address
			address = form.address.data

			#mark the places
			p = Place()
			coord = p.latlng(address)
			places = p.query(address)

			#return the result
			return render_template('home.html', form=form, coord=coord, places=places)
	elif request.method == "GET":
		return render_template("home.html", form=form, coord=coord, places=places)

@app.route("/login", methods=["GET", "POST"])
def login():
	if 'email' in session:
		return redirect(url_for('home'))
	form = LoginForm()
	if request.method == "POST":
		if form.validate() == False:
			return render_template("login.html", form = form)
		else:
			email = form.email.data
			password = form.password.data
			user = User.query.filter_by(email=email).first()
			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))
	elif request.method == "GET":
		return render_template('login.html', form = form)

@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)