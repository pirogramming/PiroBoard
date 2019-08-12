from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime
from random import random

from django.conf import settings

from django.db import models
from django.db.models import signals
from django.template.loader import render_to_string
try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor

# from django.contrib.sites.models import Site
from django.contrib.auth.models import User


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
    to_user = models.ForeignKey(User, related_name='Membership.to_user+', on_delete=models.CASCADE)
    from_group = models.ForeignKey(Group, related_name='Membership.from_group+', on_delete=models.CASCADE)

    added = models.DateField(default=datetime.now)

    objects = MembershipManager()

    class Meta:
        unique_together = (('to_user', 'from_group'),)



#
# class Contact(models.Model):
#     """
#     A contact is a person known by a user who may or may not themselves
#     be a user.
#     """
#
#     # the user who created the contact
#     user = models.ForeignKey(User, related_name="contacts",on_delete=models.ForeignKey)
#
#     name = models.CharField(max_length=100, null=True, blank=True)
#     email = models.EmailField()
#     added = models.DateField(default=datetime.now)
#
#     # the user(s) this contact correspond to
#     users = models.ManyToManyField(User)
#
#     def __unicode__(self):
#         return "%s (%s's contact)" % (self.email, self.user)
#
#
# INVITE_STATUS = (
#     ("1", "Created"),
#     ("2", "Sent"),
#     ("3", "Failed"),
#     ("4", "Expired"),
#     ("5", "Accepted"),
#     ("6", "Declined"),
#     ("7", "Joined Independently"),
#     ("8", "Deleted")
# )
#
#
# class JoinInvitationManager(models.Manager):
#
#     def send_invitation(self, from_user, to_email, message):
#         contact, created = Contact.objects.get_or_create(email=to_email, user=from_user)
#         salt = sha_constructor(str(random())).hexdigest()[:5]
#         confirmation_key = sha_constructor(salt + to_email).hexdigest()
#
#         accept_url = u"http://%s%s" % (
#             unicode(Site.objects.get_current()),
#             reverse("friends_accept_join", args=(confirmation_key,)),
#         )
#
#         ctx = {
#             "SITE_NAME": settings.SITE_NAME,
#             "CONTACT_EMAIL": settings.CONTACT_EMAIL,
#             "user": from_user,
#             "message": message,
#             "accept_url": accept_url,
#         }
#
#         subject = render_to_string("friends/join_invite_subject.txt", ctx)
#         email_message = render_to_string("friends/join_invite_message.txt", ctx)
#
#         send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, [to_email])
#         return self.create(from_user=from_user, contact=contact, message=message, status="2",
#                            confirmation_key=confirmation_key)
#
#
# class JoinInvitation(models.Model):
#     """
#     A join invite is an invitation to join the site from a user to a
#     contact who is not known to be a user.
#     """
#
#     from_group = models.ForeignKey(Group, related_name="groups2", on_delete=models.CASCADE)
#     contact = models.ForeignKey(Contact,on_delete=models.CASCADE)
#     message = models.TextField()
#     sent = models.DateField(default=datetime.now)
#     status = models.CharField(max_length=1, choices=INVITE_STATUS)
#     confirmation_key = models.CharField(max_length=40)
#
#     objects = JoinInvitationManager()
#
#     def accept(self, new_user):
#         # mark invitation accepted
#         self.status = "5"
#         self.save()
#         # auto-create friendship
#         friendship = Membership(to_user=new_user, from_user=self.from_user)
#         friendship.save()
#         # notify
#         if notification:
#             notification.send([self.from_user], "join_accept", {"invitation": self, "new_user": new_user})
#             friends = []
#             for user in friend_set_for(new_user) | friend_set_for(self.from_user):
#                 if user != new_user and user != self.from_user:
#                     friends.append(user)
#             notification.send(friends, "friends_otherconnect", {"invitation": self, "to_user": new_user})
#
#
# class FriendshipInvitationManager(models.Manager):
#
#     def invitations(self, *args, **kwargs):
#         return self.filter(*args, **kwargs).exclude(status__in=["6", "8"])
#
#
# class FriendshipInvitation(models.Model):
#     """
#     A frienship invite is an invitation from one user to another to be
#     associated as friends.
#     """
#
#     from_group = models.ForeignKey(Group, related_name="groups", on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name="invitations_to",on_delete=models.CASCADE)
#     message = models.TextField()
#     sent = models.DateField(default=datetime.now)
#     status = models.CharField(max_length=1, choices=INVITE_STATUS)
#
#     objects = FriendshipInvitationManager()
#
#     def accept(self):
#         if not Friendship.objects.are_friends(self.to_user, self.from_user):
#             friendship = Friendship(to_user=self.to_user, from_user=self.from_user)
#             friendship.save()
#             self.status = "5"
#             self.save()
#             if notification:
#                 notification.send([self.from_user], "friends_accept", {"invitation": self})
#                 notification.send([self.to_user], "friends_accept_sent", {"invitation": self})
#                 for user in friend_set_for(self.to_user) | friend_set_for(self.from_user):
#                     if user != self.to_user and user != self.from_user:
#                         notification.send([user], "friends_otherconnect", {"invitation": self, "to_user": self.to_user})
#
#     def decline(self):
#         if not Membership.objects.are_friends(self.to_user, self.from_user):
#             self.status = "6"
#             self.save()
#
#
# class FriendshipInvitationHistory(models.Model):
#     """
#     History for friendship invitations
#     """
#
#     from_user = models.ForeignKey(User, related_name="invitations_from_history",on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name="invitations_to_history",on_delete=models.CASCADE)
#     message = models.TextField()
#     sent = models.DateField(default=datetime.now)
#     status = models.CharField(max_length=1, choices=INVITE_STATUS)
#
#
#
# def delete_friendship(sender, instance, **kwargs):
#     friendship_invitations = FriendshipInvitation.objects.filter(to_user=instance.to_user, from_user=instance.from_user)
#     for friendship_invitation in friendship_invitations:
#         if friendship_invitation.status != "8":
#             friendship_invitation.status = "8"
#             friendship_invitation.save()
#
#
# signals.pre_delete.connect(delete_friendship, sender=Membership)
#
#
# # moves existing friendship invitation from user to user to FriendshipInvitationHistory before saving new invitation
# def friendship_invitation(sender, instance, **kwargs):
#     friendship_invitations = FriendshipInvitation.objects.filter(to_user=instance.to_user, from_user=instance.from_user)
#     for friendship_invitation in friendship_invitations:
#         FriendshipInvitationHistory.objects.create(
#             from_user=friendship_invitation.from_user,
#             to_user=friendship_invitation.to_user,
#             message=friendship_invitation.message,
#             sent=friendship_invitation.sent,
#             status=friendship_invitation.status
#
#         )
#         friendship_invitation.delete()
#
#
# signals.pre_save.connect(friendship_invitation, sender=FriendshipInvitation)
