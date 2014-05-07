CREATE TABLE IF NOT EXISTS interaction_notes(
       interaction_note_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_note_text	  TEXT NOT NULL,
       user_id			  BIGINT(10)NOT NULL,
       interaction_note_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_note_status    ENUM('active','inactive'),
       interaction_id		  BIGINT(10)NOT NULL,
       FOREIGN KEY(user_id)REFERENCES users(user_id),
       FOREIGN KEY(interaction_id)REFERENCES interactions(interaction_id)ON DELETE CASCADE
)