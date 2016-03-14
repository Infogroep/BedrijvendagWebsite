from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import config
from sqlalchemy.orm import sessionmaker

'''This is just a database config file. Move along'''

__author__ 	= 'Kwinten Pardon'
__contact__ = 'kwpardon@vub.ac.be'

Base = declarative_base()

#engine = create_engine('mysql://{0}:{1}@{2}:{3}/{4}'.format(config.database_user, config.database_password, config.database_host, config.database_port, config.database_name))
engine = create_engine('sqlite:///Students2Industry.db')


def new_id():
	ID = 0
	print('ID', ID)
	try:
		with open('ID', 'r') as f:
			r = f.read()
			if len(r) > 0:
				ID = int(r)
	except:
		pass
	with open('ID', 'w') as f:
		f.write(str(ID + 1))
	return ID

class AbstractDBclass():
	def __init__(self, **kwargs):
		print('init')
		for K in kwargs.keys():
			setattr(self, K, kwargs[K])
		self.ID = new_id()
		self.commit()

	def from_db(self, **kwargs):
		session = (sessionmaker(bind=engine))()
		new = session.query(self.__class__).filter_by(**kwargs).all()[0]
		self = new
		session.close()
		return self


	def commit(self):
		session = (sessionmaker(bind=engine))()
		session.expire_on_commit = False
		session.add(self)
		
		session.commit()
		session.close()

	def delete(self):
		session = (sessionmaker(bind=engine))()
		session.expire_on_commit = False
		session.delete(self)
		
		session.commit()
		session.close()