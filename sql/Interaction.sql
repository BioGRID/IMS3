CREATE TABLE IF NOT EXISTS interaction_types(
       interaction_type_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_type_name	  VARCHAR(255)NOT NULL UNIQUE,
       interaction_type_desc	  TEXT NULL,
       interaction_type_dateadded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_type_status	  ENUM('active','inactive')NOT NULL DEFAULT 'active'
);

INSERT INTO interaction_types(interaction_type_name)VALUES
('Protein-Protein'),('Complex');

CREATE TABLE IF NOT EXISTS interactions(
       interaction_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_hash      VARCHAR(64)NULL,
       publication_id        BIGINT(10)NOT NULL,
       interaction_type_id   BIGINT(10)NOT NULL,
       interaction_status    ENUM('normal','error','temporary')NOT NULL DEFAULT 'normal',
       interaction_source_id BIGINT(10)NOT NULL,
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       FOREIGN KEY(interaction_type_id)REFERENCES interaction_types(interaction_type_id),
       FOREIGN KEY(interaction_source_id)REFERENCES interaction_sources(interaction_source_id)
);


-- If this SQL is ever abstracted from the ims22ims3 script, the rest
-- of this file should be moved to the Interaction_ontology.sql file.


CREATE TABLE IF NOT EXISTS interaction_ontology_types(
       interaction_ontology_type_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_ontology_type_name      VARCHAR(255)NOT NULL,
       interaction_ontology_type_desc      TEXT NULL,
       interaction_ontology_type_shortcode VARCHAR(10)NOT NULL,
       interaction_ontology_type_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_ontology_type_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,UNIQUE KEY(interaction_ontology_type_name)
       ,UNIQUE KEY(interaction_ontology_type_shortcode)
);

INSERT INTO interaction_ontology_types(interaction_ontology_type_shortcode,
       interaction_ontology_type_name)VALUES
       ('P','Phenotype'),
       ('CL','Cell line'),
       ('PW','Pathways'),
       ('TS','Tissue specificity'),
       ('CH','Chemical'),
       ('CT','Cell type'),
       ('CC','Cellular Location (GO Celular Component)'),
       ('DS','Disease association'),
       ('DV','Development'),
       ('EV','Environmental');


CREATE TABLE IF NOT EXISTS interaction_ontologies(
       interaction_ontology_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_id                 BIGINT(10)NOT NULL,
       ontology_term_id               BIGINT(10)NOT NULL,
       user_id                        BIGINT(10)NOT NULL DEFAULT 1,
       interaction_ontology_type_id   BIGINT(10)NULL, -- for experimental_systems
       interaction_ontology_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_ontology_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(interaction_id)REFERENCES interactions(interaction_id)
       ,FOREIGN KEY(ontology_term_id)REFERENCES ontology_terms(ontology_term_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
       ,FOREIGN KEY(interaction_ontology_type_id)REFERENCES interaction_ontology_types(interaction_ontology_type_id)
);
