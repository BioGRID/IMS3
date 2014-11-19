CREATE TABLE IF NOT EXISTS ontology_terms(
       ontology_term_id		    BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_term_official_id    VARCHAR(255)NOT NULL,
       ontology_term_name	    VARCHAR(255)NOT NULL,
       ontology_term_desc           TEXT NULL,
       ontology_term_synonymns      TEXT NULL,
       ontology_term_replacement    VARCHAR(255)NULL,
       ontology_term_subsets        TEXT,
       ontology_term_preferred_name VARCHAR(255)NULL,
       ontology_id		    BIGINT(10)NOT NULL,
       ontology_term_addeddate	    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_term_status	    ENUM('active','inactive')NOT NULL DEFAULT 'active',
       ontology_term_childcount	    BIGINT(10)NOT NULL,
       ontology_term_parent	    TEXT NULL,
       FOREIGN KEY(ontology_id)REFERENCES ontologies(ontology_id),
       UNIQUE KEY(ontology_term_id,ontology_term_official_id),
       UNIQUE KEY(ontology_term_id,ontology_term_name)
);

ALTER TABLE ontologies
ADD FOREIGN KEY(ontology_rootid)REFERENCES ontology_terms(ontology_term_id);