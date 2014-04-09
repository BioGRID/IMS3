CREATE TABLE IF NOT EXISTS interaction_quantitations(
       interaction_quantitation_id	   BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_quantitation_value	   DOUBLE NOT NULL,
       interaction_quantitation_type_id   BIGINT(10)NOT NULL,
       user_id				   BIGINT(10)NOT NULL,
       interaction_quantitation_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_quantitation_status	   ENUM('active','inactive')NOT NULL DEFAULT 'active',
       interaction_id			   BIGINT(10)NOT NULL,
       FOREIGN KEY(interaction_quantitation_type_id)REFERENCES interaction_quantitation_types(interaction_quantitation_type_id),
       FOREIGN KEY(interaction_id)REFERENCES interactions(interaction_id)
)
