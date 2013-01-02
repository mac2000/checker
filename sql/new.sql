DROP VIEW IF EXISTS keywords_domains_view;
DROP VIEW IF EXISTS search_results_view;
DROP TABLE IF EXISTS search_results;
DROP TABLE IF EXISTS keywords_domains;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS domains;

CREATE TABLE IF NOT EXISTS keywords (
	id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	keyword  VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS domains (
	id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
	domain  VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE IF NOT EXISTS keywords_domains (
	id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,	
	keyword_id INT UNSIGNED NOT NULL,
	domain_id INT UNSIGNED NOT NULL,
	UNIQUE INDEX(keyword_id, domain_id),
	FOREIGN KEY(keyword_id) REFERENCES keywords(id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(domain_id) REFERENCES domains(id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE VIEW keywords_domains_view AS
SELECT keyword, domain FROM keywords_domains
LEFT JOIN keywords ON keywords_domains.keyword_id = keywords.id
LEFT JOIN domains ON keywords_domains.domain_id = domains.id;

INSERT INTO domains VALUES(NULL, 'resumewritingservice.biz');
SET @id_1 = LAST_INSERT_ID();

INSERT INTO domains VALUES(NULL, 'residencypersonalstatements.net');
SET @id_2 = LAST_INSERT_ID();

INSERT INTO keywords VALUES(NULL, 'resume writing');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'resume writing service');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'resume writing services');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'resume writing service biz');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'professional resume writing service');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'linkedin profile development service');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);
INSERT INTO keywords VALUES(NULL, 'linked profile development and resume writing service');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_1);

INSERT INTO keywords VALUES(NULL, 'residency personal statement');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'residency personal statements');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'medical residency personal statements');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'nursing residency personal statements');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'neurology residency personal statement');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'residency personal statement writing service');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'help writing residency personal statements');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);
INSERT INTO keywords VALUES(NULL, 'residency personal statement writing services');
INSERT INTO keywords_domains VALUES(NULL, LAST_INSERT_ID(), @id_2);

CREATE TABLE IF NOT EXISTS search_results (
	search_date DATE NOT NULL,	
	keywords_domains_id INT UNSIGNED NOT NULL,
	position INT UNSIGNED NULL DEFAULT NULL,
	PRIMARY KEY(search_date, keywords_domains_id),
	FOREIGN KEY(keywords_domains_id) REFERENCES keywords_domains(id) ON UPDATE CASCADE ON DELETE CASCADE	
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE VIEW search_results_view AS
SELECT search_date, keyword, domain, position FROM search_results
LEFT JOIN keywords_domains ON search_results.keywords_domains_id = keywords_domains.id
LEFT JOIN keywords ON keywords_domains.keyword_id = keywords.id
LEFT JOIN domains ON keywords_domains.domain_id = domains.id;