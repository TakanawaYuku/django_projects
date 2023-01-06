from django.db import models


# Create your models here.
class MyModelName(models.Model):

    my_field_name = models.CharField(max_length=20,
                                     help_text='Введите полевую документацию')

    class Meta:
        ordering = ['-my_field_name']
        # ordering = ['title', '-pubdate']
        # verbose_name = 'Better name'
