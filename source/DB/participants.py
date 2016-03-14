from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker

class Participants(AbstractDBclass, Base):
	__tablename__ 	= 'Participants'

	companyID 		= Column(Integer, ForeignKey('companies.ID'), primary_key=True)
	year 			= Column(Integer, primary_key=True)
	formulaID 		= Column(Integer, ForeignKey('formula.ID'))
	state 			= Column(String(255))
	tables 			= Column(Integer)
	promotion_wand 	= Column(Integer)
	remarks 		= Column(String(255))
	high_stand 		= Column(Integer)
	number_of_pages = Column(Integer)
	payment_status 	= Column(Integer)
	invoice 		= Column(Integer)

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)