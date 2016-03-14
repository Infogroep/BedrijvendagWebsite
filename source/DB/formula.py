from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker

class Formula(AbstractDBclass, Base):
	__tablename__ = 'formula'

	ID 				= Column(Integer, primary_key=True, autoincrement=True)
	name 			= Column(String(255))
	price 			= Column(Integer)
	number_of_pages = Column(Integer)
	description 	= Column(String(255))

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)