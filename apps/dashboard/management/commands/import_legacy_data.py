import os
from collections import defaultdict
from urllib.parse import urlparse

import psycopg2
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from fontes.models import FonteDados
from indicadores.models import Indicador, Periodo, ValorIndicador
from localidades.models import Localidade


class Command(BaseCommand):
    help = 'Importa os dados do banco legado OBI para os modelos do Django.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--database-url',
            default=os.getenv('LEGACY_DATABASE_URL'),
            help='URL PostgreSQL do banco legado, ou use LEGACY_DATABASE_URL.',
        )
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Remove os dados atuais do observatório antes da importação.',
        )

    def handle(self, *args, **options):
        database_url = options['database_url']
        if not database_url:
            raise CommandError('Informe --database-url ou configure LEGACY_DATABASE_URL.')

        parsed = urlparse(database_url)
        if parsed.scheme not in {'postgres', 'postgresql'} or not parsed.path.lstrip('/'):
            raise CommandError('A URL do banco legado deve ser PostgreSQL e incluir o banco.')

        try:
            with psycopg2.connect(database_url) as legacy_connection:
                with legacy_connection.cursor() as cursor:
                    data = self._read_legacy_data(cursor)
        except psycopg2.Error as exc:
            raise CommandError(f'Não foi possível ler o banco legado: {exc}') from exc

        with transaction.atomic():
            if options['replace']:
                ValorIndicador.objects.all().delete()
                Indicador.objects.all().delete()
                Periodo.objects.all().delete()
                Localidade.objects.all().delete()
                FonteDados.objects.all().delete()

            self._import_data(data)

        self.stdout.write(
            self.style.SUCCESS(
                f'Importação concluída: {len(data["observacoes"])} observações, '
                f'{len(data["indicadores"])} indicadores.'
            )
        )

    @staticmethod
    def _read_legacy_data(cursor):
        cursor.execute(
            '''
            SELECT id_fonte, nome, sigla, descricao, url
            FROM fonte
            ORDER BY id_fonte
            '''
        )
        fontes = cursor.fetchall()

        cursor.execute(
            '''
            SELECT id_indicador, nome, descricao, unidade_medida, periodicidade, id_fonte
            FROM indicador
            ORDER BY id_indicador
            '''
        )
        indicadores = cursor.fetchall()

        cursor.execute(
            '''
            SELECT id_localidade, nome, sigla, tipo, id_localidade_pai
            FROM localidade
            ORDER BY id_localidade
            '''
        )
        localidades = cursor.fetchall()

        cursor.execute(
            '''
            SELECT id_periodo, data_inicio, ano, tipo_periodo
            FROM periodo
            ORDER BY id_periodo
            '''
        )
        periodos = cursor.fetchall()

        cursor.execute(
            '''
            SELECT id_observacao, id_indicador, id_localidade, id_periodo, valor, id_categoria
            FROM observacao
            ORDER BY id_observacao
            '''
        )
        observacoes = cursor.fetchall()

        cursor.execute('SELECT id_categoria, nome FROM categoria')
        categorias = dict(cursor.fetchall())

        return {
            'fontes': fontes,
            'indicadores': indicadores,
            'localidades': localidades,
            'periodos': periodos,
            'observacoes': observacoes,
            'categorias': categorias,
        }

    def _import_data(self, data):
        fonte_map = {}
        for source_id, nome, sigla, descricao, url in data['fontes']:
            fonte = FonteDados.objects.create(
                nome=nome,
                instituicao=nome,
                descricao=descricao or '',
                url_origem=url or '',
                tipo_origem='API',
                ativo=True,
            )
            fonte_map[source_id] = fonte

        categories_by_indicator = defaultdict(set)
        for _, indicator_id, _, _, _, category_id in data['observacoes']:
            categories_by_indicator[indicator_id].add(category_id)

        indicador_map = {}
        for indicator_id, nome, descricao, unidade, periodicidade, source_id in data['indicadores']:
            category_ids = categories_by_indicator.get(indicator_id, {None})
            for category_id in category_ids:
                category_name = data['categorias'].get(category_id)
                display_name = f'{nome} — {category_name}' if category_name else nome
                indicador = Indicador.objects.create(
                    nome=display_name,
                    descricao=descricao or '',
                    categoria=self._category_for_indicator(nome),
                    unidade_medida=unidade,
                    periodicidade=periodicidade or '',
                    ativo=True,
                )
                indicador_map[(indicator_id, category_id)] = (indicador, fonte_map[source_id])

        parent_by_id = {row[0]: row for row in data['localidades']}
        locality_map = {}
        for locality_id, nome, sigla, tipo, parent_id in data['localidades']:
            parent = parent_by_id.get(parent_id)
            parent_name = parent[1] if parent else ''
            locality_map[locality_id] = Localidade.objects.create(
                codigo_ibge=sigla or '',
                nome=nome,
                tipo=self._locality_type(tipo),
                uf=sigla if tipo == 'uf' else '',
                regiao=parent_name if tipo == 'uf' else (nome if tipo == 'regiao' else 'Brasil'),
                pais='Brasil',
            )

        period_map = {}
        for period_id, data_inicio, ano, tipo_periodo in data['periodos']:
            month = data_inicio.month if tipo_periodo == 'mensal' else None
            quarter = ((data_inicio.month - 1) // 3) + 1 if tipo_periodo == 'trimestral' else None
            period_map[period_id] = Periodo.objects.create(
                ano=ano,
                mes=month,
                trimestre=quarter,
                data_referencia=data_inicio,
            )

        for observation_id, indicator_id, locality_id, period_id, value, category_id in data['observacoes']:
            indicator, source = indicador_map[(indicator_id, category_id)]
            ValorIndicador.objects.create(
                indicador=indicator,
                fonte=source,
                localidade=locality_map[locality_id],
                periodo=period_map[period_id],
                valor=value,
                unidade_original=indicator.unidade_medida,
                metadados={
                    'legacy_observacao_id': observation_id,
                    'legacy_categoria_id': category_id,
                    'importado_do_banco_legado': True,
                },
            )

    @staticmethod
    def _locality_type(value):
        return {
            'pais': 'Brasil',
            'regiao': 'Região',
            'uf': 'Estado',
        }.get(value, 'Município')

    @staticmethod
    def _category_for_indicator(name):
        normalized = name.lower()
        if 'juros' in normalized:
            return 'crédito'
        if 'dívida' in normalized or 'divida' in normalized:
            return 'endividamento'
        if 'inadimpl' in normalized:
            return 'inadimplência'
        return 'outros'
