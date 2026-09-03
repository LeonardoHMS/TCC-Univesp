from django.contrib import admin

from .models import FonteDados


@admin.register(FonteDados)
class FonteDadosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'tipo_origem', 'ativo', 'data_atualizacao')
    list_filter = ('ativo', 'tipo_origem')
    search_fields = ('nome', 'instituicao')
