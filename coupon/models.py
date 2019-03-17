from django.db import models
from bizz.models import Product


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    discount = models.CharField(max_length=20)
    active = models.BooleanField()
    product = models.ForeignKey(Product, related_name='coupons', on_delete=models.CASCADE, null=True, blank=True)  # product.coupons.all

    def __str__(self):
        return self.code