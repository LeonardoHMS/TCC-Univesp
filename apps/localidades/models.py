from django.db import models


class Localidade(models.Model):
    TIPO_CHOICES = [
        ('Brasil', 'Brasil'),
        ('Região', 'Região'),
        ('Estado', 'Estado'),
        ('Município', 'Município'),
    ]

    codigo_ibge = models.CharField(max_length=20, blank=True, default='')
    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Estado')
    uf = models.CharField(max_length=2, blank=True)
    regiao = models.CharField(max_length=50, blank=True)
    pais = models.CharField(max_length=100, default='Brasil')

    class Meta:
        ordering = ['nome']
        verbose_name = 'Localidade'
        verbose_name_plural = 'Localidades'
        constraints = [
            models.UniqueConstraint(fields=['codigo_ibge', 'nome'], name='unique_localidade_codigo_nome')
        ]

    def __str__(self):
        return self.nome
