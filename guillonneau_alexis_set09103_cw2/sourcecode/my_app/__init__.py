from flask import Flask
from my_app.movie.controler import movie_blueprint
app = Flask(__name__)
app.register_blueprint(movie_blueprint)