import os
from dotenv import load_dotenv
from supabase import Client, create_client
from src.log.pipelog import logger

load_dotenv()

class DatabaseConnection:
    '''Classe que cuida da conexão com o banco de dados pelo Supabase.'''

    def __init__(self, supabase_url: str = None, supabase_key: str = None):
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_KEY")

        if not self.supabase_url or not self.supabase_key:
            error_message = "Supabase key e url não estão configuradas"
            logger.error(error_message)
            raise ValueError(error_message)

        self.client: Client = None
        self.connect()

    def connect(self) -> Client:
        "Conecta com o Supabase e devolve o client"

        try:
            if not self.client:
                self.client = create_client(supabase_url=self.supabase_url, supabase_key=self.supabase_key)
                logger.info("Conexão realizada com o Supabase")
        except Exception as error:
            logger.error(f"Erro ao conectar com o supabase: {error}", exc_info=True)
            raise RuntimeError("Erro ao conectar com o Supabase, verifique sua conexão.")

    def set_session_token(self, acess_token: str) -> None:
        '''
        Injetor de token JWT, serve para realizar autenticação nas requisições do Supabase.
        '''

        if acess_token and self.client:
            try:
                self.client.postgrest.auth(acess_token)
                logger.info("Enviado token de acesso ao Supabase.")
            except Exception as error:
                logger.error(f"Falha ao enviar o token: {error}", exc_info=True)
                raise RuntimeError("Error ao enviar as credenciais ao banco.")