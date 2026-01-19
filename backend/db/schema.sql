CREATE DATABASE blood_donation_sys;

USE blood_donation_sys;

CREATE TABLE users (
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	phone VARCHAR(15) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	role ENUM('hospital','blood_bank','donor','admin') NOT NULL,
	is_verified BOOLEAN DEFAULT FALSE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hospitals (
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT UNIQUE NOT NULL,
	hospital_name VARCHAR(150) NOT NULL,
	latitude DECIMAL(9,6),
	longitude DECIMAL(9,6),
	address TEXT,
    
	CONSTRAINT fk_hospital_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE blood_banks (
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT UNIQUE NOT NULL,
	blood_bank_name VARCHAR(150) NOT NULL,
	latitude DECIMAL(9,6),
	longitude DECIMAL(9,6),
	address TEXT,
    
	CONSTRAINT fk_bloodBank_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE donors (
	id INT PRIMARY KEY AUTO_INCREMENT,
	user_id INT UNIQUE NOT NULL,
	blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
	last_donation_date DATE NULL,
	is_available BOOLEAN DEFAULT TRUE,
	latitude DECIMAL(9,6),
	longitude DECIMAL(9,6),
    
	CONSTRAINT fk_donor_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE blood_inventory (
	id INT PRIMARY KEY AUTO_INCREMENT,
	blood_bank_id INT NOT NULL,
	blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
	units_available INT NOT NULL,
	last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_bloodBank_inventory FOREIGN KEY (blood_bank_id) REFERENCES blood_banks(id),
	UNIQUE (blood_bank_id, blood_group)
);

CREATE TABLE blood_requests (
	id INT PRIMARY KEY AUTO_INCREMENT,
	hospital_id INT NOT NULL,
	blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
	units_required INT NOT NULL,
	status ENUM('PENDING','FULFILLED','ALERTED') DEFAULT 'PENDING',
    blood_bank_id INT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
	CONSTRAINT fk_bloodRequest_hospital FOREIGN KEY (hospital_id) REFERENCES hospitals(id), 
	CONSTRAINT fk_bloodRequest_bloodBank FOREIGN KEY (blood_bank_id) REFERENCES blood_banks(id)
);

CREATE TABLE donor_alerts (
	id INT PRIMARY KEY AUTO_INCREMENT,
	blood_request_id INT NOT NULL,
	donor_id INT NOT NULL,
	status ENUM('SENT','ACCEPTED','DECLINED') DEFAULT 'SENT',
	responded_at TIMESTAMP NULL,
    
	CONSTRAINT fk_donorAlert_bloodRequest FOREIGN KEY (blood_request_id) REFERENCES blood_requests(id),
	CONSTRAINT fk_donorAlert_donor FOREIGN KEY (donor_id) REFERENCES donors(id),
	UNIQUE (blood_request_id, donor_id)
);

CREATE TABLE donations (
	id INT PRIMARY KEY AUTO_INCREMENT,
	donor_id INT NOT NULL,
	blood_bank_id INT NOT NULL,
	blood_group ENUM('A+','A-','B+','B-','AB+','AB-','O+','O-'),
	units_donated INT NOT NULL,
	donated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
	CONSTRAINT fk_donation_donor FOREIGN KEY (donor_id) REFERENCES donors(id),
	CONSTRAINT fk_donation_bloodBank FOREIGN KEY (blood_bank_id) REFERENCES blood_banks(id)
);