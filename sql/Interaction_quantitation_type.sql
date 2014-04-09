CREATE TABLE IF NOT EXISTS interaction_quantitation_types(
       interaction_quantitation_type_id	       BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_quantitation_type_name      VARCHAR(255)NOT NULL,
       interaction_quantitation_type_desc      TEXT NULL,
       interaction_quantitation_type_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_quantitation_type_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
);
