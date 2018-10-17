import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=150, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    followers = models.ManyToManyField(User, blank=True, related_name='user_followers')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        output_size = (150, 150)
        img.thumbnail(output_size)
        img.save(self.image.path)


@receiver(post_delete, sender=Profile)
def auto_delete_file_on_post_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path) and not instance.image.path.endswith("/media/default.jpg"):
            os.remove(instance.image.path)
