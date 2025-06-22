CREATE DATABASE `sparq-api-database`;

USE `sparq-api-database`;

CREATE TABLE Reading(
	id INT PRIMARY KEY AUTO_INCREMENT,
	sens_id INT,
	sens_name VARCHAR(100),
	temp INT,
	humi INT,
	carb INT,
	dateserver DATETIME
);