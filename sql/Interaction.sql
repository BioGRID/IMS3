CREATE TABLE IF NOT EXISTS interaction_types(
       interaction_type_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       interaction_type_name	  VARCHAR(255)NOT NULL UNIQUE,
       interaction_type_desc	  TEXT NULL,
       interaction_type_dateadded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       interaction_type_status	  ENUM('active','inactive')NOT NULL DEFAULT 'active'
);

INSERT INTO interaction_types(interaction_type_name)VALUES('Protien-Protein');

CREATE TABLE IF NOT EXISTS interactions(
       interaction_id        BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_hash      VARCHAR(64)NULL,
       publication_id        BIGINT(10)NOT NULL,
       interaction_type_id   BIGINT(10)NULL, -- for now
       interaction_status    ENUM('normal','error','temporary','external')NOT NULL DEFAULT 'normal',
       interaction_source_id BIGINT(10)NOT NULL,
       FOREIGN KEY(publication_id)REFERENCES publications(publication_id),
       FOREIGN KEY(interaction_type_id)REFERENCES interaction_types(interaction_type_id)
)