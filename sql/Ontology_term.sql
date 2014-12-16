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
INSERT INTO ontology_terms(ontology_term_id,ontology_term_official_id,ontology_term_name,ontology_term_desc,ontology_id,ontology_term_childcount,ontology_term_addeddate)VALUES
( 1,'BIOGRID_IMS:0000001','Root',NULL,1,32,NULL),
( 2,'BIOGRID_IMS:0000002','Biochemical','h1',1,19,NULL),

( 3,'BIOGRID_IMS:0000003','In vivo','h2 under Biochemical',1,11,'2010-01-18 15:16:48'),
( 4,'BIOGRID_IMS,0000004','Affinity Capture-Luminescence','An interaction is inferred when a bait protein, tagged with luciferase, is enzymatically detected in immunoprecipitates of the prey protein as light emission. The prey protein is affinity captured from cell extracts by either polyclonal antibody or epitope tag.',1,0,'2008-09-30 15:38:36'),
( 5,'BIOGRID_IMS,0000005','Affinity Capture-MS','An interaction is inferred when a bait protein is affinity captured from cell extracts by either polyclonal antibody or epitope tag and the associated interaction partner is identified by mass spectrometric methods.',1,0,'2008-09-30 17:39:18'),
( 6,'BIOGRID_IMS,0000006','Affinity Capture-RNA','An interaction is inferred when a bait protein is affinity captured from cell extracts by either polyclonal antibody or epitope tag and associated RNA species identified by Northern blot, RT-PCR, affinity labeling, sequencing, or microarray analysis.',1,0,'2009-02-26 15:19:35'),
( 7,'BIOGRID_IMS,0000007','Affinity Capture-Western','An interaction is inferred when a bait protein is affinity captured from cell extracts by either polyclonal antibody or epitope tag and the associated interaction partner identified by Western blot with a specific polyclonal antibody or second epitope tag. This category is also used if an interacting protein is visualized directly by dye stain or radioactivity. Note that this differs from any co-purification experiment involving affinity capture in that the co-purification experiment involves at least one extra purification step to get rid of potential contaminating proteins.',1,0,NULL),
( 8,'BIOGRID_IMS,0000008','Co-fractionation','Interaction inferred from the presence of two or more protein subunits in a partially purified protein preparation. If co-fractionation is demonstrated between 3 or more proteins, then add them as a complex.',1,0,'2008-09-30 15:39:03'),
( 9,'BIOGRID_IMS,0000009','Co-localization','Interaction inferred from two proteins that co-localize in the cell by indirect immunofluorescence only when in addition, if one gene is deleted, the other protein becomes mis-localized. Also includes co-dependent association of proteins with promoter DNA in chromatin immunoprecipitation experiments.',1,0,'2008-07-30 17:30:53'),
(10,'BIOGRID_IMS,0000010','Co-purification','An interaction is inferred from the identification of two or more protein subunits in a purified protein complex, as obtained by classical biochemical fractionation or affinity purification and one or more additional fractionation steps.',1,0,'2008-07-30 17:31:57'),
(11,'BIOGRID_IMS,0000011','FRET','An interaction is inferred when close proximity of interaction partners is detected by fluorescence resonance energy transfer between pairs of fluorophore-labeled molecules, such as occurs between CFP (donor) and YFP (acceptor) fusion proteins.',1,0,'2008-07-30 17:40:54'),
(12,'BIOGRID_IMS,0000012','PCA','A Protein-Fragment Complementation Assay (PCA) is a protein-protein interaction assay in which a bait protein is expressed as fusion to one of the either N- or C- terminal peptide fragments of a reporter protein and prey protein is expressed as fusion to the complementary N- or C- terminal fragment of the same reporter protein. Interaction of bait and prey proteins bring together complementary fragments, which can then fold into an active reporter, e.g. the split-ubiquitin assay.',1,0,'2008-09-30 15:39:16'),
(13,'BIOGRID_IMS,0000013','Proximity Label-MS','An interaction is inferred when a bait-enzyme fusion protein selectively modifies a vicinal protein with a diffusible reactive product, followed by affinity capture of the modified protein and identification by mass spectrometric methods.',1,0,'2008-09-30 17:39:18'),
(14,'BIOGRID_IMS,0000014','Two-hybrid','Bait protein expressed as a DNA binding domain (DBD) fusion and prey expressed as a transcriptional activation domain (TAD) fusion and interaction measured by reporter gene activation.',1,0,'2008-09-30 15:40:22'),

