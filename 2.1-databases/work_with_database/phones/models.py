from autoslug import AutoSlugField
from django.db import models


class Phone(models.Model):
    # TODO: Добавьте требуемые поля
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(
        upload_to='images/',
        null = True,
        blank = True,
    )
    release_date = models.DateField()
    lte_exists = models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='name', unique=True, editable=False)


    def __str__(self):
        return self.name
