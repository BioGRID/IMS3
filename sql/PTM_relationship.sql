CREATE TABLE IF NOT EXISTS ptm_relationships(
       ptm_relationship_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ptm_id                     BIGINT(10)NOT NULL,
       participant_id    	  BIGINT(10)NOT NULL,
       ptm_relationship_type	  ENUM('activates','inhibits')NOT NULL,
       publication_id		  BIGINT(10)NOT NULL,
       user_id			  BIGINT(10)NOT NULL,
       ptm_relationship_identity  ENUM('catalytic','regulatory')NOT NULL,
       ptm_relationship_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ptm_relationship_status	  ENUM('active','inactive'),
       FOREIGN KEY(ptm_id)REFERENCES ptms(ptm_id),
       FOREIGN KEY(participant_id)REFERENCES participants(participant_id),
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       FOREIGN KEY(user_id)REFERENCES users(user_id)
)