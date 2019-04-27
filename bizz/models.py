from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from sorl.thumbnail import ImageField
from django.core.validators import MaxValueValidator
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from taggit.managers import TaggableManager
# import datetime

#user.shop.products.all()
# this model account for the user having more than one shop.
# in the future this can be changed.
# future code

# class Shop(models.Model):
#     user.shop.all() or user.shop.get(id=1).products.all()
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='shop', on_delete=models.CASCADE)
#     business_name = models.CharField(max_length=300)
#     business_address = models.CharField(max_length=500)
#     home_address = models.CharField(max_length=500)
#     logo = models.ImageField(upload_to='bizz/%y/%m/%d', blank=True)  # his companies logo ('Or any image of choice')
#     auth_image = models.ImageField(upload_to='auth/%y/%m/%d', blank=True)  # to be filled by our authentication agents.
#     market_name = models.CharField(max_length=300, db_index=True)
#     created = models.DateTimeField(auto_now_add=True, db_index=True)
#
#     def __str__(self):
#         return '{}\'s business'.format(self.user)
#
#     # returns total number of products in the shop.
#     def get_total_products(self):
#         return self.products.count()


# class Market(models.Model):
    
#     MARKETS = (
#         ('farm_center', 'Farm_Center'),
#     )

#     market = models.CharField(choices=MARKETS,
#         max_length=20)

#     def __str__(self):
#         return self.market

class Shop(models.Model):
    """shop model."""

    # user.shop.attribute  # shop.owner
    BUSINESS_ADDRESS = (
        ('private', 'Private'),
    )
    BANKS = (
        ('Access Bank Plc', 'Access Bank Plc'),
        ('Citibank Nigeria Limited', 'Citibank Nigeria Limited'),
        ('Diamond Bank Plc', 'Diamond Bank Plc'),
        ('Ecobank Nigeria Plc', 'Ecobank Nigeria Plc'),
        ('Fidelity Bank Plc', 'Fidelity Bank Plc'),
        ('First City Monument Bank Plc', 'First City Monument Bank Plc'),
        ('First Bank Limited', 'First Bank Limited'),
        ('Guaranty Trust Bank Plc', 'Guaranty Trust Bank Plc'),
        ('Heritage Banking Company Limited', 'Heritage Banking Company Limited'),
        ('JAIZ Bank Plc', 'JAIZ Bank Plc'),
        ('Keystone Bank Limited', 'Keystone Bank Limited'),
        ('Polaris Bank Limited', 'Polaris Bank Limited'),
        ('Providus Bank Limited', 'Providus Bank Limited'),
        ('Stanbic IBTC Bank Plc', 'Stanbic IBTC Bank Plc'),
        ('Standard Chartered', 'Standard Chartered'),
        ('Sterling Bank Plc', 'Sterling Bank Plc'),
        ('SunTrust Bank Nigeria Limited', 'SunTrust Bank Nigeria Limited'),
        ('Union Bank of Nigeria Plc', 'Union Bank of Nigeria Plc'),
        ('United Bank for Africa Plc', 'United Bank for Africa Plc'),
        ('Unity Bank Plc', 'Unity Bank Plc'),
        ('Wema Bank Plc', 'Wema Bank Plc'),
        ('Zenith Bank Plc', 'Zenith Bank Plc'),
        
    )
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='shop', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=300)
    # market = models.ForeignKey(Market, related_name='shops', on_delete=models.CASCADE, null=True)
    #business_address = models.CharField(max_length=500)
    business_address = models.CharField(max_length=20, choices=BUSINESS_ADDRESS, default='private')
    #shop_number = models.CharField(default='', max_length=1000)
    shop_address = models.CharField(max_length=300, db_index=True, default='')  
    home_address = models.CharField(max_length=500)
    #logo = models.ImageField(upload_to='bizz/%y/%m/%d', blank=True)  # his companies logo ('Or any image of choice')
    logo = ImageField(upload_to='bizz/%y/%m/%d', blank=True)
    #auth_image = models.ImageField(upload_to='auth/%y/%m/%d', blank=True)  # to be filled by our authentication agents.
    Bank = models.CharField(max_length=250, choices=BANKS, default='')
    #account_number = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    account_number = models.CharField(max_length=10, blank=True, null=True)
    account_name = models.CharField(max_length=250, default='', blank=True)

    

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        
        self.logo = self.compressImage(self.logo)
        super(Shop, self).save(*args, **kwargs)
    def compressImage(self,logo):
        imageTemproary = Image.open(logo)
        im = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        im.save(outputIoStream , format='JPEG', quality=50)
        outputIoStream.seek(0)
        logo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % logo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return logo

    # returns total number of products in the shop.
    def get_total_products(self):
        return self.products.count()


