import uuid
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')


 # Threading support
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"From {self.sender} ➜ {self.receiver} ({self.timestamp})"

    def get_all_replies(self):
        """Recursively fetch all replies to this message"""
        replies = []
        for reply in self.replies.all():
            replies.append(reply)
            replies.extend(reply.get_all_replies())
        return replies
    


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message.content[:30]}"
    
class MessageHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='edit_history')
    previous_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for Message ID: {self.original_message.id}"

