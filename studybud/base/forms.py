from dataclasses import field, fields
from django.forms import ModelForm
from .models import Message, Room


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'


class MessageForm(ModelForm):
    class Meta:
        model=Message
        fields='__all__'