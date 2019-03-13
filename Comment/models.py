from bizz.models import Product, Post
from django.contrib.auth.models import User
from django.db import models

class Faisal(models.Manager):
    def get_queryset(self):
        return super(Faisal, self).get.queryset() \
                                    .filter(active=True)

class Comment(models.Model):

    # user.shop.products.get(id=1).comments.all()  super long query
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    email = models.EmailField(blank=True)  # to be prepopulated from user's sign-up info.
    body = models.TextField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # default manager
    objects = models.Manager()
    # custom manager
    faisal_approved = Faisal()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} comment\'s on {}'.format(self.user.username, self.product.name)
