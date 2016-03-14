from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker

class Financial(AbstractDBclass, Base):
	__tablename__ = 'financial'

	ID 			= Column(Integer, primary_key=True, autoincrement=True)
	data 		= Column(LargeBinary)
	kring 		= Column(String(30))
	description	= Column(String(255))
	amount 		= Column(Integer)
	paid 		= Column(Boolean)
	refunded 	= Column(Boolean)

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)