CREATE TABLE IF NOT EXISTS iplex_columns(
       iplex_column_id		    BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       iplex_column_title	    VARCHAR(255)NOT NULL UNIQUE,
       participant_tag_type_id	    BIGINT(10)NOT NULL,
       participant_tag_mapping_rank BIGINT(10)NULL,
       iplex_column_rank	    BIGINT(10)NULL,
       iplex_column_addeddate	    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       iplex_column_status	    ENUM('active','inactive')NOT NULL DEFAULT 'active',
       iplex_project_id		    BIGINT(10)
       ,FOREIGN KEY(participant_tag_type_id)REFERENCES participant_tag_types(participant_tag_type_id)
       ,FOREIGN KEY(iplex_project_id)REFERENCES iplex_projects(iplex_project_id)
);

CREATE TABLE IF NOT EXISTS participant_tags(
       participant_tag_id          BIGINT(10)PRIMARY KEY AUTO_INCREMENT,
       participant_tag_shortcode   VARCHAR(255)NOT NULL UNIQUE,
       participant_tag_name        VARCHAR(255)NULL,
       participant_tag_description TEXT,
       participant_tag_type_id     BIGINT(10),
       participant_tag_parent_id   BIGINT(10),
       participant_tag_addeddate   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       participant_tag_status      ENUM('active','inactive')NOT NULL DEFAULT 'active'
       ,FOREIGN KEY(participant_tag_type_id)REFERENCES participant_tag_types(participant_tag_type_id)
       -- ,FOREIGN KEY(participant_tag_parent_id)REFERENCES participant_tags(participant_tag_id)
);
