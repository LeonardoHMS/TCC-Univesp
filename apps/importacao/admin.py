from django.contrib import admin

from .models import ImportacaoDados, ErroImportacao


@admin.register(ImportacaoDados)
class ImportacaoDadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'fonte', 'status', 'quantidade_lida', 'quantidade_importada', 'quantidade_rejeitada', 'created_at')
    list_filter = ('status', 'fonte')
    search_fields = ('mensagem_erro',)


@admin.register(ErroImportacao)
class ErroImportacaoAdmin(admin.ModelAdmin):
    list_display = ('importacao', 'linha', 'campo', 'motivo', 'created_at')
    list_filter = ('importacao__fonte',)
    search_fields = ('motivo', 'valor_original')
