from pathlib import Path
from log.pipelog import logger
import json

class JSONReader:

    def __init__(self, file_name: str, dir_path: str = "~/BrawlhallaStatDumps"):
        self.file_name = Path(file_name)
        self.dir_path = Path(dir_path).expanduser()

    def read_match_data(self) -> dict:
        json_path = self._get_full_path()

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    def _get_full_path(self) -> str:
        '''Verifica se o arquivo existe e retorna o caminho completo do arquivo'''

        full_path = self.dir_path / self.file_name

        if full_path.exists():
            logger.info(f"Arquivo encontrado: {self.file_name}.")
            return str(full_path)

        logger.error(f"Arquivo não encontrado. {self.dir_path}")
        raise FileNotFoundError(f"O arquivo: '{full_path}' não foi encontrado")


