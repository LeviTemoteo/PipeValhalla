from database.connection import DatabaseConnection
from log.pipelog import logger
from typing import Dict, Any

class MatchDAO:

    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def insert_match(self, match_data: dict) -> int: # o int é o id da partida
        '''Insere os dados completo de uma partida no Supabase'''
        
        teams = match_data["Teams"]
        score = True if match_data["GameMode"] == "Score" else False
        
        match_id = self._insert_match_header(match_data)

        try:
            self._insert_match_players(match_id, match_data, teams, score)
            self._insert_loadouts(match_id, match_data)
            self._insert_weapons(match_id, match_data)
            self._insert_attacks(match_id, match_data, teams)

        except Exception as error:
            logger.error(
            f"Erro durante o processamento dos jogadores para a partida {match_id}. "
            f"realizando rollback..."
        )
            if not self.delete_match(match_id):
                logger.critical(f"Falha no rollback! match_id: {match_id}")
            
            raise RuntimeError(f"Falha na inserção da partida. {error}")

        return match_id
            
    def delete_match(self, match_id: int) -> bool:
        '''Deleta uma partida em cascata'''

        try:
            client = self.db_connection.connect()
            response = client.table("Partidas").delete().eq("id_match", match_id).execute()
            if response.data:
                logger.info(f"Partida {match_id} deletada com sucesso.")
                return True
            
            logger.warning(f"Não foi encontrado a partida {match_id}")
            return False

        except Exception as error:
            logger.error(f"Falha ao deletar {match_id}: {error}")
            raise RuntimeError(f"Falha ao deletar {match_id}: {error}")

    def get_match_by_id(self, match_id: int) -> Dict[str, Any] | None:
        client = self.db_connection.connect()

        try:
            response = client.table("Partidas").select("*").eq("id_match", match_id).execute()
            if response.data:
                logger.info(f"Partida {match_id} retornada com sucesso")
                return response.data[0]

            logger.warning(f"Não foi encontrado a partida {match_id}")
            return None
        except Exception as error:
            logger.error(f"Falha ao retornar a partida {match_id}")
            raise RuntimeError(f"Falha ao retornar a partida {match_id}")

    def _insert_match_header(self, data: dict) -> int: # retorna o id da partida
        '''Insere os dados na tabela "Partidas" no Supabase'''
        
        match_header = {
            "build_version": data.get("BuildVersion", None),
            "date": data.get("mod_date", None),
            "map_name": data.get("MapName", None),
            "gamemode": data.get("GameMode", None),
            "teams": data.get("Teams", False),
            "team_damage": data.get("TeamDamage", None),
            "lives": data.get("Lives", 3),
            "game_duration": data.get("GameDuration", 480000),
            "score_to_win": data.get("ScoreToWin", None)
            }

        client = self.db_connection.connect()

        try:
            response = client.table("Partidas").insert(match_header).execute()
        except Exception as error:
            logger.error(f"Erro ao transferir header da partida: {error}")
            raise RuntimeError(f"Erro ao transferir header da partida: {error}")
        
        return int(response.data[0]["id_match"])

    def _insert_match_players(self, match_id: int, match_data: dict, teams=False, score=False) -> None:
        '''Insere todos os jogadores presentes em uma partida no Supabase'''

        client = self.db_connection.connect()
        players_to_insert = []
        players_to_insert_id = []
        i = 1

        while True:
            player_key = f"Player{i}"
            i += 1
            player_key_info = match_data.get(player_key, False)
            if player_key_info:
                players_to_insert.append(player_key)
                players_to_insert_id.append(player_key_info["BrawlhallaID"])
            else:
                break

        # Recebe as informações dos jogadores da tabela "Jogadores"
        try:
            response = client.table("Jogadores").select("brawlhalla_id, clan, cost").in_("brawlhalla_id", players_to_insert_id).execute()
            players_db_info = {player["brawlhalla_id"]: player for player in response.data}
        except Exception as error:
            logger.error(f"Erro ao carregar informações da tabela 'Jogadores': {error}")
            raise RuntimeError(f"Erro ao carregar informações da tabela 'Jogadores': {error}")

        players_to_insert_data = []
        for player_key in players_to_insert:
            player_data = match_data.get(player_key)
            bh_id = player_data.get("BrawlhallaID", None)

            try:
                player_info = players_db_info[bh_id]
                current_clan = player_info["clan"]
                current_cost = player_info["cost"]
            except Exception as error:
                error_msg = (
            f"BrawlhallaID: {bh_id} não encontrado na tabela 'Jogadores' "
            f"A tabela de jogadores precisa ser atualizada antes de inserir a partida {match_id}."
                )
                logger.error(error_msg)
                raise RuntimeError(error_msg)

            
            players_to_insert_data.append(
                {
                    "id_match": match_id,
                    "brawlhalla_id": bh_id,
                    "current_clan": current_clan,
                    "current_player_name": player_data.get("PlayerName", None),
                    "current_cost": current_cost,
                    "damage_dealt": player_data.get("DamageDealt", 0),
                    "damage_taken": player_data.get("DamageTaken", 0),
                    "deaths": player_data.get("Deaths", 0),
                    "kos": player_data.get("KOs", 0),
                    "suicides": player_data.get("Suicides", 0),
                    "clashes": player_data.get("Clashes", 0),
                    "total_dodges": player_data.get("TotalDodges", 0),
                    "air_dodges": player_data.get("AirDodges", 0),
                    "dashes": player_data.get("Dashes", 0),
                    "air_jumps": player_data.get("AirJumps", 0),
                    "dash_jumps": player_data.get("DashJumps", 0),
                    "total_jumps": player_data.get("TotalJumps", 0),
                    "time_in_air": player_data.get("TimeInAir", 0),
                    "time_on_ground": player_data.get("TimeOnGround", 0),
                    "time_on_wall": player_data.get("TimeOnWall", 0),
                    "team_num": player_data.get("TeamNum", None) if teams else None,
                    "team_damage_dealt": player_data.get("TeamDamageDealt", 0) if teams else None,
                    "team_damage_taken": player_data.get("TeamDamageTaken", 0) if teams else None,
                    "team_kos": player_data.get("TeamKOs", 0) if teams else None,
                    "score": player_data.get("Score", 0) if score else None
                }
            )
        if players_to_insert_data:
            # Envia jogadores
            try:
                response = client.table("Jogadores_Partidas").insert(players_to_insert_data).execute()
                logger.info(f"{len(players_to_insert_data)} jogadores inseridos para {match_id}")

            except Exception as error:
                logger.error(f"Falha ao enviar jogadores da partida {match_id}: {error}")
                raise RuntimeError(f"Falha ao enviar jogadores da partida {match_id}: {error}")
            
    def _insert_loadouts(self, match_id: int, match_data: dict) -> None:
        '''Insere o loadout (cosméticos) de cada jogador no Supabase'''

        client = self.db_connection.connect()
        players_to_insert_loadout = []
        i = 1

        while True:
            player_key = f"Player{i}"
            player_data = match_data.get(player_key)

            if not player_data:
                break

            bh_id = player_data.get("BrawlhallaID")
            player_loadout_data = player_data.get("Loadout", {})

            players_to_insert_loadout.append(
                {
                    "id_match": match_id,
                    "brawlhalla_id": bh_id,
                    "legend_name": player_loadout_data.get("LegendName", None),
                    "skin_name": player_loadout_data.get("SkinName", None),
                    "color_scheme_name": player_loadout_data.get("ColorSchemeName", "Classic Colors"),
                    "stance": player_loadout_data.get("Stance", "Base"),
                    "random": player_loadout_data.get("Random", False)
                }
            )

            i += 1

        if players_to_insert_loadout:
            # Envia loadout dos jogadores

            try:
                response = client.table("Loadout").insert(players_to_insert_loadout).execute()
                logger.info(f"{len(players_to_insert_loadout)} loadouts inseridos para {match_id}")

            except Exception as error:
                logger.error(f"Erro no carregamento dos loadouts partida {match_id}: {error}")
                raise RuntimeError(f"Erro no carregamento dos loadouts: {error}")       

    def _insert_weapons(self, match_id: int, match_data: dict) -> None:
        '''Insere as armas usadas de cada jogador'''
        
        client = self.db_connection.connect()
        weapons_to_insert = []
        weapons = {"Orb", "Boots", "Unarmed", "Hammer", "Scythe", "Spear", "Sword", 
                   "Cannon", "RocketLance", "Katar", "Fists", "Axe", "Bow", "Greatsword", 
                   "Chakram", "Pistol"}

        i = 1
        while True:
            player_key = f"Player{i}"
            player_data = match_data.get(player_key)
            

            if not player_data:
                break

            bh_id = player_data.get("BrawlhallaID")
            i += 1
            for weapon in weapons:
                weapon_data = player_data.get(weapon)
                if not weapon_data:
                    continue

                weapons_to_insert.append(
                    {
                        "id_match": match_id,
                        "brawlhalla_id": bh_id,
                        "weapon": weapon,
                        "time_held": weapon_data.get("TimeHeld", 0),
                        "damage_taken": weapon_data.get("DamageTaken", 0)
                    }
                )

        if weapons_to_insert:
            try:
                response = client.table("Armas").insert(weapons_to_insert).execute()
                logger.info(f"Armas da partida {match_id} enviadas.")
            except Exception as error:
                logger.error(f"Não foi possível enviar as armas da partida {match_id}: {error}")
                raise RuntimeError(f"Não foi possível enviar as armas da partida {match_id}: {error}")

    def _insert_attacks(self, match_id: int, match_data: dict, teams=False) -> None:
        '''Insere o ataque de cada arma de cada jogador na tabela "Ataques" '''

        client = self.db_connection.connect()

        attacks_to_insert = []
        attacks = ["nLight", "dLight", "sLight", "nHeavy", "dHeavy", "sHeavy", 
                   "nAir","sAir", "dAir", "Recovery", "GroundPound", "Throw"]
        
        weapons = ["Orb", "Boots", "Unarmed", "Hammer", "Scythe", "Spear", "Sword", 
                    "Cannon", "RocketLance", "Katar", "Fists", "Axe", "Bow", "Greatsword", 
                    "Chakram", "Pistol"]

        i = 1
        while True:
            player_key = f"Player{i}"
            player_data = match_data.get(player_key)

            if not player_data:
                break

            bh_id = player_data.get("BrawlhallaID")
            i += 1

            for weapon in weapons:
                weapon_data = player_data.get(weapon)
                
                if not weapon_data:
                    continue
                
                for attack in attacks:
                    attack_data = weapon_data.get(attack)

                    if not attack_data:
                        continue

                    attacks_to_insert.append(
                        {
                            "id_match": match_id,
                            "brawlhalla_id": bh_id,
                            "weapon": weapon,
                            "attack": attack,
                            "uses": attack_data.get("Uses", 0),
                            "enemy_hits": attack_data.get("EnemyHits", 0),
                            "enemy_damage": attack_data.get("EnemyDamage", 0),
                            "team_hits": attack_data.get("TeamHits", 0) if teams else None,
                            "team_damage": attack_data.get("TeamDamage", 0) if teams else None,
                            "enemy_kos": attack_data.get("EnemyKOs", 0),
                            "gc_uses": attack_data.get("GCUses", 0),
                            "gc_enemy_hits": attack_data.get("GCEnemyHits", 0),
                            "gc_enemy_damage": attack_data.get("GCEnemyDamage", 0),
                            "gc_enemy_kos": attack_data.get("GCEnemyKOs", 0),
                            "gc_team_hits": attack_data.get("GCTeamHits", 0) if teams else None,
                            "gc_team_damage": attack_data.get("GCTeamDamage", 0) if teams else None
                        }
                    )

        if attacks_to_insert:
            
            # Envio dos ataques, como são muitas linhas, é feito um envio em lotes.
            batch_size = 150
            total_records = len(attacks_to_insert)

            try:
                for j in range(0, total_records, batch_size):
                    batch = attacks_to_insert[j : j + batch_size]
                    
                    client.table("Ataques").insert(batch).execute()

                logger.info(f"{total_records} ataques inseridos com sucesso na partida {match_id} (divididos em lotes).")

            except Exception as error:
                logger.error(f"Falha ao enviar lote de ataques da partida {match_id}: {error}")
                raise RuntimeError(f"Falha ao enviar os ataques da partida {match_id}: {error}")