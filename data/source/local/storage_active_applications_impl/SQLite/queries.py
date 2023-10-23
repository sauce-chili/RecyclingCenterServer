from data.source.local.table_names import _APPLICATION_TABLE_NAME

query_create_application_table_if_not_exist = f"""
    CREATE TABLE IF NOT EXISTS {_APPLICATION_TABLE_NAME} (
	"weighing_order"	INTEGER,
	"source"	VARCHAR(50),
	"destination"	VARCHAR(50),
	"type_operation"	VARCHAR(20),
	"camera_type"	VARCHAR(50),
	"scales_type"	VARCHAR(50),
	"weight"	REAL,
	"url_photo"	TEXT,
	"date"	TEXT
)
"""

query_add_application_with_inc_weighing_order = f"""
INSERT INTO {_APPLICATION_TABLE_NAME} (
                weighing_order, source, destination, type_operation, camera_type, scales_type, weight, url_photo, date
)
VALUES (
    (SELECT COALESCE(MAX(weighing_order), 0) + 1 FROM {_APPLICATION_TABLE_NAME}), 
    ?, 
    ?, 
    ?, 
    ?, 
    ?, 
    ?, 
    ?, 
    ?
)   
"""

query_delete_all_applications = f"""DELETE FROM active_application"""

query_get_all_application = f"""
    SELECT * FROM {_APPLICATION_TABLE_NAME}
"""

query_count_applications = f"""
    SELECT COUNT(*) FROM active_application
"""
