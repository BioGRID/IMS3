CREATE TABLE IF NOT EXISTS interaction_history(
       interaction_history_id	   BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       modification_type	   ENUM('ACTIVATED','DISABLED','DEACTIVATED','UPDATED')NOT NULL,
       interaction_id              BIGINT(10)NOT NULL,
       user_id   		   BIGINT(10)NOT NULL,
       interaction_history_comment TEXT NOT NULL,
       interaction_history_date	   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(interaction_id)REFERENCES interactions(interaction_id)ON DELETE CASCADE,
       FOREIGN KEY(user_id)REFERENCES users(user_id)
)