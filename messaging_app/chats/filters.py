import django_filters
from .models import Message
from django_filters import rest_framework as filters

class MessageFilter(filters.FilterSet):
    sent_after = filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender_email = filters.CharFilter(field_name="sender__email", lookup_expr='iexact')

    class Meta:
        model = Message
        fields = ['sent_after', 'sent_before', 'sender_email']
