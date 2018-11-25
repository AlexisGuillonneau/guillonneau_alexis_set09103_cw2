import unittest
from my_app import app

class TestingTest(unittest.TestCase):
	def test_index(self):
		self.app = app.test_client()
		out = self.app.get('/')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type
	
	def test_category(self):
		self.app = app.test_client()
		out = self.app.get('/category/<string:category>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_movie(self):
		self.app = app.test_client()
		out = self.app.get('/movie/<string:movie>')
		print(out.status)
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_movies(self):
		self.app = app.test_client()
		out = self.app.get('/movies')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_year(self):
		self.app = app.test_client()
		out = self.app.get('/year/<int:year>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_actor(self):
		self.app = app.test_client()
		out = self.app.get('/actor/<string:actor>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_country(self):
		self.app = app.test_client()
		out = self.app.get('/country/<string:country>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_producer(self):
		self.app = app.test_client()
		out = self.app.get('/producer/<string:producer>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_distribution(self):
		self.app = app.test_client()
		out = self.app.get('/distribution/<string:distribution>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type

	def test_director(self):
		self.app = app.test_client()
		out = self.app.get('/director/<string:director>')
		assert '200 OK' in out.status
		assert 'charset=utf-8' in out.content_type
		assert 'text/html' in out.content_type	

if __name__ == "__main__":
	unittest.main()