(15,'BIOGRID_IMS,0000015','In vitro','h2 under Biochemical',1,6,'2010-01-18 15:17:04'),
(16,'BIOGRID_IMS,0000016','Biochemical Activity','An interaction is inferred from the biochemical effect of one protein upon another, for example, GTP-GDP exchange activity or phosphorylation of a substrate by a kinase. The bait protein executes the activity on the substrate hit protein. A Modification value is recorded for interactions of this type with the possible values Phosphorylation, Ubiquitination, Sumoylation, Dephosphorylation, Methylation, Prenylation, Acetylation, Deubiquitination, Proteolytic Processing, Glucosylation, Nedd(Rub1)ylation, Deacetylation, No Modification, Demethylation.',1,0,'2008-09-30 23:45:48'),
(17,'BIOGRID_IMS,0000017','Co-crystal Structure','Interaction directly demonstrated at the atomic level by X-ray crystallography. Also used for NMR or Electron Microscopy (EM) structures. If there is no obvious bait-hit directionality to the interaction involving 3 or more proteins, then the co-crystallized proteins should be listed as a complex.',1,0,'2008-09-30 15:40:57'),
(18,'BIOGRID_IMS,0000018','Far Western','An interaction is detected between a protein immobilized on a membrane and a purified protein probe.',1,0,'2008-07-30 17:39:27'),
(19,'BIOGRID_IMS,0000019','Protein-peptide','An interaction is detected between a protein and a peptide derived from an interaction partner. This includes phage display experiments.',1,0,NULL),
(20,'BIOGRID_IMS,0000020','Protein-RNA','An interaction is detected between and protein and an RNA in vitro.',1,0,'2008-09-30 15:36:08'),
(21,'BIOGRID_IMS,0000021','Reconstituted Complex','An interaction is detected between purified proteins in vitro.',1,0,'2008-07-30 17:54:30'),

(22,'BIOGRID_IMS:0000022','Genetic','h1',1,11,'2005-10-13'),
(23,'BIOGRID_IMS:0000023','Dosage Growth Defect','A genetic interaction is inferred when over expression or increased dosage of one gene causes a growth defect in a strain that is mutated or deleted for another gene.',1,0,'2008-07-30 17:32:59'),
(24,'BIOGRID_IMS:0000024','Dosage Lethality','A genetic interaction is inferred when over expression or increased dosage of one gene causes lethality in a strain that is mutated or deleted for another gene.',1,0,'2008-07-30 17:34:15'),
(25,'BIOGRID_IMS:0000025','Dosage Rescue','A genetic interaction is inferred when over expression or increased dosage of one gene rescues the lethality or growth defect of a strain that is mutated or deleted for another gene.',1,0,'2008-07-30 17:35:25'),
(26,'BIOGRID_IMS:0000026','Negative Genetic','Mutations/deletions in separate genes, each of which alone causes a minimal phenotype, but when combined in the same cell results in a more severe fitness defect or lethality under a given condition. This term is reserved for high or low throughput studies with scores.',1,0,'2010-01-18 14:45:06'),
(27,'BIOGRID_IMS:0000027','Phenotypic Enhancement','A genetic interaction is inferred when mutation or overexpression of one gene results in enhancement of any phenotype (other than lethality/growth defect) associated with mutation or over expression of another gene.',1,0,'2008-08-28 11:54:20'),
(28,'BIOGRID_IMS:0000028','Phenotypic Suppression','A genetic interaction is inferred when mutation or over expression of one gene results in suppression of any phenotype (other than lethality/growth defect) associated with mutation or over expression of another gene.',1,0,'2008-07-30 17:51:37'),
(29,'BIOGRID_IMS:0000029','Positive Genetic','Mutations/deletions in separate genes, each of which alone causes a minimal phenotype, but when combined in the same cell results in a less severe fitness defect than expected under a given condition. This term is reserved for high or low throughput studies with scores.',1,0,'2010-01-18 15:23:28'),
(30,'BIOGRID_IMS:0000030','Synthetic Growth Defect','A genetic interaction is inferred when mutations in separate genes, each of which alone causes a minimal phenotype, result in a significant growth defect under a given condition when combined in the same cell.',1,0,'2008-07-30 17:55:32'),
(31,'BIOGRID_IMS:0000031','Synthetic Haploinsufficiency','A genetic interaction is inferred when mutations or deletions in separate genes, at least one of which is hemizygous, cause a minimal phenotype alone but result in lethality when combined in the same cell under a given condition.',1,0,'2008-09-30 15:39:29'),
(32,'BIOGRID_IMS:0000032','Synthetic Lethality','A genetic interaction is inferred when mutations or deletions in separate genes, each of which alone causes a minimal phenotype, result in lethality when combined in the same cell under a given condition.',1,0,'2008-07-30 17:57:29'),
(33,'BIOGRID_IMS:0000033','Synthetic Rescue','A genetic interaction is inferred when mutations or deletions of one gene rescues the lethality or growth defect of a strain mutated or deleted for another gene.',1,0,'2008-07-30 17:58:22');

UPDATE ontologies SET ontology_rootid=1 WHERE ontology_id=1;
