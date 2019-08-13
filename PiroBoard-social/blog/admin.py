from django.contrib import admin
from .models import Post, Group, Membership,MembershipManager

admin.site.register(Post)

admin.site.register(Group)


admin.site.register(Membership)

