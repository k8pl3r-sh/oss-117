from abc import ABCMeta, abstractmethod


class AbstractParser(object, metaclass=ABCMeta):
    @abstractmethod
    def file_parser(self, file_path: str) -> list[dict]:
        pass

    @abstractmethod
    def get_index_pattern(self, idx_name: str) -> dict:
        pass