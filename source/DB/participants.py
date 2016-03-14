from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker

class Participants(AbstractDBclass, base):

	companyID 		= Column(Integer)
	year 			= Column(Integer)
	formulaID 		= Column(Integer)
	state 			= Column(varchar(255))
	tables 			= Column(Integer)
	promotion_wand 	= Column(Integer)
	remarks 		= Column(varchar(255))
	high_stand 		= Column(Integer)
	number_of_pages = Column(Integer)
	payment_status 	= Column(Integer)
	invoice 		= Column(Integer)

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)