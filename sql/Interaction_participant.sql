CREATE TABLE IF NOT EXISTS interaction_participants(
       interaction_participant_id	 BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_id			 BIGINT(10)NOT NULL,
       participant_id			 BIGINT(10)NOT NULL,
       participant_role_id		 BIGINT(10)NOT NULL,
       interaction_participant_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_participant_status	 ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(interaction_id)REFERENCES interactions(interaction_id)ON DELETE CASCADE
       ,FOREIGN KEY(participant_id)REFERENCES participants(participant_id)
       ,FOREIGN KEY(participant_role_id)REFERENCES participant_roles(participant_role_id)
);

CREATE TABLE IF NOT EXISTS interaction_participant_notes(
       interaction_participant_note_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_participant_id	      BIGINT(10)NOT NULL,
       interaction_participant_note_text      TEXT NOT NULL,
       user_id                                BIGINT(10)NOT NULL,
       interaction_participant_note_addeddate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_participant_notes_status   ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(interaction_participant_id)REFERENCES interaction_participants(interaction_participant_id)
       ,FOREIGN KEY(user_id)REFERENCES users(user_id)
);
