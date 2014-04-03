CREATE TABLE IF NOT EXISTS ptm_history(
       ptm_history_id      BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       modification_type   ENUM('ACTIVITATED','DISABLED','DEACTIVAVTED','UPDATED')NOT NULL,
       ptm_id		   BIGINT(10)NOT NULL,
       user_id		   BIGINT(10)NOT NULL,
       ptm_history_comment TEXT NULL,
       ptm_history_date	   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY(ptm_id)REFERENCES ptms(ptm_id),
       FOREIGN KEY(user_id)REFERENCES users(user_id)
)