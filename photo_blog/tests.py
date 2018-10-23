from django.test import TestCase
from .models import Post, Comment, Notification, get_image_path
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import random


class PostTest(TestCase):
    def create_post(self, caption='#selfie',
                    author=User.objects.create_user(username=str(random.randint(1,100000)),
                                                    password='12345'),
                    photo=SimpleUploadedFile(name='default.jpg',
                                             content=open('./media/default.jpg',
                                                          'rb').read(),
                                             content_type='image/jpeg'),
                    location='New York'):
        return Post.objects.create(caption=caption,
                                   date_posted=timezone.now(),
                                   author=author,
                                   photo=photo,
                                   location=location)

    def test_post_creation(self):
        test_post = self.create_post()
        self.assertTrue(isinstance(test_post, Post))
        self.assertEqual(test_post.__str__(), test_post.caption)

    def test_get_image_path(self):
        test_post = self.create_post()
        filename = 'default.jpg'
        path = 'posts/' + test_post.author.username + '/default.jpg'
        created_path = get_image_path(test_post, filename)
        self.assertEqual(path, created_path)

    def test_get_absolute_url(self):
        test_post = self.create_post()
        url = '/post/' + str(test_post.pk) + '/'
        self.assertEqual(url, test_post.get_absolute_url())

    def test_get_api_like_url(self):
        test_post = self.create_post()
        url = '/post/' + str(test_post.pk) + '/like_api/'
        self.assertEqual(url, test_post.get_api_like_url())

    #def test_save(self):


class CommentTest(TestCase):
    def create_comment(
        self,
        post=Post.objects.create(caption="#selfie",
                                date_posted=timezone.now(),
                                author=User.objects.create_user(
                                        username=str(random.randint(1,100000)),
                                        password='12345'),
                                photo=SimpleUploadedFile(
                                        name='test_image.jpg',
                                        content=open('./media/default.jpg',
                                                     'rb').read(),
                                        content_type='image/jpeg'),
                                location="New York"),
        author=User.objects.create_user(username=str(random.randint(1,100000)),
                                       password='12345'),
                       text="Great shot"):
        return Comment.objects.create(post=post,
                                      author=author,
                                      text=text,
                                      date_posted=timezone.now())

    def test_comment_creation(self):
        test_comment = self.create_comment()
        self.assertTrue(isinstance(test_comment, Comment))
        self.assertEqual(test_comment.__str__(), test_comment.text)
