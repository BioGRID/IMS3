CREATE TABLE IF NOT EXISTS ptm_notes(
       ptm_note_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       ptm_note_text	  TEXT NOT NULL,
       user_id		  BIGINT(10)NOT NULL,
       ptm_note_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       ptm_note_status	  ENUM('active','inactive')NOT NULL DEFAULT 'active',
       ptm_id		  BIGINT(10)NOT NULL,
       FOREIGN KEY(user_id)REFERENCES users(user_id),
       FOREIGN KEY(ptm_id)REFERENCES ptms(ptm_id)
)