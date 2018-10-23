from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import random


class ProfileTest(TestCase):
    def create_profile(self, user=User.objects.create_user(username=str(random.randint(1,100000)),
                                    password='12345'),
                       image=SimpleUploadedFile(name='default.jpg',
                                                content=open('./media/default.jpg',
                                                             'rb').read(),
                                                content_type='image/jpeg')):
        return Profile.objects.create(user=user, image=image)

    def test_profile_creation(self):
        test_profile = self.create_profile()
        self.assertTrue(isinstance(test_profile, Profile))
        self.assertEqual(f'{test_profile.user.username} Profile', test_profile.__str__())

    #def test_save(self):