class Product(models.Model):
    """user.shop.products.all()"""

    CATEGORY_OF_PRODUCTS = (
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
    )

    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=500, default='', unique_for_date='created')
    name = models.CharField(max_length=250) # the name of the product
    category = models.CharField(max_length=20,
                                choices=CATEGORY_OF_PRODUCTS,
                                default='clothing')  # category the product belong's to.

    # price of the product (price can be left blank hence users negotiate with the sellers)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    stock = models.PositiveIntegerField(blank=True, null=True, default=0)  # quantity of product available
    #photo = models.FileField(upload_to='products/%y/%m/%d', blank=True, null=True)  # image of product
    photo = ImageField(upload_to='products/%y/%m/%d', blank=True, null=True)
    photo0 = ImageField(upload_to='products/%y/%m/%d', blank=True, null=True, default='')
    photo1 = ImageField(upload_to='products/%y/%m/%d', blank=True, null=True, default='')
    photo2 = ImageField(upload_to='products/%y/%m/%d', blank=True, null=True, default='')
    photo3 = ImageField(upload_to='products/%y/%m/%d', blank=True, null=True, default='')
    payment_link = models.CharField(max_length=10000, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=False)  # can be user to disable products
    description = models.TextField(blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_liked', blank=True) # user.product_liked.all()
    users_hate = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_hated', blank=True)
    total_views = models.PositiveIntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    video = models.FileField(upload_to='videos/%y/%m/%d', default='', null=True, blank=True)
    tags = TaggableManager()

    # product.users_like.all()

    def rank(self):
        return (self.users_like.count() - self.users_hate.count())

    def save(self, *args, **kwargs):
        """to automatically generate the slug field based on the.
        shop owner's first_name"""

        self.photo = self.compressImage(self.photo)
        if self.photo1:
            self.photo1 = self.compressImage(self.photo1)
        if self.photo2:
            self.photo2 = self.compressImage(self.photo2)    
        if self.photo3:
            self.photo3 = self.compressImage(self.photo3)    

        if not self.slug:
            self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)

    def compressImage(self,logo):
        imageTemproary = Image.open(logo)
        imi = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imi.save(outputIoStream , format='JPEG', quality=50)
        outputIoStream.seek(0)
        logo = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % logo.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return logo




    def get_absolute_url(self):
        return reverse('bizz:detail', args=[self.id, self.slug, self.shop.owner.username])

    def __str__(self):
        return 'This product belongs to shop: {}, owned by: {}'.format(self.shop.business_name, self.shop.owner.get_full_name())


class Post(models.Model):
    
    title = models.CharField(max_length=250, default='')
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # user.posts.all()
    introduction = models.TextField(blank=True, null=True)
    post = models.TextField(default='', blank=True, null=True)
    paragraph_2 = models.TextField(default='', blank=True, null=True)
    paragraph_3 = models.TextField(default='', blank=True, null=True)
    paragraph_4 = models.TextField(default='', blank=True, null=True)
    paragraph_5 = models.TextField(default='', blank=True, null=True)
    question = models.CharField(max_length=200, blank=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_liked', blank=True) # user.product_liked.all()
    users_hate = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_hated', blank=True)
    
    
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post/%y/%m/%d', blank=True, null=True, default='')
    video = models.FileField(upload_to='post_videos/%y/%m/%d', default='', null=True, blank=True)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('bizz:post_text', args=[self.id, self.title])

    def save(self, *args, **kwargs):
        
        self.image = self.compressImage(self.image)
        super(Post, self).save(*args, **kwargs)
    def compressImage(self,image):
        imageTemproary = Image.open(image)
        imi = imageTemproary.convert('RGB')
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
        imi.save(outputIoStream , format='JPEG', quality=50)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return image




class Governor(models.Model):
    name = models.CharField(max_length=500)
    party = models.CharField(max_length=500)
    image = models.FileField(upload_to='election/%y/%m/%d')
    party_logo = models.FileField(upload_to='election_logo/%y/%m/%d')
    counts = models.DecimalField(max_digits=7, decimal_places=0)
    percent = models.CharField(max_length=50, default="")

class Supporter(models.Model):
    user = models.ForeignKey(User, related_name='supporters', on_delete=models.CASCADE)  # governor.supporters.create(user=user)
    # governors.supporters.count()
    # # algorithim
    # total_counts = 2,000,000
    #governor1 = Governor.objects.get(id=1)
    #governor2 = Governor.objects.get(id=2)
    # percent1 = int(governor1.count * 100) / 2,000,000
    # percent2 = int(governor2.count * 100) / 2, 000,000 
    # total vosts cast = int(governor1.count) + int(governor2.count)
    # remaining votes = 2, 000,000 - total vosts cast   
