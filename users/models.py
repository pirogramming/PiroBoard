from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='기본프로필.png', upload_to='profile_pics')
    group = models.ManyToManyField('Group', through='GroupMember', related_name="groups", blank=True, null=True)


    def __str__(self):
        return f'{self.user.username} Profile'


class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_img = models.ImageField(blank=True, null=True)
    group_info = models.TextField()
    group_users = models.ManyToManyField(Profile, through='GroupMember', related_name="people")

    GROUP_OPEN_STATUS_CHOICES=(
        ('n', '비공개'),
        ('s', '검색만가능'),
        ('o', '공개'),
    )

    group_open_status=models.CharField(
        max_length=1,
        choices=GROUP_OPEN_STATUS_CHOICES,
        default='o',
    )


    def __str__(self):
        return self.group_name

    # master_id = models.ForeignKey(Profile, related_name="slave_group", on_delete=models.CASCADE)


class GroupMember(models.Model):
    person = models.ForeignKey(Profile, related_name='membership', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='membership', on_delete=models.CASCADE)


    STATUS_CHOICES = (
        ('p', 'PENDING'),
        ('a', 'ACCEPTED'),
        ('r', 'REFUSE')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
