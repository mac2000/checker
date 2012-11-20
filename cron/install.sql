DROP TABLE IF EXISTS `cron`;
CREATE TABLE IF NOT EXISTS `cron` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `date` DATE NOT NULL,
    `keyword` VARCHAR(500) NOT NULL,
    `lr` VARCHAR(10) NOT NULL DEFAULT 'lang_en',
    `cr` VARCHAR(10) NOT NULL DEFAULT 'countryUS',
    `position` INT(3) NOT NULL,
    `domain` VARCHAR(500) NOT NULL,
    `url` VARCHAR(500) NOT NULL,
    PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
