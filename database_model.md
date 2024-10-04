AppTemplate:
- id: VARCHAR(36), primary key
- image_id: VARCHAR(36), foreign key (references id in glance Image)
- name: VARCHAR(255), not nullable, unique
- description: TEXT
- short_description: VARCHAR(255)
- instantiation_notice: TEXT
- creator_id: VARCHAR(36), not nullable, foreign key (references id in keystone User and id in User)
- created_at: DATETIME, not nullable
- updated_at: DATETIME, nullable
- deleted_at: DATETIME, nullable
- deleted: TINYINT(1), default 0
- version: VARCHAR(10), default '1.0'
- is_public: TINYINT(1), not nullable
- fixed_RAM_GB: DECIMAL(5,2)
- fixed_disk_GB: DECIMAL(5,2)
- fixed_cores: DECIMAL(3,2)
- per_user_RAM_GB: DECIMAL(5,2)
- per_user_disk_GB: DECIMAL(5,2)
- per_user_cores: DECIMAL(3,2)


User
- id: VARCHAR(36), primary key, foreign key (references id in keystone User)
- role_id: VARCHAR(36), foreign key (references id in Roles)

Roles
- id: VARCHAR(36), primary key
- name: VARCHAR(255), not nullable, unique