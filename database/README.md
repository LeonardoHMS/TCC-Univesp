# OBI — Banco de Dados

Banco de dados PostgreSQL desenvolvido para o projeto TCC OBI — Observatório Brasileiro da Inadimplência.

## Informações gerais

- SGBD: PostgreSQL 18
- Banco original: `tcc2026`
- Período dos dados: janeiro de 2023 a agosto de 2026
- Fontes: Banco Central do Brasil e Serasa
- Indicadores cadastrados: 5
- Observações: 1.533
- Views: 5

## Estrutura

O banco utiliza tabelas relacionais para organizar fontes, indicadores, localidades, períodos, categorias e observações.

## Integração

O banco será utilizado pelo backend Django para disponibilizar os indicadores e suas séries históricas ao frontend do OBI.

A documentação técnica e as instruções de restauração serão acrescentadas nesta pasta.
