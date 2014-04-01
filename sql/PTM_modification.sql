CREATE TABLE IF NOT EXISTS ptm_modifications(
       ptm_modification_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ptm_modification_name   	  VARCHAR(255)NOT NULL,
       ptm_modification_desc   	  TEXT NULL,
       ptm_modification_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ptm_modification_status 	  ENUM('active','inactive')NOT NULL DEFAULT 'ACTIVE'
)