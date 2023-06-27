from django.db import models

# Create your models here.

class DS(models.Model):
    title = models.CharField('Название', max_length=50)
    DS = models.TextField('Описание')

    def __str__(self):
        return self.title

class Dataset(models.Model):
    title = models.CharField('Название', max_length=255)
    created_at= models.DateField(auto_now_add=True)
    num_rows = models.IntegerField('Количество строк')


class Content(models.Model):
    country = models.CharField(max_length=255)
    first_name= models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    date = models.DateField()
    number = models.IntegerField()
    email = models.EmailField()

