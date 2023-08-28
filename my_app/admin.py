from django.contrib import admin
from .models import Category, Post, User, Aboutus, Contactus, Donation, UserNotification

# Register your models here.

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Aboutus)
admin.site.register(Contactus)
admin.site.register(Donation)
admin.site.register(UserNotification)