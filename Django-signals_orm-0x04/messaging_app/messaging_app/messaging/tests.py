

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from messaging.models import Message, Notification

User = get_user_model()

class SignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass', email='sender@example.com')
        self.receiver = User.objects.create_user(username='receiver', password='pass', email='receiver@example.com')

    def test_notification_created_on_new_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        notifications = Notification.objects.filter(user=self.receiver, message=msg)
        self.assertEqual(notifications.count(), 1)
