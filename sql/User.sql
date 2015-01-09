CREATE TABLE IF NOT EXISTS users(
       user_id		BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       user_name	VARCHAR(255) UNIQUE NOT NULL,
       user_password	VARCHAR(64) NOT NULL,
       user_cookie	VARCHAR(64) NULL,
       user_firstname	VARCHAR(255) NOT NULL,
       user_lastname	VARCHAR(255) NOT NULL,
       user_email	VARCHAR(255) NULL,
       user_addeddate	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       user_lastaccess	TIMESTAMP NULL, -- NULL means never accessed
       user_role	ENUM('curator','admin','observer')NOT NULL,
       project_id	BIGINT(10)NOT NULL,
       user_status      ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(project_id)REFERENCES projects(project_id)
);
