import os
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse
from django.conf import settings


def get_image_path(instance, filename):
    return os.path.join('posts', str(instance.author), filename)


class Post(models.Model):
    photo = models.ImageField(upload_to=get_image_path, null=True, blank=False)
    caption = models.TextField(max_length=2200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    location = models.CharField(max_length=30, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('photo_blog-detail', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('photo_blog-post_like_api', kwargs={"pk": self.pk})

# Save checks exif information for cellphone photos to see what orientation the
# photo was taken in, then rotates the image to be upright. images are reduced
# to a width of 450px, with proportionally reduced height to save room on the
# server.
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.photo.path)
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

        output_size = (450, (img.height / img.width) * 450)
        img.thumbnail(output_size)
        img.save(self.photo.path)



class Comment(models.Model):
    post = models.ForeignKey('photo_blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=2200)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    def save(self, **kwargs):
        super().save()


# Notification model is used for three different types of notifications: like,
# comment, and follow notifications.
class Notification(models.Model):
    post = models.ForeignKey('photo_blog.Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    liked = models.BooleanField(default=False, null=True)
    followed = models.BooleanField(default=False, null=True)
    date_posted = models.DateTimeField(null=True, blank=True)
