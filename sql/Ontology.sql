CREATE TABLE IF NOT EXISTS ontologies(
       ontology_id         BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_name	   VARCHAR(255)NOT NULL UNIQUE,
       ontology_url	   TEXT NULL, -- UNIQUE,
       ontology_rootid	   BIGINT(10)NULL, -- humph
       ontology_addeddate  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_lastparsed TIMESTAMP NULL,
       ontology_status     ENUM('active','hidden','inactive')NOT NULL DEFAULT'active'
       -- FOREIGN KEY(ontology_rootid)REFERENCES ontology_terms(ontology_term_id)
);

-- foreign key created in Ontology_term.sql

-- Insert IMS specific ontology for IMS2.experimental_systems stuff.
INSERT INTO ontologies(ontology_id,ontology_name,ontology_status)VALUES
(1,'experimental_systems','hidden'), -- hardcoded in www/ims/html/interaction.htm
(2,'throughputs','hidden');
-- Hidden means active but don't display in IMS3
