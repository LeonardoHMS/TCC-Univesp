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

    def test_dashboard_uses_database_data_for_chart(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['selected_indicator'])
        self.assertEqual(response.context['chart_data'], {'labels': [], 'datasets': []})
        self.assertContains(response, 'Selecione um indicador para visualizar a evolução.')

    def test_dashboard_region_filter_works_without_indicator_filter(self):
        response = self.client.get(reverse('dashboard'), {'regiao': 'Sudeste'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['selected_indicator'])
        self.assertEqual(len(response.context['tabela']), 1)
        self.assertContains(response, 'São Paulo')

    def test_dashboard_state_filter_works_without_indicator_filter(self):
        response = self.client.get(reverse('dashboard'), {'estado': str(Localidade.objects.first().id)})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['selected_indicator'])
        self.assertEqual(len(response.context['tabela']), 1)

    def test_dashboard_category_filter_is_not_limited_by_default_indicator(self):
        renda = Indicador.objects.create(
            nome='Renda média',
            categoria='renda',
            unidade_medida='R$',
            periodicidade='mensal',
        )
        ValorIndicador.objects.create(
            indicador=renda,
            fonte=FonteDados.objects.first(),
            localidade=Localidade.objects.first(),
            periodo=Periodo.objects.first(),
            valor='3000',
        )
        response = self.client.get(reverse('dashboard'), {'categoria': 'renda'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['selected_indicator'])
        self.assertFalse(response.context['chart_data']['datasets'])
        self.assertContains(response, 'Renda média')

    def test_seed_demo_data_command(self):
        call_command('seed_demo_data')
        self.assertTrue(Indicador.objects.exists())
        self.assertTrue(FonteDados.objects.exists())
        self.assertTrue(ValorIndicador.objects.exists())
