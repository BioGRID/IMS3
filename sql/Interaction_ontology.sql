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

CREATE TABLE IF NOT EXISTS interaction_ontologies_notes(
       interaction_ontology_note_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_ontology_id             BIGINT(10)NOT NULL,
       interaction_ontology_note_text      TEXT NOT NULL,
       user_id                             BIGINT(10)NOT NULL,
       interaction_ontology_note_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_ontology_note_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(interaction_ontology_id)REFERENCES interaction_ontologies(interaction_ontology_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
);
