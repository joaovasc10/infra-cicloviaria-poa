from django.db import models

class Ciclovia(models.Model):
    data_extracao = models.DateTimeField(null=True, blank=True)
    descricao = models.CharField(max_length=100, db_index=True)
    estado = models.CharField(max_length=20)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    implantacao = models.DateField(null=True, blank=True, db_index=True)
    logradouro_nome = models.CharField(max_length=100, db_index=True)
    num_inicial = models.CharField(max_length=20, null=True, blank=True)
    num_final = models.CharField(max_length=20, null=True, blank=True)
    defronte = models.CharField(max_length=10, null=True, blank=True)
    cruzamento_nome = models.CharField(max_length=100, null=True, blank=True)
    lado = models.CharField(max_length=20, null=True, blank=True)
    fluxo = models.CharField(max_length=20, null=True, blank=True)
    local_de_instal = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.logradouro_nome} ({self.descricao})"

    class Meta:
        verbose_name = "Ciclovia"
        verbose_name_plural = "Ciclovias"
        indexes = [
            models.Index(fields=['logradouro_nome']),
            models.Index(fields=['implantacao']),
        ]
