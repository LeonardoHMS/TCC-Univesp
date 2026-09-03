from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from fontes.models import FonteDados
from indicadores.models import Indicador, Periodo, ValorIndicador
from localidades.models import Localidade


class DashboardViewsTests(TestCase):
    def setUp(self):
        fonte = FonteDados.objects.create(
            nome='Teste de fonte',
            instituicao='Instituição de Teste',
            tipo_origem='CSV',
            url_origem='https://example.com',
        )
        localidade = Localidade.objects.create(codigo_ibge='3550308', nome='São Paulo', tipo='Estado', uf='SP', regiao='Sudeste')
        indicador = Indicador.objects.create(
            nome='Taxa de inadimplência',
            categoria='inadimplência',
            unidade_medida='%',
            periodicidade='mensal',
        )
        periodo = Periodo.objects.create(ano=2025, mes=3, trimestre=2, data_referencia='2025-03-01')
        ValorIndicador.objects.create(indicador=indicador, fonte=fonte, localidade=localidade, periodo=periodo, valor='8.5', unidade_original='%')

    def test_home_page_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Observatório Brasileiro da Inadimplência')

    def test_seed_demo_data_command(self):
        call_command('seed_demo_data')
        self.assertTrue(Indicador.objects.exists())
        self.assertTrue(FonteDados.objects.exists())
        self.assertTrue(ValorIndicador.objects.exists())
