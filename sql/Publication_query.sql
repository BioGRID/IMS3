CREATE TABLE IF NOT EXISTS publication_queries(
       publication_query_id	     BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       project_id		     BIGINT(10) NOT NULL,
       publication_query_value	     TEXT NOT NULL,
       publication_query_addeddate   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       publication_query_lastrun     TIMESTAMP NULL, -- null if never queried
       publication_query_type	     ENUM('manual','automatic') NOT NULL,
       publication_query_status	     ENUM('active','inactive') NOT NULL,
       FOREIGN KEY(project_id)REFERENCES projects(project_id)
);