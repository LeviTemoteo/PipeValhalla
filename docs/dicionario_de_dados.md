<h3>Dicionário de Dados</h3>

Esse documento irá abrangir todos os diferentes dados de todas as tabelas do banco de dados.

Aqui você vai encontrar informações do dado, suas propriedades e significado.

Como há 6 tabelas diferentes relacionadas, esse documento será separado em tópicos, cada tópico sendo uma tabela:

- Partidas
- Jogadores_Partidas
- Jogadores
- Loadout
- Armas
- Ataques


# Tabela Partidas

A tabela `Partidas` é a tabela raiz do banco de dados, registrando informações gerais e configurações de sala.

## match_id

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | INT |
| Nullable | No |

Identificador único de cada partida registrada (Chave primária).
Para cada partida nova registrada, seu id é incrementado em 1.


## build_version

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(15) |
| Nullable | No |

Versão do jogo que a partida foi registrada.


## date

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | DATE |
| Nullable | No |

Data que foi registrada a partida.
É retirado a partir da data de criação do arquivo enviado pelo usuário, então se houver alterações do arquivo, pode comprometer a validade desse dado.


## map_name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(50) |
| Nullable | No |

Nome do mapa que a partida foi jogada.


## gamemode

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(30) |
| Nullable | No |

Modo de jogo que a partida foi jogada (por alguma razão, o writestats não permite o registro dos modos que possuem entidades diferentes de gadgets e de jogadores, como a bola do kung foot)

O banco de dados foi pensado nos modos de jogo Stock, Timed e Crew Battle.


## teams

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BOOLEAN |
| Nullable | No |

Identifica se é uma partida de equipes ou não.


## team_damage

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BOOLEAN |
| Nullable | No |

Identifica se o fogo amigo está ativado ou não. Obviamente sempre será falso se o dado `teams` for falso.


## lives

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vidas (stocks) definidos para cada jogador.


## score_to_win

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Pontuação necessária para vencer em partidas Timed.

Pode ser nulo caso a partida não foi jogada no modo timed ou o valor é infinito (vence quem tiver a maior pontuação).


# Tabela Jogadores_Partidas

Tabela filha da tabela Partidas.

Essa tabela registra dados gerais de cada jogador de uma partida específica.

OBS: Bots não são registrados no banco de dados.


## match_id

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | INT |
| Nullable | No |

Identificador da partida que o jogador participou, chave estrangeira que vem da tabela `Partidas`.


## brawlhalla_id

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BIGINT |
| Nullable | No |

Identificador da conta do jogador, chave estrangeira que está presente na tabela `Jogadores`, mas não está apontando para essa tabela.
Esse dado é recebido direto do brawlhalla e checado pelo PipeValhalla na tabela `Jogadores`.


## current_clan

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | VARCHAR(50) |
| Nullable | No |

Não confundir com o clã do jogador dentro do brawlhalla.

É o identificador do clã do jogador no Panteão de Valhalla naquela partida, confira os clãs do Panteão na tabela `Jogadores`.


## current_player_name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(100) |
| Nullable | No |

É o nome do jogador dentro do Brawlhalla naquela partida.
Como os jogadores costumam usar e trocar de nomes comparado ao seu registro, não é utilizado como chave.


## current_cost

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | SMALLINT |
| Nullable | No |

É o custo do jogador atual naquela partida.
Caso tenha curiosidade para saber quais valores é possível um jogador ter, confira o discord do Panteão de Valhalla para entender esse sistema!


## damage_dealt

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | No |

Dano total causado pelo jogador na partida.


## damage_taken

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | No |

Dano total recebido pelo jogador na partida.


## deaths

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador caiu da arena.


## kos

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador derrubou alguém da arena.



## suicides

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador se jogou da arena.



## clashes

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o ataque do jogador colidiu com o ataque do outro jogador ao mesmo tempo.



## total_dodges

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de esquivas (dodges) que o jogador usou na partida.



## air_dodges

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de esquivas aéreas o jogador usou na partida.



## dashes

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de dashes o jogador usou na partida.



