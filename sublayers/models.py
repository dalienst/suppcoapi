from django.db import models
from django.contrib.auth import get_user_model

from accounts.abstracts import TimeStampedModel, UniversalIdModel, ReferenceModel
from layers.models import Layer

User = get_user_model()

class SubLayer(TimeStampedModel, UniversalIdModel, ReferenceModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sublayers")
    name = models.CharField(max_length=255,)
    layer = models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='sublayers')

    class Meta:
        verbose_name = 'SubLayer'
        verbose_name_plural = 'SubLayers'
        ordering = ['created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'layer'],
                name='unique_sublayer_name_per_layer',
            )
        ]

    def __str__(self):
        return self.name
    