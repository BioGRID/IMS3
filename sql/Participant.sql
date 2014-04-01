CREATE TABLE IF NOT EXISTS participants(
       participant_id	     BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       participant_value     BIGINT(10), -- phony foreign key
       participant_type_id   BIGINT(10),
       participant_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_status    ENUM('active','inactive')NOT NULL DEFAULT 'active',
       UNIQUE KEY(participant_value,participant_type_id)
       )