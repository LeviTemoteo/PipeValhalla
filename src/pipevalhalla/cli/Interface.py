import argparse
from pipevalhalla.auth.authenticator import AuthService
from pipevalhalla.services.Orchestrator import PipelineOrchestrator

class CLIHandler:

    def __init__(self, auth_service: AuthService, pipeline: PipelineOrchestrator):
        self.auth_service = auth_service
        self.pipeline = pipeline
        self.parser = argparse.ArgumentParser(prog="pipevalhalla", description="CLI que possui comandos para gerenciar o banco de dados no supabase")
        self._setup_parsers()

    def run(self, args: list = None) -> None:
        '''Função orquestradora que envia o comando do usuário para o parser e chama a função correspondente'''
        
        # Faz a análise dos comandos e devolve a função correspondente configurada no setup_parsers.
        args = self.parser.parse_args()
        args.func(args)

    def handle_login(self, args: argparse.Namespace) -> None:
        '''Trata o comando de login, recebe email e senha'''
        print("Autenticando...")

        try:
            email = args.email
            senha = args.senha

            user = self.auth_service.login(email=email, password=senha)

            if user:
                print("Login realizado.")
            else:
                print("Falha no login, verifique suas credenciais")
        except Exception as error:
            print(f"Ocorreu um erro ao tentar o login: {error}")

    def handle_logout(self, args: argparse.Namespace) -> None:
        '''Trata o comando de logout'''

        print("Realizando logout...")

        try:
            user = self.auth_service.logout()

            if user:
                print("Logout realizado.")
            else:
                print("Falha no logout, não foi encontrado uma sessão local.")

        except Exception as error:
            print(f"Ocorreu um erro ao tentar o logout: {error}")

    def handle_add_match(self, args: argparse.Namespace) -> None:
        '''Trata o comando de adicionar partida'''

        print("Enviando partida...")

        try:
            file_name = args.nome_arquivo
            request = self.pipeline.process_match(file_name)

            if request:
                print(f"Partida enviada, id: {request}")
            else:
                print(f"Não foi possível enviar a partida.")

        except Exception as error:
            print(f"Ocorreu um erro ao enviar a partida: {error}")

    def handle_delete_match(self, args: argparse.Namespace) -> None:
        '''Trata o comando de deletar partida'''

        print("Deletando partida...")

        try:
            match_id = args.match_id
            request = self.pipeline.delete_match(match_id)

            if request:
                print("Partida deletada com sucesso.")
            else:
                print("Não foi possível deletar a partida, verifique suas permissões.")

        except Exception as error:
            print(f"Ocorreu um erro ao deletar a partida: {error}")

    def handle_import_players(self, args: argparse.Namespace) -> None:
        '''Trata o comando de envio dos jogadores'''

        print("Sincronizando jogadores...")

        try:
            csv_path = args.caminho_csv
            request = self.pipeline.send_players(csv_path=csv_path)

            if request:
                print("Jogadores sincronizados com sucesso.")
            else:
                print(f"Não foi possível sincronizar os jogadores.")

        except Exception as error:
            print(f"Ocorreu um erro ao sincronizar os jogadores: {error}")

    def _setup_parsers(self) -> None:
        '''Gerencia os comandos do comando pipevalhalla'''

        subparsers = self.parser.add_subparsers(dest="subcommand", required=True, help="Subcomandos disponíveis")

        # parser do login
        parser_login = subparsers.add_parser("login", help="Realiza o login do usuário")
        parser_login.add_argument("email", type=str, help="E-mail usado no supabase")
        parser_login.add_argument("senha", type=str, help="Senha usada no supabase")
        parser_login.set_defaults(func=self.handle_login)

        # parser de logout
        parser_logout = subparsers.add_parser("logout", help="Encerra sua sessão, sendo necessário fazer login novamente")
        parser_logout.set_defaults(func=self.handle_logout)

        # parser de envio de partida
        parser_add = subparsers.add_parser("add", help="Envia o arquivo os dados da partida para o supabase")
        parser_add.add_argument("nome_arquivo", type=str, help="Nome exato do arquivo que deseja enviar, não é necessário o caminho absoluto")
        parser_add.set_defaults(func=self.handle_add_match)

        # parser de deletar partida
        parser_del = subparsers.add_parser("del", help="Deleta uma partida do supabase")
        parser_del.add_argument("match_id", type=int, help="ID da partida que deseja deletar, cheque o supabase e veja a coluna 'match_id'")
        parser_del.set_defaults(func=self.handle_delete_match)

        #parser de enviar jogadores
        parser_sendplayers = subparsers.add_parser("sendplayers", help="Atualiza os dados dos jogadores do panteão no supabase")
        parser_sendplayers.add_argument("caminho_csv", type=str, help="Caminho absoluto do arquivo csv, partida do C: ou / (linux)")
        parser_sendplayers.set_defaults(func=self.handle_import_players)
