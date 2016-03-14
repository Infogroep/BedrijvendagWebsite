from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker

class Contact(AbstractDBclass, Base):
	__tablename__ = 'contact'

	name	= Column(String(255))
	email	= Column(String(255), primary_key=True)

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)