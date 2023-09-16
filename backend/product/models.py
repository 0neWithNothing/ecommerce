from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

User = get_user_model()

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
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.ManyToManyField(Size, blank=True, related_name='products')
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to ='uploads/')
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    default = models.BooleanField(default=False)


class Cart(models.Model):
    user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    def __str__(self) -> str:
        return self.user.email


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.product.price * self.count
    
    def __str__(self) -> str:
        return self.product.title
    

def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

post_save.connect(create_cart, sender=User)