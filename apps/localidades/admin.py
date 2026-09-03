from django.contrib import admin

from .models import Localidade


@admin.register(Localidade)
class LocalidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'uf', 'regiao', 'pais')
    list_filter = ('tipo', 'regiao', 'pais')
    search_fields = ('nome', 'uf', 'codigo_ibge')
