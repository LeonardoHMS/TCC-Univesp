from django.db import models

from fontes.models import FonteDados


class ImportacaoDados(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'PENDENTE'),
        ('PROCESSANDO', 'PROCESSANDO'),
        ('CONCLUIDO', 'CONCLUIDO'),
        ('ERRO', 'ERRO'),
    ]

    fonte = models.ForeignKey(FonteDados, on_delete=models.PROTECT, related_name='importacoes', blank=True, null=True)
    arquivo = models.FileField(upload_to='importacoes/%Y/%m/%d/', blank=True, null=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_fim = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    quantidade_lida = models.PositiveIntegerField(default=0)
    quantidade_importada = models.PositiveIntegerField(default=0)
    quantidade_rejeitada = models.PositiveIntegerField(default=0)
    mensagem_erro = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Importação de dados'
        verbose_name_plural = 'Importações de dados'

    def __str__(self):
        return f'Importação #{self.pk} - {self.status}'
