from werkzeug import abort, generate_password_hash,check_password_hash
from flask import Blueprint
from flask import render_template, url_for, send_from_directory,session,request,redirect,flash,jsonify
import my_app.movie.model as bd
import my_app as app
import json
from random import shuffle
import os
from functools import wraps




import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


import os

def send(gmail_user, gmail_pwd, to, subject, text, attach=None):
    msg = MIMEMultipart("alternative")
    msg.set_charset("utf-8")
    
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(text, "plain", "utf-8"))
    
    print (msg)

    try:
        mailServer = smtplib.SMTP("smtp.gmail.com", 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(gmail_user, gmail_pwd)
        mailServer.sendmail(gmail_user, to, msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()
        return True
    except:
        # app.loggger.error("Couldn't send confirmation email: " + str(text)) - Causes crash
        # TODO: fix error logging here so that it doesn't cause a crash.
        pass

movie_blueprint = Blueprint('movie',__name__)
categories = sorted(bd.get_all_categories())
@movie_blueprint.route('/')
def index():
	
	res = bd.get_data_carousel()
	shuffle(res)
	return render_template('index.html',movies=res[:10], categories=categories),200

@movie_blueprint.route('/category/<string:category>')
def category(category):
	res = bd.get_from_category(category)
	if res is None:
		abort(404)
	return render_template('category.html',movies=res[0],categories=categories,category=category),200

@movie_blueprint.route('/movies/<string:movie>')
def movie(movie):
	rating = bd.getRating(bd.getMovieId(movie))
	res = bd.get_movie(movie)
	if res is None:
		abort(404)
	return render_template('movie.html',movie=res,categories=categories,rating=rating),200

@movie_blueprint.route('/movies')
def display_all_movies():
	res = bd.get_all_data()
	actors = bd.get_all_actors()
	return render_template('all_movies.html',movies=res,categories=categories,actors=sorted(actors)),200

@movie_blueprint.route('/year/<int:year>')
def year(year):
	res = bd.get_all_data_for_year(year)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies in "+str(year),movies=res,categories=categories),200

@movie_blueprint.route('/actor/<string:actor>')
def actor(actor):
	res = bd.get_all_data_for_actor(actor)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies where "+actor+" is starring",movies=res,categories=categories),200

@movie_blueprint.route('/country/<string:country>')
def country(country):
	res = bd.get_all_data_for_country(country)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies from "+country,movies=res,categories=categories),200

@movie_blueprint.route('/producer/<string:producer>')
def producer(producer):
	res = bd.get_all_data_from_producer(producer)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies produced by "+producer,movies=res,categories=categories),200

@movie_blueprint.route('/distribution/<string:distribution>')
def distribution(distribution):
	res = bd.get_all_data_from_distribution(distribution)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies distribued by "+distribution,movies=res,categories=categories),200

@movie_blueprint.route('/director/<string:director>')
def director(director):
	res = bd.get_all_data_from_director(director)
	if res is None:
		abort(404)
	return render_template('display_data.html',name="Movies leaded by "+director,movies=res,categories=categories),200

@movie_blueprint.app_errorhandler(404)
def error404(error):
	return render_template('error.html',categories=categories,error=error),404

@movie_blueprint.app_errorhandler(403)
def error403(error):
	return render_template('error.html',categories=categories,error=error),403

@movie_blueprint.route('/about')
def about():
	return render_template('about.html',categories=categories),200

@movie_blueprint.route('/report', methods=['POST'])
def report():
	return send_from_directory(directory='static/pdf',filename='report.pdf',as_attachment=True,attachment_filename='report.pdf')

def check_auth(email,password):
	if(bd.checkEmail(email)):
		pwd = bd.getPwd(email)

		return check_password_hash(pwd[0],password)

def requires_login(f):
	@wraps(f)
	def decorated(*args, **kwargs):

		status = session.get('logged',False)

		if not status:

			return redirect(url_for('movie.root'))
		return f(*args, **kwargs)
	return decorated

@movie_blueprint.route('/logout')
def logout():
	session['logged'] = False
	return render_template('login.html',categories=categories),200

@movie_blueprint.route('/secret')
@requires_login
def secret():
	return "secret page"

@movie_blueprint.route('/login_page')
def login():
	return render_template('login.html',categories=categories),200

@movie_blueprint.route('/login', methods=['POST'])
def root():
	email = request.form['email']
	pw = request.form['password']

	if check_auth(email,pw):
		session['logged'] = email
		return redirect(url_for('movie.index'))
	flash("Wrong email adress or password. Please try again.")
	return render_template('login.html',categories=categories),200

@movie_blueprint.route('/sign')
def sign():
	return render_template('sign.html',categories=categories),200

@movie_blueprint.route('/signup',methods=['POST'])
def signup():
	user = request.form['username']
	email = request.form['email']
	password = request.form['password']
	if not bd.checkEmail(email):
		send("donotreply.searchmovie@gmail.com", "searchmovie",email,"Welcome", "Welcome to searchMovie !")
		bd.addUser(user,email,password)
		return render_template('login.html',categories=categories),200
	else:
		flash("This user already exist.")
		return render_template('sign.html',categories=categories),200

@movie_blueprint.route('/like',methods=['GET'])
def like():
	id_movie = request.args.get('q')
	email = session['logged']
	response = bd.changeState(id_movie,email,2)
	return jsonify(response=[response]),200

@movie_blueprint.route('/list',methods=['GET'])
def list():
	id_movie = request.args.get('q')
	email = session['logged']
	response = bd.changeState(id_movie,email,1)
	return jsonify(response=[response]),200

@movie_blueprint.route('/comment',methods=['GET'])
@requires_login
def comment():

	body = request.args.get('body')
	id_movie = request.args.get('id_movie')
	parent = request.args.get('parent')
	email = session['logged']
	bd.addComment(body,email,id_movie,parent)
	return jsonify(response=['ok'])

@movie_blueprint.route('/getCom',methods=['GET'])
def getCom():
	id_movie = request.args.get('id')
	res = bd.getCom(id_movie)
	return jsonify(response=res)

@movie_blueprint.route('/rating',methods=['GET'])
def rating():
	id_movie = request.args.get('id_movie');
	email = session['logged']
	rating = bd.getRatingMovie(id_movie,email);
	return jsonify(response=[rating])

@movie_blueprint.route('/changeRating',methods=['GET'])
def changeRating():
	rating = request.args.get('rating')
	id_movie = request.args.get('id_movie')
	email = session['logged']
	bd.changeRatingMovie(rating,id_movie,email)
	return jsonify(response=['ok']),200

@movie_blueprint.route('/getSate',methods=['GET'])
def getState():
	id_movie = request.args.get('id_movie')
	email = session['logged']
	state = bd.getState(id_movie,email)
	return jsonify(response=[state])

@movie_blueprint.route('/account')
@requires_login
def account():
	username = bd.getPseudo(bd.getIdUser(session['logged']))
	movies = bd.getWatchlist(session['logged'])
	print(movies)
	return render_template('account.html',categories=categories,username=username,movies=movies)
