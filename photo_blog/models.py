import os
from PIL import Image
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


def get_image_path(instance, filename):
    return os.path.join('posts', str(instance.author), filename)


class Post(models.Model):
    photo = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    caption = models.TextField(max_length=2200, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    location = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('photo_blog-detail', kwargs={'pk': self.pk})

    def get_api_like_url(self):
        return reverse('photo_blog-post_like_api', kwargs={"pk": self.pk})

    def save(self):
        super().save()

        img = Image.open(self.photo.path)

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

    def save(self):
        super().save()

    def get_absolute_url(self):
        return reverse('photo_blog-comment', kwargs={'pk': self.pk})


class Notification(models.Model):
    post = models.ForeignKey('photo_blog.Post', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    liked = models.BooleanField(default=False)
    date_posted = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=Comment)
def auto_create_comment_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(post=instance.post, comment=instance, date_posted=instance.date_posted)


@receiver(m2m_changed, sender=Post.likes.through)
def auto_create_like_notification(sender, instance, action, **kwargs):
    if action == "post_add":
        post = instance.likes.all()
        Notification.objects.create(post=instance, user=instance.likes.through.objects.last().user, liked=True)
    
