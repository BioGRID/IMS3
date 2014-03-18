-- Some day I'll figure out what an iplex is
CREATE TABLE IF NOT EXISTS iplex_projects(
       iplex_project_id			BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       iplex_project_name		VARCHAR(255) UNIQUE NOT NULL,
       iplex_project_fullname		VARCHAR(255) NULL,
       iplex_project_description	TEXT NULL,
       iplex_project_addeddate		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       iplex_project_status		ENUM('active','inactive') NOT NULL
);
