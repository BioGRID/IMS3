CREATE TABLE IF NOT EXISTS ptm_sources(
       ptm_source_id	    BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       ptm_source_name	    VARCHAR(255)NOT NULL,
       ptm_source_desc	    TEXT NULL,
       ptm_source_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ptm_source_status    ENUM('active','inactive')NOT NULL
)