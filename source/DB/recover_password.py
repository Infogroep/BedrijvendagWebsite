from DB.database import Base, engine, AbstractDBclass
from sqlalchemy import Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import sessionmaker

class RecoverPassword(AbstractDBclass, Base):
	__tablename__ = 'recover_password'

	recoverID 		= Column(Integer, autoincrement=True, primary_key=True)
	companyID 		= Column(Integer, ForeignKey('companies.ID'))
	password_url	= Column(LargeBinary)