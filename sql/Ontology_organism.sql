CREATE TABLE IF NOT EXISTS ontology_organisms(
       ontology_organism_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_id                 BIGINT(10)NOT NULL, 
       organism_id                 BIGINT(10)NOT NULL, -- fake foreign key to quick_organisms
       ontology_organism_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_organism_status	   ENUM('active','inactive')NOT NULL DEFAULT 'active',
       UNIQUE KEY(ontology_id,organism_id),
       FOREIGN KEY(ontology_id)REFERENCES ontologies(ontology_id)
)

-- must be careful as ontology_ids have been slightly renumbered
-- porting from IMS2.