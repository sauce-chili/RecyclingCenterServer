from data.source.local.table_names import _WAYBILL_TABLE_NAME, _APPLICATION_TABLE_NAME

query_create_table_waybill_if_not_exist = f"""
CREATE TABLE IF NOT EXISTS {_WAYBILL_TABLE_NAME} (
    "id" INTEGER,
	"weighing_order"	INTEGER,
	"source"	VARCHAR(50),
	"destination"	VARCHAR(50),
	"type_operation"	VARCHAR(20),
	"camera_type"	VARCHAR(50),
	"scales_type"	VARCHAR(50),
	"weight"	REAL,
	"url_photo"	TEXT,
	"date"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
"""

query_insert_all_records_from_active_application_table = f"""
    INSERT INTO {_WAYBILL_TABLE_NAME} ("weighing_order", "source", "destination", "type_operation", "camera_type", "scales_type", "weight", "url_photo", "date")
    SELECT "weighing_order", "source", "destination", "type_operation", "camera_type", "scales_type", "weight", "url_photo", "date"
    FROM {_APPLICATION_TABLE_NAME};
"""

query_get_all = f"""
    SELECT * FROM {_WAYBILL_TABLE_NAME}
"""

