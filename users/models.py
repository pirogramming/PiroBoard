from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='기본프로필.png', upload_to='profile_pics')
    phone_number = models.CharField(blank=True, max_length=20, null=True)
    region = models.CharField(blank=True, max_length=50, null=True)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    #interests = models.ManyToManyField('Interest', max_length=20, blank=True, null=True, related_name='users')
    group = models.ManyToManyField('Group', through='GroupMember', related_name="people")

    def __str__(self):
        return f'{self.user.username} Profile'


class Interest(models.Model):
    # STATUS_CHOICES = (
    #     ('음식', '음식'),
    #     ('스포츠', '스포츠'),
    #     ('코딩', '코딩'),
    #     ('여행', '여행'),
    #     ('컴퓨터', '컴퓨터'),
    #     ('게임', '게임'),
    #     ('영화', '영화'),
    #     ('언어', '언어'),
    #     ('예술', '예술'),
    #     ('음악', '음악'),
    #     ('경훈', '경훈'),
    # )
    name = models.CharField(max_length=10, blank=True, null=True)

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


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()