CREATE TABLE IF NOT EXISTS  ontology_relationships(
       ontology_relationship_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_term_id                BIGINT(10)NOT NULL,
       ontology_parent_id              BIGINT(10)NOT NULL,
       ontology_relationship_type      VARCHAR(255)NOT NULL,
       ontology_relationship_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_relationship_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(ontology_term_id)REFERENCES ontology_terms(ontology_term_id)
       ,FOREIGN KEY(ontology_parent_id)REFERENCES ontology_terms(ontology_term_id)
);

-- INSERT INTO ontology_relationships(ontology_relationship_id,ontology_term_id,
