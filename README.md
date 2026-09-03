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
- PostgreSQL 16 (opcional para execução local via Docker)
- Virtualenv ou venv

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

A configuração padrão do projeto usa PostgreSQL via `DATABASE_URL`. Exemplo:

```env
DATABASE_URL=postgresql://observatorio:observatorio@localhost:5432/observatorio
```

Se preferir, é possível subir o banco com Docker Compose:

```bash
docker compose up -d db
```

## Migrations

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
