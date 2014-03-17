CREATE TABLE IF NOT EXISTS interaction_sources(
       interaction_source_id		BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       interaction_source_name		VARCHAR(255) NOT NULL,
       interaction_source_url		VARCHAR(255) NULL,
       interaction_source_baseurl	VARCHAR(255) NULL,
       interaction_source_addeddate	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_source_status	ENUM('active','inactive')NOT NULL
);

INSERT INTO interaction_sources(interaction_source_name,interaction_source_url)VALUES('BioGRID','http://thebiogrid.org/');