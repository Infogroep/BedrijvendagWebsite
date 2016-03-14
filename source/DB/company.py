from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker

## Autoincrement doesn't work so, .... yeah
## Should be omitted in production

class Company(AbstractDBclass, Base):
	__tablename__ = 'companies'

	ID 					= Column(Integer, primary_key=True, autoincrement=True)
	name 				= Column(String(255), unique=True)
	address 			= Column(String(255))
	area_code 			= Column(String(255))
	place 				= Column(String(255))
	country 			= Column(String(255))
	tav 				= Column(String(255))
	email 				= Column(String(255))
	telephone_number 	= Column(String(255))
	fax_number 			= Column(String(255))
	cellphone_number 	= Column(String(255))
	website 			= Column(String(255))
	tax_exempt_number 	= Column(String(255))
	filename 			= Column(String(255))
	password 			= Column(String(255))

	def __init__(self, **kwargs):
		super(Company, self).__init__(**kwargs)

	