from django.db import IntegrityError
from django.test import TestCase

from fontes.models import FonteDados
from indicadores.models import Indicador, Periodo, ValorIndicador
from localidades.models import Localidade


class IndicadoresModelsTests(TestCase):
    def test_indicator_creation(self):
        indicador = Indicador.objects.create(
            nome='Renda média',
            categoria='renda',
            unidade_medida='R$',
            periodicidade='mensal',
        )
        self.assertEqual(str(indicador), 'Renda média')

    def test_unique_value_is_enforced(self):
        fonte = FonteDados.objects.create(
            nome='Fonte teste',
            instituicao='Instituição',
            tipo_origem='CSV',
        )
        localidade = Localidade.objects.create(codigo_ibge='3550308', nome='São Paulo', tipo='Estado', uf='SP', regiao='Sudeste')
        indicador = Indicador.objects.create(
            nome='Taxa de desemprego',
            categoria='emprego/desemprego',
            unidade_medida='%',
            periodicidade='mensal',
        )
        periodo = Periodo.objects.create(ano=2025, mes=4, trimestre=2, data_referencia='2025-04-01')

        ValorIndicador.objects.create(indicador=indicador, fonte=fonte, localidade=localidade, periodo=periodo, valor='7.1', unidade_original='%')

        with self.assertRaises(IntegrityError):
            ValorIndicador.objects.create(indicador=indicador, fonte=fonte, localidade=localidade, periodo=periodo, valor='7.2', unidade_original='%')
