DROP TABLE IF EXISTS `proxy`;
CREATE TABLE IF NOT EXISTS `proxy` (
	`id` INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`host` VARCHAR(255) NOT NULL UNIQUE,
	`username` VARCHAR(255) DEFAULT NULL,
	`password` VARCHAR(255) DEFAULT NULL,
	`port` INT(5) DEFAULT 80
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

INSERT INTO `proxy` (`host`, `username`, `password`, `port`) VALUES
    ('174.122.73.120', 'ip3', 'ohzahnohdohnuyoseeph', 3128),
    ('174.122.73.121', 'ip4', 'eijeerauhovojighohvi', 3128);
