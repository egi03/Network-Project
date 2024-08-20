from django.contrib import admin
from .models import User, Follow, Like, Post


admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Post)