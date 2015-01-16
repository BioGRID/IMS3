CREATE TABLE IF NOT EXISTS participant_tag_mappings(
       participant_tag_mapping_id          BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_tag_id		   BIGINT(10)NOT NULL,
       participant_id			   BIGINT(10)NOT NULL,
       participant_tag_evidence_type_id	   BIGINT(10)NOT NULL,
       participant_tag_evidence_value      VARCHAR(255)NOT NULL,
       participant_tag_evidence_value_text VARCHAR(255)NULL,
       participant_tag_mapping_rank        BIGINT(10)NULL,
       participant_tag_mapping_addeddate   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_tag_mapping_status      ENUM('active','inactive')NOT NULL DEFAULT 'active',
       user_id      			   BIGINT(10)NOT NULL
       ,FOREIGN KEY(participant_tag_id)REFERENCES participant_tags(participant_tag_id)
       ,FOREIGN KEY(participant_id)REFERENCES participants(participant_id)
       ,FOREIGN KEY(participant_tag_evidence_type_id)REFERENCES participant_tag_evidence_types(participant_tag_evidence_type_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
)