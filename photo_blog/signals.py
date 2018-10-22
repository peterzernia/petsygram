import os
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Post, Comment, Notification
from users.models import Profile


# Image file is deleted when post is deleted.
@receiver(post_delete, sender=Post)
def auto_delete_file_on_post_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)


# Creates a notification object if a comment is made on a post by a user other
# than the author.
@receiver(post_save, sender=Comment)
def auto_create_comment_notification(sender, instance, created, **kwargs):
    if created:
        if instance.author != instance.post.author:
            Notification.objects.create(post=instance.post, comment=instance, date_posted=instance.date_posted)

# Creates a notification instance if a post is liked.
@receiver(m2m_changed, sender=Post.likes.through)
def auto_create_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        Notification.objects.create(post=instance, user=instance.likes.through.objects.last().user, liked=True)
    if action == "post_remove":
        for num in pk_set:
            pk = num
        Notification.objects.filter(user_id=pk, post=instance).delete()


# Creates a notification instance if a user is followed.
@receiver(m2m_changed, sender=Profile.followers.through)
def auto_create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        Notification.objects.create(profile=instance, user=instance.followers.through.objects.last().user, followed=True)
    if action == "post_remove":
        for num in pk_set:
            pk = num
        Notification.objects.filter(user_id=pk, profile=instance).delete()
