CREATE TABLE contact(
		name varchar(255),
		email varchar(255)
		);

CREATE TABLE companies(
		ID int,
		name varchar(255),
		address varchar(255),
		area_code varchar(255),
		place varchar(255),
		country varchar(255),
		tav varchar(255),
		email varchar(255),
		telephone_number varchar(255),
		fax_number varchar(255),
		cellphone_number varchar(255),
		website varchar(255),
		tax_exempt_number varchar(255),
		PRIMARY KEY(ID)
		);
		
CREATE TABLE formula(
		ID int,
		name varchar(255),
		price int,
		description varchar(255),
		PRIMARY KEY(ID)
		);
		
CREATE TABLE participants(
		companyID int,
		year int,
		formulaID int,
		state varchar(255),
		tables int,
		promotion_wand int,
		remarks varchar(255),
		high_stand int,
		number_of_pages int,
		FOREIGN KEY(companyID) REFERENCES companies(ID),
		FOREIGN KEY(formulaID) REFERENCES formula(ID)
		);
