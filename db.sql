-- SCHEMA: public

-- DROP SCHEMA IF EXISTS public ;

CREATE SCHEMA IF NOT EXISTS public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO PUBLIC;

GRANT ALL ON SCHEMA public TO postgres; 

GRANT ALL ON SCHEMA public TO ubuntu;

CREATE TABLE IF NOT EXISTS usertable (
	name varchar(32) NOT NULL,
	user_id int GENERATED ALWAYS AS IDENTITY,
	PRIMARY KEY(user_id)
);

CREATE TABLE IF NOT EXISTS userinfo (
	info_id int GENERATED ALWAYS AS IDENTITY,
	user_id serial NOT NULL,
	firstname varchar(32) NOT NULL,
	lastname varchar(32) NOT NULL,
	height int,
	weight int,
	dateofbirth date NOT NULL,
	PRIMARY KEY(info_id),
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES usertable(user_id)
);

CREATE TABLE IF NOT EXISTS userstaff (
	staff_id int GENERATED ALWAYS AS IDENTITY,
	user_id serial NOT NULL,
	nurse_id serial NOT NULL,
	doctor_id serial NOT NULL,
	PRIMARY KEY(staff_id),
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES usertable(user_id),
	CONSTRAINT fk_nurse FOREIGN KEY(nurse_id) REFERENCES usertable(user_id),
	CONSTRAINT fk_doctor FOREIGN KEY(doctor_id) REFERENCES usertable(user_id)	
);

CREATE TABLE IF NOT EXISTS userpwd (
	pwd_id int GENERATED ALWAYS AS IDENTITY,
	user_id serial NOT NULL,
	pwd varchar(128),
	PRIMARY KEY(pwd_id),
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES usertable(user_id)
);

CREATE TABLE IF NOT EXISTS prescription (
	prescription_id int GENERATED ALWAYS AS IDENTITY,
	user_id serial NOT NULL,
	nurse_id serial NOT NULL,
	drug_name varchar(64) NOT NULL,
	drug_description varchar(512),
	drug_power int NOT NULL,
	drug_days varchar(16) NOT NULL,
	drug_time varchar(16) NOT NULL,
	expiry date NOT NULL,
	PRIMARY KEY(prescription_id),
	CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES usertable(user_id),
	CONSTRAINT fk_nurse FOREIGN KEY(nurse_id) REFERENCES usertable(user_id)
);