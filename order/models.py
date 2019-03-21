from django.db import models
from django.contrib.auth.models import User
from bizz.models import Product
from django.conf import settings
from django.utils import timezone

# order form to be filled when placing an order
now = timezone.now()
class Order(models.Model):

    STATES_ACTIVE = (
        ('kano', 'Kano'),
        ('bauchi', 'Bauchi')
    )

    MAX_QUANTITY = (
        ('1', str(1)),
        ('2', str(2)),
        ('3', str(3)),
        ('4', str(4)),
        ('5', str(5)),
        ('6', str(6)),
        ('7', str(7)),
        ('8', str(8)),
        ('9', str(9)),
        ('10', str(10)),
        ('11', str(11)),
        ('12', str(12)),
        ('13', str(13)),
        ('14', str(14)),
        ('15', str(15)),
    )

    # user.order_created.all()
    user = models.ForeignKey(User, related_name='order_created', on_delete=models.CASCADE)
    
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    city = models.CharField(choices=STATES_ACTIVE,
                            max_length=15,
                            default='kano')
    quantity = models.CharField(choices=MAX_QUANTITY,
                                max_length=5,
                                default='1')

    phone_number = models.DecimalField(max_digits=13, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    #product = models.ForeignKey(Product, related_name='order_products',on_delete=models.CASCADE, null=True)
    pproduct = models.ForeignKey(Product, related_name='products', unique=False,on_delete=models.CASCADE, null=True)  # order.products.get
    discount_code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}\' order no: {}'.format(self.user.username, self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, default='')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.quantity * self.price



