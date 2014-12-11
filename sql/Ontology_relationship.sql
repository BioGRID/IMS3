CREATE TABLE IF NOT EXISTS  ontology_relationships(
       ontology_relationship_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ontology_term_id                BIGINT(10)NOT NULL,
       ontology_parent_id              BIGINT(10)NULL, -- NULL mean root?
       ontology_relationship_type      VARCHAR(255)NOT NULL,
       ontology_relationship_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ontology_relationship_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(ontology_term_id)REFERENCES ontology_terms(ontology_term_id)
       ,FOREIGN KEY(ontology_parent_id)REFERENCES ontology_terms(ontology_term_id)
);



INSERT INTO ontology_relationships
(ontology_relationship_id,ontology_term_id,ontology_parent_id,ontology_relationship_type)VALUES
( 1, 1,NULL,'root'), -- root
( 2, 2,   1,'head'), -- Biochemical
( 3, 3,   2,'stem'), -- In vivo
( 4, 4,   3,'leaf'),
( 5, 5,   3,'leaf'),
( 6, 6,   3,'leaf'),
( 7, 7,   3,'leaf'),
( 8, 8,   3,'leaf'),
( 9, 9,   3,'leaf'),
(10,10,   3,'leaf'),
(11,11,   3,'leaf'),
(12,12,   3,'leaf'),
(13,13,   3,'leaf'),
(14,14,   3,'leaf'),
(15,15,   2,'stem'), -- In vitro
(16,16,  15,'leaf'),
(17,17,  15,'leaf'),
(18,18,  15,'leaf'),
(19,19,  15,'leaf'),
(20,20,  15,'leaf'),
(21,21,  15,'leaf'),
(22,22,   1,'stem'), -- Genetic
(23,23,  22,'leaf'),
(24,24,  22,'leaf'),
(25,25,  22,'leaf'),
(26,26,  22,'leaf'),
(27,27,  22,'leaf'),
(28,28,  22,'leaf'),
(29,29,  22,'leaf'),
(30,30,  22,'leaf'),
(31,31,  22,'leaf'),
(32,32,  22,'leaf'),
(33,33,  22,'leaf');
