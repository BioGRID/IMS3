CREATE TABLE IF NOT EXISTS unknown_participants(
       unknown_participant_id	      BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       unknown_participant_identifier VARCHAR(255)NOT NULL,
       participant_type_id	      VARCHAR(255)NOT NULL,
       organism_id		      BIGINT(10)NULL,
       publication_id		      BIGINT(10)NOT NULL,
       unknown_participant_addeddate  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       unknown_participant_status     ENUM('active','inactive')NOT NULL DEFAULT 'active',
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       UNIQUE KEY(unknown_participant_identifier,participant_type_id,organism_id,publication_id)
)