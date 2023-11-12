import yaml
from pathlib import Path

from data.repository_impl.exceptions import YamlKeyNotFound
from domain.model.entities import DatabaseParam


def get_arguments_from_yaml(path_to_yaml_file: Path, key: str) -> list[dict]:
    if not path_to_yaml_file.exists():
        raise FileExistsError(f"Config file {path_to_yaml_file} isn't exist.")

    with open(path_to_yaml_file, encoding='utf-8', mode='r') as f:
        try:
            return yaml.load(f, Loader=yaml.Loader)[key]
        except KeyError:
            raise YamlKeyNotFound(yaml_file=str(path_to_yaml_file), missed_key=key)


def get_database_param(yaml_config_file: Path) -> DatabaseParam:
    root_key = "DB_PARAM"

    cfg = get_arguments_from_yaml(
        path_to_yaml_file=yaml_config_file,
        key=root_key
    )

    return DatabaseParam(
        db_path=Path(cfg["db_path"]),
        db_remote_path=Path(cfg["db_remote_path"]),
        image_buffer_folder_path=Path(cfg["image_buffer_folder_path"]),
        image_buffer_folder_remote_path=Path(cfg["image_buffer_folder_remote_path"])
    )
