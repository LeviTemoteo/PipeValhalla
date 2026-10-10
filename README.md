# PipeValhalla

Sistema de coleta de dados do Panteão de Valhalla.

Por comandos via CLI, o sistema faz a extração de dados e envia os dados tratados ao Banco de Dados.

---

## Panteão de Valhalla

Para quem é de fora do jogo, o Panteão de Valhalla é uma organização criada pela comunidade brasileira de Brawlhalla, nela é administrado um campeonato de pontos corridos, tendo o foco em clãs (times) e seus confrontos. Um e-Sports diferenciado.

Ideia estruturada pelo player YaksaTH e continuada pela a Staff do Panteão de Valhalla, o time com mais pontos no final do campeonato se torna o vencedor!

Redes:

- Canal de transmissão pela Twitch
- Discord oficial
- Site do Panteão

---

## Sistema do Pipevalhalla

A ideia central desse sistema é automatizar a coleta de dados de **todas** as partidas realizadas no campeonato.

Essa automatização se beneficia de uma opção de inicialização via Steam, que é o comando -writestats.

### -writestats

Dentro das propriedades do Brawlhalla na Steam, é possível colocar uma opção de inicialização, o -writestats.

No início de campeonatos oficiais do Brawlhalla, havia um problema de coleta de informações das partidas, algo que é muito importante nos e-Sports, com isso, os desenvolvedores do jogo criaram um inicializador de registro de dados da partida.

Tendo essa opção ativada, o Brawlhalla irá guardar um arquivo no formato JSON, havendo todos os dados da partida. 
O PipeValhalla tira vantagem justamente desse arquivo! Por tanto, o mesmo arquivo que o Brawlhalla oficialmente usa em seus torneios, o Panteão de Valhalla usará para seus campeonatos.

Para saber como é esse arquivo, dê uma olhada em: docs/partidas_base/...

## Banco Modelo

Para ter mais detalhes visualmente do banco de dados, criei uma planilha pelo Google Sheets:

https://docs.google.com/spreadsheets/d/1MPmtRNx-gMNYI6uvHKEQ9nulzp03lpwjLLW-AeuBe_g/edit?gid=0#gid=0

Está inserido 3 partidas de teste e o esquema das tabelas.

Caso tenha curiosidade sobre os dados, dê uma olhada em docs/dicionario_de_dados.md


