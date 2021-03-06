CREATE TABLE IF NOT EXISTS projects(
       project_id	   BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       project_name	   VARCHAR(255)UNIQUE NOT NULL,
       project_description TEXT NULL,
       project_addeddate   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       organism_id	   BIGINT(10),
       project_status	   ENUM('public','private')NOT NULL DEFAULT 'public'
);
