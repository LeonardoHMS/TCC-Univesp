# Observatório Brasileiro da Inadimplência

Projeto acadêmico de TCC para integração, tratamento, consulta e visualização de indicadores relacionados à inadimplência e ao contexto socioeconômico brasileiro.

## Objetivo acadêmico

A plataforma tem como finalidade apoiar a análise exploratória de indicadores agregados e públicos, com foco em tendências, comparações e rastreabilidade dos dados. Não há classificação individual de consumidores, não há previsão de inadimplência e não há afirmações de causalidade entre indicadores.

## Arquitetura proposta

A estrutura modular foi organizada para separar responsabilidades por domínio:

- `config/`: configuração central do Django.
- `apps/dashboard/`: landing page, dashboard e páginas públicas.
- `apps/indicadores/`: indicadores, períodos e valores.
- `apps/localidades/`: localidades e mapeamento territorial.
- `apps/fontes/`: fontes de dados e rastreabilidade.
- `apps/importacao/`: importação e registro de processamento de arquivos.
- `templates/`: templates HTML do frontend público.
- `static/`: CSS e recursos estáticos.
- `media/`: uploads de arquivos de importação.

## Stack

- Python 3.14
- Django 6.1
- PostgreSQL (configuração recomendada)
- Pandas e openpyxl para importação de arquivos
- Chart.js no frontend

## Requisitos

- Python 3.12+
- PostgreSQL 16 ou superior
- Docker Desktop (alternativa para executar o PostgreSQL)
- Virtualenv ou venv, caso execute o Django fora do Docker

## Instalação local

1. Crie o ambiente virtual:

   ```bash
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente:

   ```bash
   copy .env.example .env
   ```

4. Ajuste o arquivo `.env` conforme o ambiente.

## Configuração do PostgreSQL

A aplicação usa exclusivamente PostgreSQL por meio da variável `DATABASE_URL`.
SQLite não é suportado. Exemplo para um PostgreSQL instalado localmente:

```env
DATABASE_URL=postgresql://observatorio:observatorio@localhost:5432/observatorio
```

Se você já possui PostgreSQL instalado no Windows, crie o banco `observatorio`,
ajuste as credenciais no `.env` e mantenha o `DATABASE_URL` apontando para
`localhost`.

## Execução com Docker

Com o Docker Desktop instalado e aberto, execute:

```bash
docker compose up --build
```

O Compose inicia o PostgreSQL, aguarda o banco ficar saudável, executa as
migrations e disponibiliza a aplicação em http://127.0.0.1:8000/. Para parar
os serviços:

```bash
docker compose down
```

### Importação do backup OBI

O backup em `database/` usa um esquema legado separado do schema Django. Depois
de restaurá-lo no banco `tcc2026`, importe os registros para as tabelas usadas
pelo frontend. No Windows PowerShell, com os serviços em execução, use:

```powershell
docker compose exec db createdb -U observatorio tcc2026
docker run --rm --network tcc_default `
  -v "${PWD}\database:/backup" `
  -e PGPASSWORD=observatorio `
  postgres:18-alpine `
  pg_restore -h db -U observatorio -d tcc2026 --no-owner --no-privileges `
  /backup/OBI_banco_integracao_2026-10-22.backup
```

Se o banco `tcc2026` já existir, pule o primeiro comando. Depois, importe os
registros para as tabelas usadas pelo frontend:

```bash
docker compose exec web python manage.py import_legacy_data --replace
```

O comando converte fontes, indicadores, localidades, períodos e as 1.533
observações para os modelos da aplicação. A opção `--replace` remove dados
anteriores do observatório, incluindo dados demo.

## Migrations locais

Com um PostgreSQL local em execução e o `.env` configurado:

```bash
python manage.py migrate
```

## Criação do superusuário

```bash
python manage.py createsuperuser
```

## Executando o projeto

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## Carregamento dos dados fictícios

```bash
python manage.py seed_demo_data
```

Esse comando cria dados simulados apenas para desenvolvimento e testes. A aplicação marca claramente essa condição no frontend e no README.

## Execução dos testes

```bash
python manage.py test
```

## Uso do dashboard

O dashboard permite filtrar os dados por indicador, categoria, período, região,
estado e fonte. O filtro inicial é **Todos**, para que região, estado ou fonte
possam ser selecionados individualmente sem receber um indicador implícito.

Para evitar a mistura de unidades de medida e excesso de legendas, o gráfico de
evolução é exibido depois que um indicador é selecionado. Com **Todos**, os
registros continuam disponíveis na tabela e o painel orienta a escolha de um
indicador para montar o gráfico.

## Estrutura das principais tabelas

- `FonteDados`: fontes de dados e rastreabilidade.
- `Indicador`: nome, categoria, unidade, periodicidade.
- `Localidade`: Brasil, regiões, estados, municípios.
- `Periodo`: ano, mês, trimestre e referência temporal.
- `ValorIndicador`: fato principal do observatório, com FK para indicador, fonte, localidade e período.
- `ImportacaoDados`: registro do processamento de arquivos importados.

## Funcionamento da importação

A estrutura de importação foi organizada para receber arquivos em CSV, XLSX e JSON, com etapas de leitura, validação, normalização e persistência. A aplicação já prevê extensões para futuros adaptadores de API.

## Observações importantes

- Não foram inventadas APIs ou endpoints de instituições.
- Não há cadastro de pessoas físicas ou registros individuais.
- Todos os dados de exemplo são simulados para desenvolvimento.
- O Django Admin é usado apenas para administração técnica.

### Mensagem exibida quando dados demo são usados

DADOS SIMULADOS PARA DESENVOLVIMENTO.
