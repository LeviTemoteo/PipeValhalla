from pathlib import Path
from pipevalhalla.log.pipelog import logger
import csv

class CSVReader:

    def __init__(self, csv_path: str):
        self.csv_path = Path(csv_path)

    def read_players(self) -> list[dict]:
        '''Lê um arquivo csv e transforma em uma lista de dicionários (players nesse caso)'''

        if not self.csv_path.exists():
            logger.error(f"Arquivo csv não encontrado: {self.csv_path}")
            raise FileNotFoundError(f"Arquivo csv não encontrado: {self.csv_path}")

        players = []

        with open(self.csv_path, "r", encoding="utf-8") as csv_file:
            file = csv.DictReader(csv_file, delimiter=";")

            for row in file:
                player = self._transform_row(row)
                players.append(player)

        logger.info(f"Jogadores lidos: {len(players)}.")
        return players

    def _transform_row(self, row: dict) -> dict:
        "Converte os dados do dicionário para seus respectivos tipos"

        try:
            return {
                "brawlhalla_id": int(row["brawlhalla_id"].strip()),
                "clan": int(row["clan"].strip()),
                "name": str(row["name"].strip()),
                "cost": int(row["cost"].strip())
            }
        except Exception as error:
            logger.error(f"Ocorreu um erro ao transformar a linha {row}: {error}")
            raise ValueError(f"Ocorreu um erro com o jogador {row}: {error}")
        