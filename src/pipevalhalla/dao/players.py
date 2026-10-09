from pipevalhalla.database.connection import DatabaseConnection
from pipevalhalla.log.pipelog import logger

class PlayerDAO:
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def sync_players(self, players_data: list[dict]) -> bool:
        '''Sincroniza os jogadores no banco de dados a partir do arquivo csv lido pelo CSVReader'''
        
        client = self.db_connection.connect()
        db_players = self.get_all_players()
        
        db_players_dict_tuple = {player["brawlhalla_id"]: self._format_player_row(player) for player in db_players}
        db_ids = set(db_players_dict_tuple.keys())

        csv_ids = {player["brawlhalla_id"] for player in players_data}

    # UPSERT no banco de dados
        players_to_upsert = []

        for player_dict in players_data:
            player_id = player_dict["brawlhalla_id"]
            formatted_csv_dict_tuple = self._format_player_row(player_dict)

            if (player_id not in db_ids) or (db_players_dict_tuple[player_id] != formatted_csv_dict_tuple):
                players_to_upsert.append(player_dict)

        try:
            if players_to_upsert:
                logger.info(f"Sincronizando {len(players_to_upsert)} jogador(es)...")
                client.table("Jogadores").upsert(players_to_upsert, on_conflict="brawlhalla_id").execute()
        except Exception as error:
            logger.error(f"Erro ao fazer upsert nos jogadores: {error}")
            return False

    # DELETE jogadores não presentes no csv
        players_to_delete = list(db_ids - csv_ids)

        try:
            if players_to_delete:
                logger.info(f"Removendo {len(players_to_delete)} ausentes no CSV...")
                client.table("Jogadores").delete().in_("brawlhalla_id", players_to_delete).execute()
        except Exception as error:
            logger.error(f"Erro ao deletar os jogadores: {error}")
            return False
        
        return True

    def get_player_by_id(self, brawlhalla_id: int) -> list[dict] | None:
        '''Devolve um jogador pelo seu id do brawlhalla'''
        try:
            client = self.db_connection.connect()
            response = client.table("Jogadores").select("*").eq("brawlhalla_id", brawlhalla_id).execute()
            return response.data[0] if response.data else None
        
        except Exception as error:
            logger.error(f"Erro ao retornar o jogador {brawlhalla_id}: {error}")
            raise RuntimeError(f"Erro ao retornar o jogador {brawlhalla_id}: {error}")

    def get_all_players(self) -> dict:
        '''Pega todos os jogadores cadastrados na tabela "Jogadores" no Supabase'''
        
        try:
            client = self.db_connection.connect()
            response = client.table("Jogadores").select("*").execute()
            logger.info("Tabela de jogadores retornado.")
            return response.data
        
        except Exception as error:
            logger.error(f"Falha ao retornar tabela de jogadores: {error}")
            raise InterruptedError(f"Falha ao retornar tabela de jogadores: {error}")

    def _format_player_row(self, row: dict) -> tuple:
        '''Recebe um jogador e devolve como tupla padronizada
        (id, clan, name, cost)
        '''

        return (
            int(row["brawlhalla_id"]),
            int(row["clan"]) if row.get("clan") is not None else "N/A",
            str(row.get("name", "")).strip(),
            int(row.get("cost", 0))
        )
    