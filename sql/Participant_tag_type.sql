CREATE TABLE IF NOT EXISTS iplex_projects(
       iplex_project_id			BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       iplex_project_name		VARCHAR(255)UNIQUE NOT NULL,
       iplex_project_fullname		VARCHAR(255)NULL,
       iplex_project_description	TEXT NULL,
       iplex_project_addeddate		TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       iplex_project_status		ENUM('active','inactive')NOT NULL DEFAULT 'active'
);

INSERT INTO iplex_projects(iplex_project_name)VALUES('Ubiquitin Project');

CREATE TABLE IF NOT EXISTS participant_tag_types(
       participant_tag_type_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_tag_type_name      VARCHAR(255)NOT NULL UNIQUE,
       participant_tag_type_desc      TEXT,
       iplex_project_id		      BIGINT(10)NOT NULL,
       participant_tag_type_display   ENUM('true','false')NOT NULL DEFAULT 'true', -- Why not boolean?
       participant_tag_type_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_tag_type_status    ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(iplex_project_id)REFERENCES iplex_projects(iplex_project_id)
);
