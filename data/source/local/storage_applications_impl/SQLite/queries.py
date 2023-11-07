# from data.source.local.table_names import APPLICATION_TABLE_NAME

query_create_application_table_if_not_exist = """
    CREATE TABLE IF NOT EXISTS  {table_name} (
	"id"	INTEGER UNIQUE,
	"car_plate"	TEXT,
	"counterparty"	TEXT,
	"type_operation"	VARCHAR(20),
	"type_equipment"	TEXT,
	"camera_type"	VARCHAR(20),
	"scales_type"	VARCHAR(20),
	"weight_gross"	REAL,
	"weight_container"	REAL,
	"weight_extra"	REAL,
	"weight_net"	REAL,
	"url_photo"	TEXT,
	"date"	TEXT,
	"end_weighing"	INTEGER DEFAULT 0,
	PRIMARY KEY("id" AUTOINCREMENT)
)
"""

query_add_application = """
INSERT INTO {table_name} (
    "car_plate",
    "counterparty",
    "type_operation",
    "type_equipment",
    "camera_type",
    "scales_type",
    "weight_gross",
    "weight_container",
    "weight_extra",
    "weight_net",
    "url_photo",
    "date",
    "end_weighing"
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

query_delete_table = """DROP TABLE {table_name}"""

query_get_all_application = """
    SELECT * FROM {table_name} WHERE "end_weighing" <> 1
"""

query_count_applications = """
    SELECT COUNT(*) FROM {table_name} WHERE "end_weighing" <> 1
"""
