CREATE TABLE IF NOT EXISTS ontologies(
       ontology_id         BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_name	   VARCHAR(255)NOT NULL UNIQUE,
       ontology_url	   TEXT NULL, -- UNIQUE,
       ontology_rootid	   BIGINT(10)NULL, -- humph
       ontology_addeddate  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_lastparsed TIMESTAMP NULL,
       ontology_status     ENUM('active','inactive')NOT NULL DEFAULT'active'
       -- FOREIGN KEY(ontology_rootid)REFERENCES ontology_terms(ontology_term_id)
);

-- foreign key created in Ontology_term.sql

-- Insert IMS specific ontology for "Experimental Evidence and Annotation"
INSERT INTO ontologies(ontology_id,ontology_name)
VALUES(1,'Experimental Evidence and Annotation');
