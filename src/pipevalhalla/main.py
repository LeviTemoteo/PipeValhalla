import sys
import os
from dotenv import load_dotenv
from supabase import create_client, Client

from pipevalhalla.auth.authenticator import AuthService
from pipevalhalla.services.Orchestrator import PipelineOrchestrator
from pipevalhalla.cli.Interface import CLIHandler
from pipevalhalla.dao.match import MatchDAO
from pipevalhalla.dao.players import PlayerDAO

def main() -> None:
    load_dotenv()

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_key or not supabase_url:
        print("Arquivo ENV não foi configurado")
        sys.exit()

    try:
        supabase_client: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)

        match_dao = MatchDAO(supabase_client)
        player_dao = PlayerDAO(supabase_client)

        auth_service = AuthService(supabase_client)
        pipeline_orchestrator = PipelineOrchestrator(match_dao, player_dao)

        cli = CLIHandler(auth_service, pipeline_orchestrator)

        cli.run(sys.argv[1:])
    except Exception as error:

        print(f"Erro ao inicializar sistema: {error}")

if __name__ == "__main__":
    main()