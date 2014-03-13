CREATE TABLE IF NOT EXISTS users(
       user_id		BIGINT(10) PRIMARY KEY,
       user_name	VARCHAR(255) UNIQUE NOT NULL,
       user_password	VARCHAR(64) NOT NULL,
       user_cookie	VARCHAR(64) NULL,
       user_firstname	VARCHAR(255) NULL,
       user_lastname	VARCHAR(255) NULL,
       user_email	VARCHAR(255) NOT NULL,
       user_addedate	DATETIME NOT NULL,
       user_lastaccess	DATETIME NOT NULL,
       user_role	ENUM('curator','admin','observer'),
       project_id	BIGINT(10),
       FOREIGN KEY(project_id)REFERENCES projects(project_id)
);

CREATE TABLE IF NOT EXISTS project_users(
       project_user_id		BIGINT(10) PRIMARY KEY,
       project_id		BIGINT(10) NOT NULL,
       user_id			BIGINT(10) NOT NULL,
       project_user_status	ENUM('active','inactive') NOT NULL,
       project_user_addeddate	DATETIME,
       FOREIGN KEY(project_id)REFERENCES projects(project_id),
       FOREIGN KEY(user_id)REFERENCES users(user_id),
       UNIQUE KEY(project_id,user_id)
);
