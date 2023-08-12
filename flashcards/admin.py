from django.contrib import admin
from .models import FlashCard, Room, Message


# Register your models here.
admin.site.register(FlashCard)
admin.site.register(Room)
admin.site.register(Message)

