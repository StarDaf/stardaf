from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
# from django.utils import timezone
from django.utils import timezone
from PIL import Image
from PIL import ImageFilter
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Contact(models.Model):
    """we have to create a foreignKey for both sides of the.
    relation."""

    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

class Profile(models.Model):
    """extending the django user model."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    #image = models.ImageField(upload_to='users/%y/%m/%d', blank=True, db_index=True)  # can be left out.
    image = ImageField(upload_to='users/%y/%m/%d', blank=True,db_index=True)
    phone = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True, db_index=True)  # can also be left out.
    gender = models.CharField(max_length=50)  # male or female
    created = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        self.image = self.compressImage(self.image)
        super(Profile, self).save(*args, **kwargs)

    def compressImage(self,image):
        if self.image:
            imageTemproary = Image.open(image)
            imi = imageTemproary.convert('RGB')
            outputIoStream = BytesIO()
            imageTemproaryResized = imageTemproary.resize( (1020,573) ) 
            imi.save(outputIoStream , format='JPEG', quality=50)
            outputIoStream.seek(0)
            image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
            return image

    def __str__(self):
        return 'Profile for {}'.format(self.user.username)

# symmetrical set to false because, following me does not mean i should follow you.
User.add_to_class('following', models.ManyToManyField('self', through=Contact, symmetrical=False, related_name='followers'))


