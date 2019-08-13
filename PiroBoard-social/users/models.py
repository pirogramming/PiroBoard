from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/pic.png', upload_to='profile_pics')

    group = models.ManyToManyField('Group', through='GroupMember', related_name="people")

    def __str__(self):
        return f'{self.user.username} Profile'


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_img = models.ImageField(blank=True, null=True)
    group_info = models.TextField()
    # master_id = models.ForeignKey(Profile, related_name="slave_group", on_delete=models.CASCADE)


class GroupMember(models.Model):
    person = models.ForeignKey('Profile', related_name='membership', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', related_name='membership', on_delete=models.CASCADE)

    STATUS_CHOICES = (
        ('p', 'PENDING'),
        ('a', 'ACCEPTED'),
        ('r', 'REFUSE')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

