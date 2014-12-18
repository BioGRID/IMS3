-- The interaction_ontology and interaction_ontology types tables are
-- created in the Interaction.sql file.


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
