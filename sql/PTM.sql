CREATE TABLE IF NOT EXISTS ptms(
       ptm_id	            BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_id	    BIGINT(10)NOT NULL,
       ptm_residue_location BIGINT(10)NOT NULL,
       ptm_residue	    VARCHAR(1)NOT NULL,
       ptm_modification_id  BIGINT(10)NOT NULL,
       publication_id	    BIGINT(10)NOT NULL,
       ptm_source_id	    BIGINT(10)NOT NULL,
       ptm_status 	    ENUM('experimental','inferred')NOT NULL,
       FOREIGN KEY(participant_id)REFERENCES participants(participant_id),
       FOREIGN KEY(ptm_modification_id)REFERENCES ptm_modifications(ptm_modification_id),
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       FOREIGN KEY(ptm_source_id)REFERENCES ptm_sources(ptm_source_id)
)