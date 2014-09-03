CREATE TABLE IF NOT EXISTS pubmed_mappings(
       pubmed_mapping_id      BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       external_database_id   VARCHAR(255) NOT NULL,
       external_database_url  TEXT NOT NULL,
       external_database_name VARCHAR(255) NOT NULL,
       publication_pubmed_id  BIGINT(10)NOT NULL,
       UNIQUE KEY(external_database_name,external_database_id)
       --       FOREIGN KEY(publication_pubmed_id)REFERENCES publications(publication_pubmed_id)
);
