CREATE TABLE IF NOT EXISTS participant_tag_evidence_types(
       participant_tag_evidence_type_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_tag_evidence_type_name      VARCHAR(255)NOT NULL UNIQUE,
       participant_tag_evidence_type_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_tag_evidence_type_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
);
