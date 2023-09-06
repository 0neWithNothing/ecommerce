from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to ='uploads/')
    price = models.FloatField()
    size = models.ManyToManyField('Size', blank=True)
    category = models.ForeignKey('Category', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title