## air_jumps

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador pulou no ar.



## dash_jumps

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de dash + jump o jogador usou na partida.



## total_jumps

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidades totais de pulos do jogador na partida.



## time_in_air

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | INT |
| Nullable | No |

Tempo em milissegundos que o jogador esteve no ar.



## time_on_ground

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | INT |
| Nullable | No |

Tempo em milissegundos que o jogador esteve no chão.



## time_on_wall

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | INT |
| Nullable | No |

Quantidade em milissegundos que o jogador esteve na parede (edge).



## team_num

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Valor numérico do time do jogador (times do brawlhalla azul/vermelho).
Nulo caso a partida não tem o dado `teams` como verdadeiro.



## team_damage_dealt

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | Yes |

Dano que o jogador causou ao seu companheiro de equipe.
Nulo caso a partida não tem o dado `teams` e `team_damage` como verdadeiro.



## team_damage_taken

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | Yes |

Dano que o jogador recebeu do seu companheiro de equipe.
Nulo caso a partida não tem o dado `teams` e `team_damage` como verdadeiro.



## team_kos

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Mortes que o jogador causou ao seu companheiro de equipe.
Nulo caso a partida não tem o dado `teams` e `team_damage` como verdadeiro.



## score

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Pontuação do jogador na partida.
Nulo caso a partida não seja no modo `timed`.



# Tabela Jogadores

Essa tabela guarda todos os jogadores registrados no Panteão de Valhalla, sendo um cadastro de referência.
Nenhuma tabela do banco está diretamente conectada a ela. Essa tabela serve como consulta pro sistema do PipeValhalla adquirir os dados dos jogadores.

## brawlhalla_id

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BIGINT |
| Nullable | No |

Identificador da conta do jogador, nessa tabela é tratada como chave primária.
O identificador do brawlhalla é um inteiro incrementado, conforme a criação de novas contas, o id recebe o valor mais recente + 1.

Tratado como BIGINT, o jogo já possui mais de 100 milhões de contas diferentes.
(Como exemplo, confira minha conta no site corehalla.com e utilize o id: 6972776)



## clan

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Identificador do clã que o jogador faz parte no momento no Panteão de Valhalla.


| Id | Clã |
| --- | --- |
| 1 | Liga dos Buxas |
| 2 | Inimigos da Moda |
| 3 | Rankead Beasts |
| 4 | Dark Triad |
| 5 | Toxicity |
| 6 | Oniscientes |
| 7 | Espada Z.D |
| 8 | Low Cortisol |
| 10 | TEAM TGG |
| 0 | N/A |

Essa lista é dinâmica, então pode haver acréscimos de novos clãs, porém nenhum clã é excluído, mesmo em casos de expulsão ou banimento do clã.



## name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(100) |
| Nullable | No |

Não confundir com o nome in-game.
Nome cadastrado no Panteão de Valhalla.



## cost

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | SMALLINT |
| Nullable | No |

Custo atual do jogador no Panteão de Valhalla. 



# Tabela Loadout

Essa tabela se trata dos "cosméticos" usados pelo jogador.
No arquivo fornecido há muitos outros dados, havendo até mesmo quais skins de arma o jogador usou, mas por decisão de eficiência e utilidade, não foram retirados todos os dados do arquivo.

Pelo esquema feito pelo banco, era possível colocar esses dados na mesma tabela `Jogadores_Partidas`, mas para evitar um "God Table", foi decido separar essa tabela.

## match_id

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | INT |
| Nullable | No |

Identificador da partida que o jogador participou, chave estrangeira que vem da tabela `Partidas`.



## brawlhalla_id

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BIGINT |
| Nullable | No |

Identificador da conta do jogador, chave estrangeira que está presente na tabela `Jogadores`, mas não está apontando para essa tabela.
Esse dado é recebido direto do brawlhalla e checado pelo PipeValhalla na tabela `Jogadores`.



## legend_name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(50) |
| Nullable | No |

Nome do legend usado na partida pelo jogador.



## skin_name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(100) |
| Nullable | No |

