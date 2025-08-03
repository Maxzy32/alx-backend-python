from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class SignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='pass123')
        self.receiver = User.objects.create_user(username='bob', password='pass123')

    def test_notification_created_on_message(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello Bob!")
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)

    def test_edit_message_creates_history(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Original")
        msg.content = "Edited content"
        msg.save()

        history = MessageHistory.objects.filter(original_message=msg)
        self.assertTrue(msg.edited)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().previous_content, "Original")
