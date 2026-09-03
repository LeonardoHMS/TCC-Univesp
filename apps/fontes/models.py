from django.db import models


class FonteDados(models.Model):
    TIPO_ORIGEM_CHOICES = [
        ('CSV', 'CSV'),
        ('XLSX', 'XLSX'),
        ('JSON', 'JSON'),
        ('API', 'API'),
        ('MANUAL', 'MANUAL'),
    ]

    nome = models.CharField(max_length=150)
    instituicao = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    url_origem = models.URLField(blank=True)
    tipo_origem = models.CharField(max_length=20, choices=TIPO_ORIGEM_CHOICES, default='CSV')
    data_atualizacao = models.DateField(null=True, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Fonte de dados'
        verbose_name_plural = 'Fontes de dados'

    def __str__(self):
        return f'{self.nome} ({self.instituicao})'
