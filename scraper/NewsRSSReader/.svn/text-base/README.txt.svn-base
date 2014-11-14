 === README for NewsRSSReader === 

 This project serves as a component of the CS242 Final Project FA14, written by Zefu Lu.

0. Package Requirements
	In order to run the program successfully, one needs the following Python Packages:
	MySQLdb, urllib2, xml, ConfigParser, lxml, dateutil

1. Database Setup:
	(1) Open MySQL as root
	(2) Execute the following commands:
		CREATE DATABASE NewsRSS;
		USE NewsRSS;
		CREATE TABLE topics ( 
			news_id MEDIUMINT NOT NULL AUTO_INCREMENT, 
			title VARCHAR(255),
			date DATETIME, 
			content TEXT,
			url VARCHAR(255),
			source VARCHAR(255),
			PRIMARY KEY (news_id)) ENGINE=InnoDB;
	(3) Create user:
		CREATE USER rss_client@localhost IDENTIFIED BY 'mypass';
		GRANT ALL ON NewsRSS.topics TO rss_client@localhost;

2. Crontab setup:
	(1) See http://en.wikipedia.org/wiki/Cron for more info.