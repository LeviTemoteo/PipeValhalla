import sys
import os
from dotenv import load_dotenv
from supabase import create_client, Client

from pipevalhalla.auth.authenticator import AuthService
from pipevalhalla.services.Orchestrator import PipelineOrchestrator
from pipevalhalla.cli.Interface import CLIHandler
from pipevalhalla.dao.match import MatchDAO
from pipevalhalla.dao.players import PlayerDAO
from pipevalhalla.database.connection import DatabaseConnection

def main() -> None:
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_key or not supabase_url:
        print("Arquivo ENV não foi configurado")
        sys.exit()

    try:
        db_connection = DatabaseConnection(supabase_url=supabase_url, supabase_key=supabase_key)

        match_dao = MatchDAO(db_connection)
        player_dao = PlayerDAO(db_connection)

        auth_service = AuthService(db_connection)
        auth_service.is_authenticated()
        pipeline_orchestrator = PipelineOrchestrator(match_dao, player_dao)

        cli = CLIHandler(auth_service, pipeline_orchestrator)

        cli.run(sys.argv[1:])
    except Exception as error:

        print(f"Erro ao inicializar sistema: {error}")

if __name__ == "__main__":
    main()