import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.signals import post_delete, pre_save
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


@receiver(post_delete, sender=Profile)
def auto_delete_profile_image_file_on_profile_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path) and not instance.image.path.endswith("/media/default.jpg"):
            os.remove(instance.image.path)


@receiver(pre_save, sender=Profile)
def auto_delete_profile_image_file_on_image_update(sender, instance, **kwargs):
    try:
        old_file = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False

    new_file = instance.image
    if new_file != old_file:
        if os.path.isfile(old_file.path) and not old_file.path.endswith("/media/default.jpg"):
            os.remove(old_file.path)
