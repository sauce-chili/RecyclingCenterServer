from yaml import YAMLError


class YamlKeyNotFound(YAMLError):
    def __init__(self, yaml_file: str | None, missed_key: str | None, msg: str | None = None):
        super()
        self.__file = yaml_file
        self.__key = missed_key
        self.msg = msg

    def __str__(self):
        return f"Invalid config file {self.__file}.A required key {self.__key} is missing."
