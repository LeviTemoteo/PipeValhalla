from log.pipelog import logger
from pathlib import Path
from readers.CSVReader import CSVReader
from readers.JSONReader import JSONReader
from dao.match import MatchDAO
from dao.players import PlayerDAO
from datetime import datetime

class PipelineOrchestrator:

    def __init__(self, match_dao: MatchDAO, player_dao: PlayerDAO):
        self.match_dao = match_dao
        self.player_dao = player_dao

    def process_match(self, file_name: str) -> int:
        '''Faz a leitura do arquivo JSON, envia para o banco de dados e retorna o id da partida'''

        try:
            reader = JSONReader(file_name)
            raw_match_data = reader.read_match_data()

            completed_match_data = self._complete_match_data(raw_match_data, reader)

            match_id = self.match_dao.insert_match(completed_match_data)
            logger.info(f"Partida processada: {match_id}")
            return match_id
        
        except Exception as error:
            logger.error(f"Erro ao processar o arquivo '{file_name}': {error}")
            raise RuntimeError(f"Erro ao processar o arquivo {error}")

    def delete_match(self, match_id: int) -> bool:
        '''Envia o id da partida para deletar ela do banco'''

        try:
            return self.match_dao.delete_match(match_id)
        except Exception as error:
            logger.error(f"Ocorreu algum erro na chamada para deletar a partida {match_id}: {error}")
            raise RuntimeError(f"Ocorreu algum erro na chamada para deletar a partida {match_id}: {error}")

    def send_players(self, csv_path: str) -> bool:
        '''Envia o caminho do arquivo csv para atualizar os jogadores no banco de dados'''

        try:
            reader = CSVReader(csv_path)
            players_data = reader.read_players()

            success = self.player_dao.sync_players(players_data)

            if success:
                logger.info("Sincronização dos jogadores realizada.")
            else:
                logger.warning("Falha na sincronização dos jogadores.")

            return success
        
        except Exception as error:
            logger.error(f"Erro inesperado ao processo csv {csv_path}: {error}")
            raise RuntimeError(f"Erro inesperado ao processo csv {csv_path}: {error}")

    def _complete_match_data(self, raw_match_data: dict, reader: JSONReader) -> dict:
        '''Função para completar os dados do JSON, nesse caso, adicionar a data de modificação do arquivo'''

        json_path = reader.get_full_path()

        unix_timestamp = Path(json_path).stat().st_mtime
        file_date = datetime.fromtimestamp(unix_timestamp).strftime("%Y-%m-%d")

        raw_match_data["mod_date"] = file_date

        return raw_match_data