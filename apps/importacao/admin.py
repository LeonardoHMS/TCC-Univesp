from django.contrib import admin

from .models import ImportacaoDados


@admin.register(ImportacaoDados)
class ImportacaoDadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'fonte', 'status', 'quantidade_lida', 'quantidade_importada', 'quantidade_rejeitada', 'created_at')
    list_filter = ('status', 'fonte')
    search_fields = ('mensagem_erro',)
