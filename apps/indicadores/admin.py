from django.contrib import admin

from .models import Indicador, Periodo, ValorIndicador


@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'unidade_medida', 'periodicidade', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome', 'descricao')


@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    list_display = ('ano', 'mes', 'trimestre', 'data_referencia')
    list_filter = ('ano', 'trimestre')


@admin.register(ValorIndicador)
class ValorIndicadorAdmin(admin.ModelAdmin):
    list_display = ('indicador', 'localidade', 'periodo', 'valor', 'fonte')
    list_filter = ('indicador', 'localidade', 'fonte', 'periodo')
    search_fields = ('indicador__nome', 'localidade__nome', 'observacao')
