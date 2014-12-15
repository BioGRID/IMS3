CREATE TABLE IF NOT EXISTS dataset_queue(
       dataset_queue_id                BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       dataset_queue_filename          VARCHAR(255)NOT NULL,
       dataset_queue_data              LONGBLOB,
       dataset_queue_filesize          DOUBLE,
       user_id                         BIGINT(10)NOT NULL,
       project_id                      BIGINT(10)NOT NULL,
       dataset_queue_interaction_count BIGINT(10)NOT NULL,
       dataset_queue_forced	       BIGINT(10)NOT NULL DEFAULT 0, -- just add to interaction_count?
       dataset_queue_addeddate	       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       dataset_queue_status	       ENUM('new','processed')NOT NULL DEFAULT 'new'
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
       ,FOREIGN KEY(project_id)REFERENCES projects(project_id)
)
