DROP TABLE IF EXISTS `settings`;
DROP TABLE IF EXISTS `domains`;
DROP TABLE IF EXISTS `proxies`;
DROP TABLE IF EXISTS `google_domains`;
DROP TABLE IF EXISTS `google_search`;
DROP TABLE IF EXISTS `keywords`;

CREATE TABLE IF NOT EXISTS `settings` (
	`key` VARCHAR(255) NOT NULL,
	`value` TEXT NULL,
	PRIMARY KEY(`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO settings VALUES('version', '1');

CREATE TABLE IF NOT EXISTS `keywords` (
	`keyword` VARCHAR(255) NOT NULL PRIMARY KEY,
	`lr` VARCHAR(10) NOT NULL DEFAULT 'lang_en',
	`cr` VARCHAR(10) NOT NULL DEFAULT 'countryUS'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO keywords (`keyword`) VALUES
	('resume writing'),
	('resume writing service'),
	('resume writing services'),
	('resume writing service biz'),
	('professional resume writing service'),
	('linkedin profile development service'),
	('linked profile development and resume writing service'),
	('residency personal statement'),
	('residency personal statements'),
	('medical residency personal statements'),
	('nursing residency personal statements'),
	('neurology residency personal statement'),
	('residency personal statement writing service'),
	('help writing residency personal statements'),
	('residency personal statement writing services');

CREATE TABLE IF NOT EXISTS `domains` (
	`host` VARCHAR(255) NOT NULL,
	PRIMARY KEY(`host`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO domains VALUES
	('resumewritingservice.biz'),
	('residencypersonalstatements.net');

CREATE TABLE IF NOT EXISTS `proxies` (
	`host` VARCHAR(255) NOT NULL,
	`username` VARCHAR(255) DEFAULT NULL,
	`password` VARCHAR(255) DEFAULT NULL,
	`port` INT DEFAULT 80,
	PRIMARY KEY(`host`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
INSERT INTO proxies VALUES
	('174.122.73.120', 'ip3', 'ohzahnohdohnuyoseeph', 3128),
	('174.122.73.121', 'ip4', 'eijeerauhovojighohvi', 3128);

CREATE TABLE IF NOT EXISTS `google_search` (
	`keyword` VARCHAR(255) NOT NULL,
	`date` DATE NOT NULL,
	`page` INT(2) NOT NULL,
	`status` VARCHAR(255) NOT NULL,
	`retries` INT(1) NOT NULL,
	`response` TEXT,
	PRIMARY KEY(`keyword`, `date`, `page`),
	FOREIGN KEY(`keyword`) REFERENCES `keywords`(`keyword`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS `google_domains` (
	`keyword` VARCHAR(255) NOT NULL,
	`date` DATE NOT NULL,
	`page` INT(2) NOT NULL,
	`position` INT(3) NOT NULL,
	`domain` VARCHAR(255),
	`url` VARCHAR(500),
	PRIMARY KEY(`keyword`, `date`, `position`),
	INDEX(`keyword`, `date`, `page`),
	FOREIGN KEY(`keyword`, `date`, `page`) REFERENCES `google_search`(`keyword`, `date`, `page`) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
