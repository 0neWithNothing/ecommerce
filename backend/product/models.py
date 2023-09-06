from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.ManyToManyField(Size, blank=True)
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to ='uploads/')
    product = models.ForeignKey(Product,related_name='images', on_delete=models.CASCADE)
    default = models.BooleanField(default=False)