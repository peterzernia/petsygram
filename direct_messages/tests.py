from django.test import TestCase
from .models import DirectMessage
from django.contrib.auth.models import User
from django.utils import timezone
import random


class DirectMessageTest(TestCase):
    def create_direct_message(self, sender=User.objects.create_user(username=str(random.randint(1,100000)),
                                    password='12345'),
                              receiver=User.objects.create_user(username=str(random.randint(1,100000)),
                                                                password='12345'),
                              content="Test Message"):
        return DirectMessage.objects.create(sender=sender,
                                            receiver=receiver,
                                            content=content,
                                            date_sent=timezone.now())

    def test_direct_message_creation(self):
        test_direct_message = self.create_direct_message()
        self.assertTrue(isinstance(test_direct_message, DirectMessage))
        self.assertEqual(test_direct_message.__str__(), test_direct_message.content)