Nome da skin usada pelo jogador.



## color_scheme_name

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(100) |
| Nullable | No |

Nome da cor usada pelo jogador no seu legend.



## stance

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(30) |
| Nullable | No |

Stance usada pelo jogador no legend.
Confira a wiki do brawlhalla para saber quais stances existem no jogo.



## random

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BOOLEAN |
| Nullable | No |

Dado booleano que confirma se o jogador usou a configuração "random" (brawlhalla escolher aleatoriamente o esquema Loadout inteiro).



# Tabela Armas

## match_id

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | INT |
| Nullable | No |

Identificador da partida que o jogador participou, chave estrangeira que vem da tabela `Partidas`.



## brawlhalla_id

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BIGINT |
| Nullable | No |

Identificador da conta do jogador, chave estrangeira que está presente na tabela `Jogadores`, mas não está apontando para essa tabela.
Esse dado é recebido direto do brawlhalla e checado pelo PipeValhalla na tabela `Jogadores`.


## weapon

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(30) |
| Nullable | No |

Nome da arma usada pelo jogador na partida, tratada como chave primária nessa tabela.



## time_held

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | INT |
| Nullable | No |

Tempo que o jogador se manteve "segurando" a arma durante a partida, em milissegundos.



## damage_taken

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | No |

Dano que o jogador recebeu enquanto segurava a arma durante a partida.

 

# Tabela Ataques

## match_id

| Propriedade | Value |
| --- | --- |
| Fonte | PipeValhalla |
| Tipo | INT |
| Nullable | No |

Identificador da partida que o jogador participou, chave estrangeira que vem da tabela `Partidas`.



## brawlhalla_id

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | BIGINT |
| Nullable | No |

Identificador da conta do jogador, chave estrangeira que está presente na tabela `Jogadores`, mas não está apontando para essa tabela.
Esse dado é recebido direto do brawlhalla e checado pelo PipeValhalla na tabela `Jogadores`.


## weapon

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(30) |
| Nullable | No |

Nome da arma usada pelo jogador na partida, chave estrangeira nessa tabela que vem da tabela `Armas`.




## attack

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | VARCHAR(30) |
| Nullable | No |

Ataque usado pelo jogador, usado como parte da chave primária.
Para saber quais ataques o jogo possui, verifique a wiki do brawlhalla.



## uses

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que um ataque foi usado na partida pelo jogador.



## enemy_hits

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador acertou o ataque no oponente.



## enemy_damage

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | No |

Quantidade de dano causado pelo ataque no oponente.



## team_hits

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Quantidade de vezes que o jogador acertou o companheiro de equipe com o ataque.
Nulo caso a partida não tenha o dado `teams` e `team_damage` como verdadeiro.



## team_damage

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | Yes |

Quantidade de dano que o jogador causou no companheiro de equipe com o ataque.
Nulo caso a partida não tenha o dado `teams` e `team_damage` como verdadeiro.



## enemy_kos

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de kos o jogador teve com o ataque.



## gc_uses

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador usou o *gravity cancel* em conjunto com o ataque.



## gc_enemy_hits

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de vezes que o jogador usou o *gravity cancel* e acertou um oponente.



## gc_enemy_damage

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | No |

Quantidade de dano causado no oponente usando em conjunto o *gravity cancel*.



## gc_enemy_kos

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | No |

Quantidade de kos que o jogador teve usando em conjunto o *gravity cancel*.



## gc_team_hits

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | SMALLINT |
| Nullable | Yes |

Quantidade de acertos o jogador teve no companheiro de equipe usando em conjunto o *gravity cancel*.
Nulo caso a partida não tenha o dado `teams` e `team_damage` como verdadeiro.



## gc_team_damage

| Propriedade | Value |
| --- | --- |
| Fonte | Brawlhalla |
| Tipo | REAL |
| Nullable | Yes |

Quantidade de dano o jogador causou no companheiro de equipe usando em conjunto o *gravity cancel*.
Nulo caso a partida não tenha o dado `teams` e `team_damage` como verdadeiro.
