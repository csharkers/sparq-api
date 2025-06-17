USE `sparq-api-database`;

CREATE TABLE Reading(
	id INT PRIMARY KEY AUTO_INCREMENT,
	sens_id INT,
	temp INT,
	humi INT,
	carb INT,
	dateserver DATETIME
);