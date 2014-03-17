CREATE TABLE IF NOT EXISTS projects(
       project_id		BIGINT(10) PRIMARY KEY,
       project_name		VARCHAR(255) UNIQUE NOT NULL,
       project_description	TEXT NOT NULL,
       project_addeddate	TIMESTAMP NOT NULL,
       organism_id		BIGINT(10),
       project_status		ENUM('public','private') NOT NULL
);
