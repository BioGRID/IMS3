CREATE TABLE IF NOT EXISTS project_publications(
       project_publication_id	     BIGINT(10) PRIMARY KEY AUTO_INCREMENT,
       project_id		     BIGINT(10) NOT NULL,
       publication_id		     BIGINT(10) NULL,
       project_publication_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       project_publication_status    ENUM('normal','high','error','processed','low') NOT NULL,
       publication_query_id	     BIGINT(10) NULL,
       FOREIGN KEY(project_id)REFERENCES projects(project_id),
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       FOREIGN KEY(publication_query_id)REFERENCES publication_queries(publication_query_id)
);