from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)
class Sensor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название датчика")
    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    class Meta:
        ordering = ['name']
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"

    def __str__(self):
        return self.name

class Measurement(models.Model):
    temperature = models.FloatField()
    recorded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время замера"
    )
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.PROTECT,
        related_name='measurements',
        verbose_name="Датчик"
    )

    class Meta:
        ordering = '-recorded_at',
        verbose_name = "Измерение",
        verbose_name_plural = "Измерения"


    def __str__(self): return f"{self.sensor.name} — {self.temperature} ({self.recorded_at.strftime('%Y-%m-%d %H:%M')})"
