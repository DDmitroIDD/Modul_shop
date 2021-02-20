from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    wallet = models.PositiveSmallIntegerField(default=10000)

    def __str__(self):
        return f'{self.username} id {self.id}'


class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=1000)
    price = models.PositiveIntegerField(default=0)
    quantity_in_stock = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name} id {self.id}'


class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_of_products = models.PositiveSmallIntegerField(default=1)
    time_of_buy = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User_id-{self.user.id} | Product-{self.product.name} | qt.{self.quantity_of_products} | id-{self.id}'


class PurchaseReturns(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    time_of_request = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User_id-{self.purchase.user.id} Prod.-{self.purchase.product.name} {self.purchase.product.id} '
