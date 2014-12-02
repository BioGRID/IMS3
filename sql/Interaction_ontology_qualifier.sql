CREATE TABLE IF NOT EXISTS interaction_ontologies_qualifiers(
       interaction_ontology_qualifier_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_ontology_id                  BIGINT(10)NOT NULL,
       ontology_term_id                         BIGINT(10)NOT NULL,
       user_id                                  BIGINT(10)NOT NULL DEFAULT 1,
       interaction_ontology_qualifier_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_ontology_qualifier_status	ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(interaction_ontology_id)REFERENCES interaction_ontologies(interaction_ontology_id)
       ,FOREIGN KEY(ontology_term_id)REFERENCES ontology_terms(ontology_term_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
)