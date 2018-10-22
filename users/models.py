import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    followers = models.ManyToManyField(User, blank=True, related_name='user_followers')

    def __str__(self):
        return f'{self.user.username} Profile'

# Save checks exif information for cellphone photos to see what orientation the
# photo was taken in, then rotates the image to be upright. images are reduced
# to an output of 200px x 200px to save room on the server.
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        exif = img._getexif()
        orientation_key = 274
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]

            rotate_values = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }

            if orientation in rotate_values:
                img = img.transpose(rotate_values[orientation])

        output_size = (200, 200)
        img.thumbnail(output_size)
        img.save(self.image.path)
