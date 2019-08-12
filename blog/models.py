from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Group(models.Model):
    group_creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    group_info = models.TextField()
    group_img = models.ImageField(blank=True)
    created_date = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.group_name


class MembershipManager(models.Manager):

    def friends_for_user(self, user):
        groups = []
        for membership in self.filter(from_user=user).select_related(depth=1):
            groups.append({"user": membership.to_user, "membership": membership})
        for membership in self.filter(to_user=user).select_related(depth=1):
            groups.append({"user": membership.from_user, "membership": membership})
        return groups

    def are_friends(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2).count() > 0:
            return True
        if self.filter(from_user=user2, to_user=user1).count() > 0:
            return True
        return False

    def remove(self, user1, user2):
        if self.filter(from_user=user1, to_user=user2):
            membership = self.filter(from_user=user1, to_user=user2)
        elif self.filter(from_user=user2, to_user=user1):
            membership = self.filter(from_user=user2, to_user=user1)
        membership.delete()


class Membership(models.Model):
    to_user = models.ForeignKey(User, related_name="friends",on_delete=models.CASCADE)
    from_group = models.ForeignKey(Group, related_name="groups",on_delete=models.CASCADE)

    added = models.DateField(default=datetime.now)

    objects = MembershipManager()

    class Meta:
        unique_together = (('to_user', 'from_group'),)
