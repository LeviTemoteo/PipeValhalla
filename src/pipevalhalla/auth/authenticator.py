import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from supabase import Client
from pipevalhalla.database.connection import DatabaseConnection
from pipevalhalla.log.pipelog import logger

class AuthService:
    '''Classe gerenciadora de autenticação, realiza validação do cadastro e sessão local'''

    def __init__(self, db_connection: DatabaseConnection, session_path: str = "~/.pipevalhalla/.session"):
        self.db_connection = db_connection
        self.client = self.db_connection.client
        self.session_path = Path(session_path).expanduser()
        self.current_user: Optional[Dict[str, Any]] = None

        self._load_session() # Tenta buscar uma sessão recente

    def login(self, email: str, password: str) -> bool:
        '''Autentica o usuário no Supabase e salva sua sessão na memória
        Retorna booleano para indicar confirmação ou rejeição de cadastro,
        não necessariamente significa que ocorreu uma falha de sistema, por isso o retorno é apenas booleano.
        '''

        try:
            response = self.client.auth.sign_in_with_password(
                {"email":email, "password": password}
                )
            if not response.session or not response.user:
                logger.warning(f"Tentativa de sessão invalidada: {email}")
                return False

            user_data = {
                "acess_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "user_id": response.user.id,
                "email": response.user.email
            }
            self.current_user = user_data
            self.db_connection.set_session_token(response.session.access_token) # Envio do acesso para o banco de dados

            self._save_session(user_data)    
            logger.info(f"{email} autenticado com sucesso.")
        
            return True
        
        except Exception as error:
            logger.error(f"Tentativa de sessão invalidada: {error}", exc_info=True)
            return False

    def logout(self) -> bool:
        '''Encerra a sessão do usuário no Supabase e localmente'''

        supase_logout = True

        try:
            self.client.auth.sign_out()

        except Exception as error:
            logger.warning(f"Ocorreu um erro ao deslogar no Supabase: {error}")
            supase_logout = False

        self.current_user = None
        self._clear_session()

        if supase_logout:
            logger.info("Logout no supabase realizado com sucesso.")
        else:
            logger.warning("Logout realizado apenas localmente. Houve falha ao deslogar no Supabase")

        return supase_logout

    def is_authenticated(self) -> bool:
        '''
        Verifica se o usuário está autenticado no Supabase
        Em caso de erro, tentar autenticar o usuário caso seja possível com o refresh token
        '''

        user_data = self.get_current_user()

        if not user_data or "acess_token" not in user_data:
            return False

        try:
            supabase_response = self.client.auth.get_user(user_data["acess_token"])

            if supabase_response and supabase_response.user:
                return True

        except Exception as error:
            logger.warning(f"Session expirada ou invalidada no Supabase: {error}")

            refresh_token = user_data.get("refresh_token")

            if refresh_token:
                try:
                    refresh = self.client.auth.refresh_session(refresh_token)

                    if refresh and refresh.user and refresh.session:
                        new_session = {
                            "acess_token": refresh.session.access_token,
                            "refresh_token": refresh.session.refresh_token,
                            "user_id": refresh.user.id,
                            "email":refresh.user.email
                        }

                        self._save_session(new_session)
                        self.current_user = new_session

                        self.db_connection.set_session_token(refresh.session.access_token)

                        logger.info("Session renovada com o refresh token")
                        return True
                    
                except Exception as error:
                    logger.error(f"Session não renovada: {error}")

            self.current_user = None
            self._clear_session()
            
        return False

    def get_current_user(self) -> Dict[str, Any] | None:
        '''
        Retorna os dados do usuário em formato de dicionário.
        Verifica  se está na memória, se não, verifica no disco.
        '''

        if self.current_user is not None:
            return self.current_user

        user_data = self._load_session()

        if user_data:
            self.current_user = user_data
            return self.current_user

        return None

    def _save_session(self, user_data: Dict[str, Any]) -> None:

        try:
            self.session_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.session_path, "w", encoding="utf-8") as file:
                json.dump(user_data, file, indent=4)
            logger.debug("Sessão salva")

        except Exception as error:
            logger.error(f"Falha ao salvar a sessão: {error}", exc_info=True)
    
    def _load_session(self) -> Dict[str, Any] | None:
        '''Retorna o arquivo .session como dicionário'''

        if not self.session_path.exists():
            logger.debug("Arquivo session não encontrado")
            return None

        try:
            with open(self.session_path, "r", encoding="utf-8") as session_file:
                user_data = json.load(session_file)

            if not isinstance(user_data, dict) or "acess_token" not in user_data:
                logger.warning("Arquivo session incompleto. Realizado limpeza do arquivo")
                self._clear_session()
                return None

            logger.debug("Sessão carregada.")
            return user_data

        except Exception as error:
            logger.error(f"Erro ao ler o arquivo session: {error}. Realizado limpeza do arquivo")
            self._clear_session()
            return None  

    def _clear_session(self) -> None:
        '''Apaga o arquivo .session'''

        try:
            self.session_path.unlink(missing_ok=True)
            logger.debug("Arquivo session removido.")
        except Exception as error:
            logger.error(f"Ocorreu um erro ao remover o arquivo session: {error}")
    