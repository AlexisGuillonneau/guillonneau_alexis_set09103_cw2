import sqlite3 as sql
from werkzeug import abort, generate_password_hash,check_password_hash

def getWatchlist(email):
	with sql.connect('database.db') as db:
		c = db.cursor()
		id_user = getIdUser(email)
		try:
			c.execute("SELECT id_movie FROM state WHERE id_user=? AND state=1;",[id_user])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		movies = []
		for r in res:
			tab = []
			movie = getMovieById(r[0])
			for m in movie[0]:
				tab.append(m)
			movies.append(tab)
		return movies

def getMovieById(id_movie):
	with sql.connect('database.db') as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE id=?;",[id_movie])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def getCom(id_movie):
	with sql.connect('database.db') as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM comments WHERE id_movie = ?;",[id_movie])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		res = list(res)
		tab = []
		for r in res:
			r = list(r)
			r[1] = getPseudo(r[1])
			tab.append(r)
		return tab

def getPseudo(id_user):
	with sql.connect('database.db') as db:
		c = db.cursor()
		try:
			c.execute('SELECT username FROM account WHERE id = ?;',[id_user])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		return res[0]



def addComment(body,email,id_movie,reponse):
	with sql.connect('database.db') as db:
		c = db.cursor()
		id_user = getIdUser(email)
		try:
			c.execute("SELECT COUNT(*) FROM comments;")
			nb = c.fetchone()
			if nb is None:
				nb = 0
			else:
				nb = nb[0]
			c.execute("INSERT INTO comments VALUES(?,?,?,?,?);",[nb,id_user,body,id_movie,reponse])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))


def changeState(movie,email,state):
	with sql.connect("database.db") as db:
		c = db.cursor()
		id_user = getIdUser(email)
		print(movie)
		try:
			c.execute("SELECT state FROM state where id_user = ? AND id_movie = ?;",[id_user,movie])
			res = c.fetchone()
			if res is None:
				c.execute("SELECT COUNT(*) FROM state;")
				nb = c.fetchone()
				c.execute("INSERT INTO state VALUES(?,?,?,?);",[nb[0],movie,id_user,state])
			else:
				if res[0] == state:
					state = 0
				c.execute("UPDATE state SET state = ? WHERE id_user = ? AND id_movie = ?;",[state,id_user,movie])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		return state
		
def getIdUser(email):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT id FROM account WHERE email = ?;",(email,))
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		id_user = c.fetchone()
		return id_user[0]

def get_all_data():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_abstract(name):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT abstract FROM movie WHERE Name="+name+";")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		if res is not None:
			return res[0]
		else:
			return res

def get_author(name):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT author FROM movie WHERE Name="+name+";")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		if res is not None:
			authors = res[0]
			return authors.split(";")
		else:
			return res

def get_data_carousel():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT Name, Abstract,Director,Year,Image FROM movie;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_categories():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT genres FROM movie;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		tab = []
		for r in res:
			current = list(r)
			if current[0] is not None:
				current = current[0].split(";")
				for n in current:
					if n not in tab:
						tab.append(n)
		print(tab)
		return tab

def get_from_category(cat):
	with sql.connect("database.db") as db:
		c = db.cursor()
		res = []
		try:
			c.execute("SELECT * FROM movie WHERE genres LIKE '%"+cat+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res.append(c.fetchall())
		try:
			c.execute("SELECT Image FROM movie WHERE genres LIKE  '%"+cat+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		r = c.fetchall()
		tab = []
		for t in r:
			tab.append(t[0])
		res.append(tab)
		return res

def get_movie(name):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE name=?;",(name,))
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		return res

def get_all_actors():
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT actors FROM movie;")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		tab = []
		for row in res:
			if row[0] is None:
				break
			row = list(row)
			data = row[0].split(";")
			for d in data:
				if d not in tab:
					tab.append(d)
		return tab

def get_all_data_for_year(year):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE year="+str(year)+";")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_data_for_actor(actor):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE actors LIKE '%"+actor+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_data_for_country(country):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE country LIKE '%"+country+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_data_from_producer(producer):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE producer LIKE '%"+producer+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_data_from_distribution(distribution):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE distribution LIKE '%"+distribution+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def get_all_data_from_director(director):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM movie WHERE director LIKE '%"+director+"%';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		return res

def checkEmail(email):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT * FROM account WHERE email='"+email+"';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		return res is not None

def getPwd(email):
	with sql.connect("database.db") as db:
		c = db.cursor()
		try:
			c.execute("SELECT password FROM account WHERE email='"+email+"';")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		return res

def addUser(user,email,password):
	with sql.connect("database.db") as db:
		c = db.cursor()
		pw = generate_password_hash(password)
		try:
			c.execute("SELECT COUNT(*) FROM account;")
			nb = c.fetchone()
			c.execute("INSERT INTO account VALUES("+str(nb[0]+1)+",'"+user+"','"+str(pw)+"','0','"+str(email)+"');")
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))

def getRating(id_movie):
	with sql.connect('database.db') as db:
		c = db.cursor()
		try:
			c.execute("SELECT rating FROM rating WHERE id_movie=?;",[id_movie])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchall()
		summ = 0
		nb = 0
		for r in res:
			summ += r[0]
			nb+=1
		if nb != 0:
			return summ/nb
		else:
			return 0

def getMovieId(movie):
	with sql.connect('database.db') as db:
		c = db.cursor()
		try:
			c.execute("SELECT id FROM movie WHERE name = ?;",[movie])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		if res is not None:
			return res[0]
		else:
			return ''

def getRatingMovie(id_movie,email):
	with sql.connect('database.db') as db:
		c = db.cursor()
		id_user = getIdUser(email)
		try:
			c.execute("SELECT rating FROM rating WHERE id_movie=? AND id_user=?;",[id_movie,id_user])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		if res is not None:
			return res[0]
		else:
			return 0

def changeRatingMovie(rating,id_movie,email):
	with sql.connect('database.db') as db:
		c = db.cursor()
		id_user = getIdUser(email)
		try:
			c.execute("SELECT id_rating FROM rating WHERE id_movie=? AND id_user=?;",[id_movie,id_user])
			res = c.fetchone()
			if res is not None:
				c.execute("UPDATE rating SET rating=? WHERE id_user=? and id_movie=?;",[rating,id_user,id_movie])
			else:
				c.execute("SELECT COUNT(*) FROM rating;")
				nb = c.fetchone()
				c.execute("INSERT INTO rating VALUES(?,?,?,?);",[nb[0],id_movie,id_user,rating])

		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))

def getState(id_movie,email):
	with sql.connect('database.db') as db:
		c = db.cursor()
		id_user = getIdUser(email)
		try:
			c.execute("SELECT state FROM state WHERE id_movie=? AND id_user=?;",[id_movie,id_user])
		except sql.DatabaseError as err:
			print("Error when accessing the database: '{}'".format(err))
		res = c.fetchone()
		if res is not None:
			return res[0]
		else:
			return 0
