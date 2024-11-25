from django.contrib import admin
from .models import Post, User,Category,Tag,Comment

admin.site.register(Post)
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)