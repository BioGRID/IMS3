
CREATE TABLE IF NOT EXISTS project_users(
       project_user_id		BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       project_id		BIGINT(10) NOT NULL,
       user_id			BIGINT(10) NOT NULL,
       project_user_status	ENUM('active','inactive') NOT NULL,
       project_user_addeddate	DATETIME,
       FOREIGN KEY(project_id)REFERENCES projects(project_id),
       FOREIGN KEY(user_id)REFERENCES users(user_id),
       UNIQUE KEY(project_id,user_id)
);
