from django.contrib import admin
from .models import books,Order,TrackUpdate

# Register your models here.
admin.site.register(books),
admin.site.register(Order),
admin.site.register(TrackUpdate),