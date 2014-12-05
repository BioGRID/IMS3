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

CREATE INDEX i_ontology_terms_oid ON ontology_terms(ontology_term_official_id)USING HASH;
-- The following is done in ims2.py, it's not done here because the
-- circular foreign keys confuse mysql durning loading.
-- ALTER TABLE ontologies
-- ADD FOREIGN KEY(ontology_rootid)REFERENCES ontology_terms(ontology_term_id);

-- "Experimental Evidence and Annotation" terms.  Current I'm using
-- ontology_term_description to record the level they are at, but feel
-- free to add proper descriptions.
INSERT INTO ontology_terms(ontology_term_id,ontology_term_official_id,ontology_term_name,ontology_term_desc,ontology_id,ontology_term_childcount)VALUES
( 1,'BIOGRID_IMS:0000001','Root',NULL,1,32),
( 2,'BIOGRID_IMS:0000002','Biochemical','h1',1,19),

( 3,'BIOGRID_IMS:0000003','In vivo','h2 under Biochemical',1,11),
( 4,'BIOGRID_IMS,0000004','Affinity Capture-Luminescence','h3 leaf under In vivo',1,0),
( 5,'BIOGRID_IMS,0000005','Affinity Capture-MS','h3 leaf under In vivo',1,0),
( 6,'BIOGRID_IMS,0000006','Affinity Capture-RNA','h3 leaf under In vivo',1,0),
( 7,'BIOGRID_IMS,0000007','Affinity Capture-Western','h3 leaf under In vivo',1,0),
( 8,'BIOGRID_IMS,0000008','Co-fractionation','h3 leaf under In vivo',1,0),
( 9,'BIOGRID_IMS,0000009','Co-localization','h3 leaf under In vivo',1,0),
(10,'BIOGRID_IMS,0000010','Co-purification','h3 leaf under In vivo',1,0),
(11,'BIOGRID_IMS,0000011','FRET','h3 leaf under In vivo',1,0),
(12,'BIOGRID_IMS,0000012','PCA','h3 leaf under In vivo',1,0),
(13,'BIOGRID_IMS,0000013','Proximity Label-MS','h3 leaf under In vivo',1,0),
(14,'BIOGRID_IMS,0000014','Two-hybrid','h3 leaf under In vivo',1,0),

(15,'BIOGRID_IMS,0000016','In vitro','h2 under Biochemical',1,6),
(16,'BIOGRID_IMS,0000016','Biochemical Activity','h3 leaf under In vitro',1,0),
(17,'BIOGRID_IMS,0000017','Co-crystal Structure','h3 leaf under In vitro',1,0),
(18,'BIOGRID_IMS,0000018','Far Western','h3 leaf under In vitro',1,0),
(19,'BIOGRID_IMS,0000019','Protein-peptide','h3 leaf under In vitro',1,0),
(20,'BIOGRID_IMS,0000020','Protein-RNA','h3 leaf under In vitro',1,0),
(21,'BIOGRID_IMS,0000021','Reconstituted Complex','h3 leaf under In vitro',1,0),

(22,'BIOGRID_IMS:0000022','Genetic','h1',1,11),
(23,'BIOGRID_IMS:0000023','Dosage Growth Defect','h2 leaf under Genetic',1,0),
(24,'BIOGRID_IMS:0000024','Dosage Lethality','h2 leaf under Genetic',1,0),
(25,'BIOGRID_IMS:0000025','Dosage Rescue','h2 leaf under Genetic',1,0),
(26,'BIOGRID_IMS:0000026','Negative Genetic','h2 leaf under Genetic',1,0),
(27,'BIOGRID_IMS:0000027','Phenotypic Enhancement','h2 leaf under Genetic',1,0),
(28,'BIOGRID_IMS:0000028','Phenotypic Suppression','h2 leaf under Genetic',1,0),
(29,'BIOGRID_IMS:0000029','Positive Genetic','h2 leaf under Genetic',1,0),
(30,'BIOGRID_IMS:0000030','Synthetic Growth Defect','h2 leaf under Genetic',1,0),
(31,'BIOGRID_IMS:0000031','Synthetic Haploinsufficiency','h2 leaf under Genetic',1,0),
(32,'BIOGRID_IMS:0000032','Synthetic Lethality','h2 leaf under Genetic',1,0),
(33,'BIOGRID_IMS:0000033','Synthetic Rescue','h2 leaf under Genetic',1,0);

UPDATE ontologies SET ontology_rootid=1 WHERE ontology_id=1;
