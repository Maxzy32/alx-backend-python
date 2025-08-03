from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

from .models import Message, MessageHistory




@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                instance.edited = True  # Mark as edited
                MessageHistory.objects.create(
                    original_message=old_message,
                    previous_content=old_message.content
                )
        except Message.DoesNotExist:
            pass
